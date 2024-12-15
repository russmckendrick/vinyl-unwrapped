#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import fetch_collection
import fetch_lastfm
import generate_report
import shutil
import logging
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Vinyl Unwrapped report for a specific year')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                      help='Year to generate the report for (defaults to current year)')
    parser.add_argument('--lastfm', action='store_true',
                      help='Include Last.fm listening data in the report')
    parser.add_argument('--force', action='store_true',
                      help='Force regeneration of collection and Last.fm data')
    return parser.parse_args()

def setup_unwrapped_structure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    unwrapped_dir = os.path.join(base_dir, 'unwrapped')
    
    # Create base directories
    os.makedirs(unwrapped_dir, exist_ok=True)
    os.makedirs(os.path.join(unwrapped_dir, 'css'), exist_ok=True)
    os.makedirs(os.path.join(unwrapped_dir, 'js'), exist_ok=True)
    
    # Always copy static files to ensure we have the latest version
    static_dir = os.path.join(base_dir, 'static')
    if os.path.exists(static_dir):
        # Copy CSS files
        if os.path.exists(os.path.join(static_dir, 'css', 'style.css')):
            shutil.copy2(
                os.path.join(static_dir, 'css', 'style.css'),
                os.path.join(unwrapped_dir, 'css', 'style.css')
            )
            logger.info("Updated style.css in unwrapped directory")
            
        # Copy JS files
        if os.path.exists(os.path.join(static_dir, 'js', 'charts.js')):
            shutil.copy2(
                os.path.join(static_dir, 'js', 'charts.js'),
                os.path.join(unwrapped_dir, 'js', 'charts.js')
            )
            logger.info("Updated charts.js in unwrapped directory")

def generate_index_html():
    """Generate the main index.html file"""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
    # Year descriptions
    year_descriptions = {
        2024: "Explore my vinyl journey through 2024",
        2023: "Revisit the records of 2023",
        2022: "Look back at 2022's collection",
        2021: "Discover the vinyl from 2021",
        2020: "Remember the music of 2020",
        2019: "Relive 2019's additions",
        2018: "Explore the sounds of 2018",
        2017: "Journey back to 2017",
        2016: "Revisit 2016's collection",
        2015: "Where it all began"
    }
    
    # Sort years in descending order
    years = [(year, year_descriptions[year]) for year in sorted(year_descriptions.keys(), reverse=True)]
    
    # Generate HTML
    html_content = template.render(years=years)
    
    # Write to file
    output_file = os.path.join('unwrapped', 'index.html')
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    logger.info(f"Generated index page: {output_file}")

def main():
    args = parse_args()
    year = args.year
    
    # Create base directory structure
    setup_unwrapped_structure()
    
    # Create year directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    year_dir = os.path.join(base_dir, 'unwrapped', str(year))
    os.makedirs(year_dir, exist_ok=True)
    
    # Set collection file path
    collection_file = os.path.join(base_dir, f'collection_{year}.json')
    
    # Check if collection file exists
    if os.path.exists(collection_file) and not args.force:
        logger.info(f"Using existing collection file: {collection_file}")
    else:
        # Fetch collection data
        logger.info(f"Fetching collection data for {year}...")
        fetch_collection.main(year, collection_file)
    
    # Get Last.fm data if requested
    lastfm_data = None
    if args.lastfm:
        lastfm_file = os.path.join(base_dir, f'lastfm_{year}.json')
        lastfm_data = fetch_lastfm.main(year, lastfm_file, args.force)
        if lastfm_data:
            logger.info(f"Last.fm data loaded with {lastfm_data['total_scrobbles']} scrobbles")
        else:
            logger.warning("Failed to load Last.fm data")
    
    # Generate report
    logger.info(f"Generating report for {year}...")
    logger.debug(f"Passing Last.fm data to report generator: {lastfm_data is not None}")
    generate_report.main(year, year_dir, lastfm_data)
    
    # Generate/update index.html
    generate_index_html()
    
    logger.info(f"Report generation complete for {year}!")

if __name__ == "__main__":
    main()
