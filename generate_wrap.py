#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import fetch_collection
import generate_report

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Vinyl Unwrapped report for a specific year')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                      help='Year to generate the report for (defaults to current year)')
    return parser.parse_args()

def main():
    args = parse_args()
    year = args.year
    
    # Update the year and output file in fetch_collection
    fetch_collection.YEAR = year
    fetch_collection.OUTPUT_FILE = f"collection_{year}.json"
    
    # Run fetch collection
    print(f"Fetching collection data for {year}...")
    fetch_collection.main()
    
    # Run generate report
    print(f"Generating report for {year}...")
    generate_report.main()
    
    print(f"Report generation complete for {year}!")

if __name__ == "__main__":
    main()
