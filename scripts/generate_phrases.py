#!/usr/bin/env python3
import argparse
import csv
import logging
from itertools import product

def load_seeds(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def expand_phrases(seeds, prefixes=None, suffixes=None):
    prefixes = prefixes or ['']
    suffixes = suffixes or ['']
    combos = []
    for seed in seeds:
        for pre, suf in product(prefixes, suffixes):
            phrase = f"{pre}{seed}{suf}".strip()
            combos.append(phrase)
    return sorted(set(combos))

def write_combos(combos, out_path):
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['phrase'])
        for phrase in combos:
            writer.writerow([phrase])

def main():
    parser = argparse.ArgumentParser(
        description='Generate phrase combos from seed list'
    )
    parser.add_argument('--input', '-i', required=True, help='Path to seeds.txt')
    parser.add_argument('--output', '-o', default='../output/combos.csv',
                        help='Output CSV path')
    parser.add_argument('--prefixes', '-p', nargs='*',
                        help='Optional list of prefixes')
    parser.add_argument('--suffixes', '-s', nargs='*',
                        help='Optional list of suffixes')
    args = parser.parse_args()

    logging.basicConfig(filename='../output/run.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('Loading seeds from %s', args.input)
    seeds = load_seeds(args.input)

    logging.info('Expanding phrases (prefixes=%s, suffixes=%s)',
                 args.prefixes, args.suffixes)
    combos = expand_phrases(seeds, args.prefixes, args.suffixes)

    logging.info('Writing %d combos to %s', len(combos), args.output)
    write_combos(combos, args.output)
    logging.info('Done')

if __name__ == '__main__':
    main()
