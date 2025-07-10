#!/usr/bin/env python3
import os, json, csv, requests

# Load API keys (we won’t actually hit Bing in stub mode)
cfg = json.load(open(os.path.join(os.path.dirname(__file__), "../config/api_keys.json")))
BING_KEY      = cfg["bing_autosuggest"]["key"]
ENDPOINT_BASE = cfg["bing_autosuggest"]["endpoint"].rstrip("/")
SUGGEST_URL   = f"{ENDPOINT_BASE}/bing/v7.0/suggestions"

def fetch_suggestions(phrase):
    try:
        headers = {"Ocp-Apim-Subscription-Key": BING_KEY}
        params  = {"q": phrase, "mkt": "en-US", "count": 5}
        res = requests.get(SUGGEST_URL, headers=headers, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
        return [
            s["displayText"]
            for grp in data.get("suggestionGroups", [])
            for s in grp.get("searchSuggestions", [])
        ][:5]
    except Exception as e:
        print(f"[stub] Autocomplete API failed for “{phrase}” ({e}), using dummy suggestions")
        return [f"{phrase} suggestion {i}" for i in range(1, 6)]

def main():
    infile = os.path.join("output", "combos.csv")
    outfile = os.path.join("output", "augmented.csv")
    with open(infile, newline="", encoding="utf-8") as fin, \
         open(outfile, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        fieldnames = ["base"] + [f"sugg_{i}" for i in range(1,6)]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            base = row["phrase"]
            suggestions = fetch_suggestions(base)
            row_out = {"base": base}
            for i in range(1,6):
                row_out[f"sugg_{i}"] = suggestions[i-1] if i-1 < len(suggestions) else ""
            writer.writerow(row_out)

if __name__ == "__main__":
    main()
