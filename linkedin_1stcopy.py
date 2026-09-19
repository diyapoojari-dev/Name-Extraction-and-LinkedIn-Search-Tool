import spacy
import requests
import time
import re

nlp = spacy.load("en_core_web_trf")

input_file = "text.txt"
output_file = "linked_in_profiles.txt"

search_engine_id = "d3673e81214b84054"
google_api_key = "AIzaSyA7r0EnPzIxTFj2hxif2GdU7ZKir0wIb5Q"

# Name filtering logic with help from ChatGPT
def is_real_person(name):
    url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        "query": name,
        "key": google_api_key,
        "limit": 1,
        "indent": True
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("itemListElement"):
            types = data["itemListElement"][0]["result"].get("@type", [])
            return "Person" in types
    except:
        pass
    return False

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)
raw_names = set(ent.text for ent in doc.ents if ent.label_ == "PERSON")

#LLM
clean_names = set()
for name in raw_names:
    name = name.strip(" \"'“”‘’\n\t\r")
    if len(name.split()) < 2:
        continue
    if any(char.isdigit() for char in name):
        continue
    if not re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)+$", name):
        continue
    clean_names.add(name)

candidate_names = clean_names
print(f"Found {len(candidate_names)} names.\n")



with open(output_file, "w", encoding="utf-8") as f:
    for name in sorted(candidate_names):
        if is_real_person(name):
            search_name = "+".join(name.split())
            link = f"https://www.google.com/search?q={search_name}+site:linkedin.com/in&cx={search_engine_id}"
            f.write(f"{name} → {link}\n")
        time.sleep(1)

print(f"Saved results to '{output_file}'.")

