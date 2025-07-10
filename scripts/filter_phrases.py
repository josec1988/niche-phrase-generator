#!/usr/bin/env python3
import os, csv

INPUT  = os.path.join("output", "scored.csv")
OUTPUT = os.path.join("output", "filtered.csv")

# Thresholds—tweak if you like
MIN_VOLUME = 0
MIN_CPC    = 0.0
TOP_N      = 100  # how many top phrases to keep

def main():
    with open(INPUT, newline="", encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        rows = []
        for r in reader:
            vol = float(r.get("volume", 0) or 0)
            cpc = float(r.get("cpc", 0) or 0)
            if vol >= MIN_VOLUME and cpc >= MIN_CPC:
                r["score"] = vol * cpc
                rows.append(r)
        # sort by score descending
        rows.sort(key=lambda x: x["score"], reverse=True)
        # take top N
        rows = rows[:TOP_N]

    # write filtered file
    fieldnames = reader.fieldnames + ["score"]
    with open(OUTPUT, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

if __name__ == "__main__":
    main()
