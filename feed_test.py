import os
import csv
import json
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("AWIN_API_TOKEN")
PUBLISHER_ID = os.getenv("AWIN_PUBLISHER_ID")
DEALS_FILE = os.path.expanduser("~/kids-deals/pending_deals.json")

# Test data matching real Awin feed format
TEST_FEED = [
    {
        "id": "FRUGI001",
        "title": "Frugi Boys Sam Striped Hoodie Age 5-6",
        "price": "18.00",
        "rrp": "36.00",
        "merchant": "Frugi",
        "merchant_id": "4459",
        "url": "https://www.frugi.com/sample",
        "image_url": "",
        "category": "Childrenswear",
        "in_stock": True
    },
    {
        "id": "VERT001",
        "title": "Vertbaudet Girls Padded Jacket Age 12",
        "price": "24.00",
        "rrp": "48.00",
        "merchant": "Vertbaudet",
        "merchant_id": "3636",
        "url": "https://www.vertbaudet.co.uk/sample",
        "image_url": "",
        "category": "Childrenswear",
        "in_stock": True
    },
    {
        "id": "VERT002",
        "title": "Vertbaudet Boys Joggers Age 6",
        "price": "9.00",
        "rrp": "18.00",
        "merchant": "Vertbaudet",
        "merchant_id": "3636",
        "url": "https://www.vertbaudet.co.uk/sample2",
        "image_url": "",
        "category": "Childrenswear",
        "in_stock": True
    },
    {
        "id": "PATPAT001",
        "title": "PatPat Girls Floral Dress Age 11-12",
        "price": "12.00",
        "rrp": "14.00",
        "merchant": "PatPat",
        "merchant_id": "15189",
        "url": "https://www.patpat.com/sample",
        "image_url": "",
        "category": "Childrenswear",
        "in_stock": True
    }
]

MIN_DISCOUNT_PCT = 30  # Only surface deals with 30%+ off

def calculate_discount(price, rrp):
    try:
        p = float(price)
        r = float(rrp)
        if r > 0 and r > p:
            return round((1 - p/r) * 100)
    except:
        pass
    return 0

def filter_deals(feed):
    good_deals = []
    for item in feed:
        discount = calculate_discount(item["price"], item["rrp"])
        if discount >= MIN_DISCOUNT_PCT and item["in_stock"]:
            item["discount_pct"] = discount
            item["fetched_at"] = datetime.now().isoformat()
            good_deals.append(item)
    return good_deals

def save_pending(deals):
    with open(DEALS_FILE, "w") as f:
        json.dump(deals, f, indent=2)

if __name__ == "__main__":
    print(f"Processing {len(TEST_FEED)} products...")
    deals = filter_deals(TEST_FEED)
    print(f"Found {len(deals)} deals with {MIN_DISCOUNT_PCT}%+ discount:")
    for d in deals:
        print(f"  {d['discount_pct']}% off | {d['title']} | £{d['price']} was £{d['rrp']}")
    save_pending(deals)
    print(f"\nSaved to pending_deals.json — ready for Telegram approval")
