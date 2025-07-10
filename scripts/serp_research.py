#!/usr/bin/env python3
import os, json, csv, time, requests

cfg     = json.load(open(os.path.join(os.path.dirname(__file__),"../config/api_keys.json")))
CSE_KEY = cfg["cse"]["api_key"]
ENGINE  = cfg["cse"]["engine_id"]

def fetch_top_results(query, num=3):
    params = {
      "key": CSE_KEY,
      "cx": ENGINE,
      "q": query,
      "num": num
    }
    res = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=10).json()
    items = res.get("items", [])[:num]
    results = []
    for i, itm in enumerate(items):
        results.append({
          "position": i+1,
          "link":     itm.get("link",""),
          "title":    itm.get("title",""),
          "snippet":  itm.get("snippet","")
        })
    # pad
    while len(results) < num:
        idx = len(results)
        results.append({"position": idx+1,"link":"","title":"","snippet":""})
    return results

def main():
    inp  = os.path.join("output","filtered.csv")
    out  = os.path.join("output","serp_results.csv")
    header = ["base"]
    for i in range(1, 4):
        header += [f"url_{i}", f"title_{i}", f"snippet_{i}"]
    with open(inp) as fin, open(out,"w",newline="",encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=header)
        writer.writeheader()
        for row in reader:
            base = row["base"]
            serp = fetch_top_results(base)
            out = {"base": base}
            for item in serp:
                idx = item["position"]
                out[f"url_{idx}"]     = item["link"]
                out[f"title_{idx}"]   = item["title"]
                out[f"snippet_{idx}"] = item["snippet"]
            writer.writerow(out)
            time.sleep(1)

if __name__=="__main__":
    main()
