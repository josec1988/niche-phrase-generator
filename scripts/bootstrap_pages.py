#!/usr/bin/env python3
import os, csv, re

TEMPLATE = """# {base}

## Introduction
*Write a compelling intro to `{base}` here.*

## Top Products
1. [Product 1](AFFILIATE_LINK) — short description.
2. [Product 2](AFFILIATE_LINK) — short description.
3. [Product 3](AFFILIATE_LINK) — short description.
4. [Product 4](AFFILIATE_LINK) — short description.
5. [Product 5](AFFILIATE_LINK) — short description.

## Conclusion
*Call to action.*
"""

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

os.makedirs("pages", exist_ok=True)
with open("output/filtered.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        base = row["base"]
        slug = slugify(base)
        folder = os.path.join("pages", slug)
        os.makedirs(folder, exist_ok=True)
        md = os.path.join(folder, "README.md")
        if not os.path.exists(md):
            with open(md, "w", encoding="utf-8") as o:
                o.write(TEMPLATE.format(base=base))
            print("Created", md)
