#fetching and saving links
import requests

rss_url = "https://economictimes.indiatimes.com/rssfeeds/110870909.cms"
output_file = "input.txt"  

try: 
    
    response = requests.get(rss_url) #content of webpage 
    response.raise_for_status()  #checking error or not

   
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text) 

    print("RSS feed content has been saved to", output_file)

except Exception as e:
    print("ERROR fetching the RSS feed:", e)

