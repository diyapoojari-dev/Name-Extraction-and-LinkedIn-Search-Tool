# extract links and content
import xml.etree.ElementTree as ET #parsing XML
import requests
from bs4 import BeautifulSoup #extract readable text from html


input_file = "input.txt"   
output_file = "text.txt"  


with open(input_file, "r", encoding="utf-8") as f:
    xml_data = f.read()


root = ET.fromstring(xml_data)
#parses the xml and returns the root element

links = []
for item in root.findall(".//item"):
    link_tag = item.find("link")
    if link_tag is not None and ".com" in link_tag.text:
        links.append(link_tag.text.strip())

print("Found", len(links), "links")


with open(output_file, "w", encoding="utf-8") as f:
    for url in links:
        try:
          
            res = requests.get(url, timeout=10)
            res.raise_for_status()

           
            soup = BeautifulSoup(res.text, "html.parser")
            article_text = soup.get_text(separator="\n", strip=True)

          
            f.write(article_text + "\n\n---\n\n")

            print("Saved content from", url)

        except Exception as e:
            print("Could not fetch", url)
            print("Reason:", e)