import json
import os
from datetime import datetime

APPROVED_FILE = os.path.expanduser("~/kids-deals/approved_deals.json")
OUTPUT_FILE = os.path.expanduser("~/kids-deals/index.html")

def build_page(deals):
    items = ""
    for deal in deals.values():
        items += f"""
        <div class="deal">
            <h2>{deal['title']}</h2>
            <p class="price">{deal['price']} <s>{deal['was']}</s> &mdash; {deal['discount']}</p>
            <p class="merchant">{deal['merchant']}</p>
            <a href="{deal['url']}" target="_blank">View Deal &rarr;</a>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Today's Kids Deals</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #fff; }}
        .disclosure {{ font-size: 0.8em; color: #888; margin-bottom: 30px; padding: 10px; background: #f9f9f9; border-radius: 6px; }}
        .deal {{ border: 1px solid #eee; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
        .deal h2 {{ margin: 0 0 8px 0; font-size: 1em; }}
        .price {{ font-weight: bold; color: #e44; margin: 4px 0; }}
        .was {{ text-decoration: line-through; color: #999; font-weight: normal; }}
        .merchant {{ color: #888; font-size: 0.85em; margin: 4px 0; }}
        a {{ display: inline-block; margin-top: 8px; background: #222; color: #fff; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-size: 0.9em; }}
        .updated {{ font-size: 0.75em; color: #bbb; text-align: right; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>Today's Kids Deals 👕</h1>
    <div class="disclosure">
        Some links on this page are affiliate links — we earn a small commission 
        if you buy, at no extra cost to you. We only share deals we'd actually 
        buy for our own kids.
    </div>
    {items}
    <p class="updated">Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}</p>
</body>
</html>"""
    return html

if __name__ == "__main__":
    if not os.path.exists(APPROVED_FILE):
        print("No approved deals yet.")
        exit()

    with open(APPROVED_FILE) as f:
        deals = json.load(f)

    html = build_page(deals)
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"Published {len(deals)} deals to {OUTPUT_FILE}")
