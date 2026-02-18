import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

url = f"https://api.awin.com/publishers/{publisher_id}/programmes"
headers = {"Authorization": f"Bearer {token}"}
params = {
    "relationship": "notjoined",
    "countryCode": "GB"
}

response = requests.get(url, headers=headers, params=params)
programmes = response.json()

keywords = ["kids", "child", "children", "baby", "boden", "next", "jojo", "mini", "monsoon", "mothercare", "john lewis", "marks", "joules", "frugi", "vertbaudet"]

matches = []
for p in programmes:
    name = p.get("name") or ""
    desc = p.get("description") or ""
    name = name.lower()
    desc = desc.lower()
    if any(k in name or k in desc for k in keywords):
        matches.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "sector": p.get("primarySector")
        })

print(f"Found {len(matches)} potential kids clothing merchants:\n")
for m in matches:
    print(f"ID: {m['id']} | {m['name']} | {m['sector']}")
