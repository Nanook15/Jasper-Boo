import os
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv("AWIN_API_TOKEN")
publisher_id = os.getenv("AWIN_PUBLISHER_ID")

url = f"https://api.awin.com/publishers/{publisher_id}/programmes"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(response.text[:500])
