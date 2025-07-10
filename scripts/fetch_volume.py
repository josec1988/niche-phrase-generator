#!/usr/bin/env python3
import os, json, csv
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Load Google Ads credentials
cfg = json.load(open(os.path.join(os.path.dirname(__file__), "../config/api_keys.json")))["google_ads"]
client = GoogleAdsClient.load_from_dict(cfg)
ga_service = client.get_service("GoogleAdsService")

def fetch_metrics(keyword, customer_id):
    # Safely inject keyword into query
    escaped_kw = keyword.replace("'", "\\'")
    query = f"""
      SELECT
        segments.keyword.info.text,
        metrics.average_monthly_searches,
        metrics.average_cpc
      FROM keyword_view
      WHERE segments.keyword.info.text = '{escaped_kw}'
    """
    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        vol = 0
        cpc = 0.0
        for batch in response:
            for row in batch.results:
                vol = row.metrics.average_monthly_searches or 0
                cpc = (row.metrics.average_cpc.micros or 0) / 1e6
        return vol, cpc
    except GoogleAdsException as e:
        # Permission denied or dev token not approved
        return 0, 0.0

def main():
    inp = os.path.join("output", "augmented.csv")
    out = os.path.join("output", "scored.csv")
    customer_id = cfg["login_customer_id"]

    with open(inp, newline="", encoding="utf-8") as fin, \
         open(out, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["volume", "cpc"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            kw = row["sugg_1"]
            vol, cpc = fetch_metrics(kw, customer_id)
            writer.writerow({**row, "volume": vol, "cpc": cpc})

if __name__ == "__main__":
    main()
