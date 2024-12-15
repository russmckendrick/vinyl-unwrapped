#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import fetch_collection
import fetch_lastfm
import generate_report
import shutil
import logging

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    unwrapped_dir = os.path.join(base_dir, 'unwrapped')
    
    # Get list of year directories
    years = []
    for item in os.listdir(unwrapped_dir):
        if item.isdigit() and os.path.isdir(os.path.join(unwrapped_dir, item)):
            years.append(item)
    years.sort(reverse=True)
    
    # Generate year cards HTML
    year_cards_html = ""
    for year in years:
        year_cards_html += f"""
            <div class="year-card">
                <a href="/{year}/" class="year-link">{year} Unwrapped</a>
            </div>"""
    
    # Create index.html
    index_path = os.path.join(unwrapped_dir, 'index.html')
    with open(index_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vinyl Unwrapped - Year by Year Stats</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: #0f172a;
            color: #e2e8f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        .header {
            text-align: center;
            padding: 4rem 0;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid #334155;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .year-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        .year-card {
            background: #1e293b;
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            transition: transform 0.2s ease-in-out;
            border: 1px solid #334155;
        }
        .year-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .year-link {
            color: #e2e8f0;
            text-decoration: none;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .year-link:hover {
            color: #38bdf8;
        }
        .description {
            max-width: 800px;
            margin: 2rem auto;
            text-align: center;
            color: #94a3b8;
        }
        footer {
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            border-top: 1px solid #334155;
            color: #94a3b8;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>Vinyl Unwrapped</h1>
            <div class="description">
                A year-by-year journey through my vinyl collection, powered by Discogs data and visualized with modern web technologies.
            </div>
        </div>
    </div>
    <main class="container">
        <div class="year-grid">
            """ + year_cards_html + """
        </div>
    </main>
    <footer>
        <p>Built with ❤️ using Discogs data</p>
    </footer>
</body>
</html>""")

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
