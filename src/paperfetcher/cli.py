# cli.py

import argparse
import csv
import logging
from paperfetcher.fetch import search_pubmed, fetch_details


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with industry authors.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-f", "--file", help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    ids = search_pubmed(args.query)
    if not ids:
        print("No results found.")
        return

    papers = fetch_details(ids)
    if not papers:
        print("No qualifying papers found.")
        return

    if args.file:
        with open(args.file, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        print(f"Saved to {args.file}")
    else:
        for p in papers:
            print(p)


if __name__ == "__main__":
    main()
