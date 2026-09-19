import spacy
import requests
import time
import re


nlp = spacy.load("en_core_web_trf")

input_file = "text.txt"
output_file = "linked_in_profiles.txt"

SERP_API_KEY = "3bd4fcf8df5dae11b5a963ebecdbbedef65ad5b3f72b3b4c7c5b6aaac3246138"

def is_real_person(name):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": name + "www.linkedin.com/in",
        "api_key": SERP_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("organic_results", [])
        for result in results:
            link = result.get("link", "")
            if "linkedin.com/in" in link.lower():
                return True
    except:
        pass
    return False


print(f"Reading '{input_file}'...")
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

print("Extracting names...")
doc = nlp(text)
raw_names = set(ent.text for ent in doc.ents if ent.label_ == "PERSON")

# Name filtering logic with help from ChatGPT
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

print("Searching for LinkedIn profiles...")
with open(output_file, "w", encoding="utf-8") as f:
    for name in sorted(candidate_names):
        if is_real_person(name):
            search_name = "+".join(name.split())
            link = f"https://www.google.com/search?q={search_name}+site:linkedin.com/in"
            f.write(f"{name} → {link}\n")
        time.sleep(1)

print(f"\nThe results are saved in '{output_file}'.")

