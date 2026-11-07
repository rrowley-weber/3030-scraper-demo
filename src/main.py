#!/usr/bin/env python3
"""
main.py - Integrating scraper and database
Coordinates the scraping, saving, and verification steps.

Usage:
    python src/main.py [-u URL] [-o DATABASE]
"""
import argparse
import sqlite3
import sys

import requests

from database import create_states_table, save_state
from scraper import scrape_states

DEFAULT_URL = "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States"
DEFAULT_DB = "data/states.db"


def parse_args():
    parser = argparse.ArgumentParser(description="Save national parks by state to SQLite.")
    parser.add_argument("-u", "--url", default=DEFAULT_URL, help="page to scrape")
    parser.add_argument("-o", "--output", default=DEFAULT_DB, help="database file")
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Fetching {args.url} ...")
    try:
        records = scrape_states(args.url)
    except requests.exceptions.RequestException as error:
        print(f"Error: could not download page: {error}")
        sys.exit(1)
    print(f"Collected {len(records)} records.")

    print(f"Saving to {args.output} ...")
    conn = sqlite3.connect(args.output)
    create_states_table(conn)
    for record in records:
        save_state(conn, record)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM states").fetchone()[0]
    print(f"Saved {count} records.")
    conn.close()


if __name__ == "__main__":
    main()