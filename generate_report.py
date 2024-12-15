from datetime import datetime
from collections import Counter
import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_month_id(month):
    """Create a valid HTML ID from a month name"""
    return f"month-{month.lower().replace(' ', '-')}"

def load_collection(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def analyze_collection(data, year=None):
    # Use provided year or current year as fallback
    if year is None:
        year = datetime.now().year
        
    # Filter out records without russ.fm URLs
    data = [record for record in data if record['album_uri'] is not None and record['artist_uri'] is not None]
    
    total_records = len(data)
    
    # Sort all records by date
    sorted_records = sorted(data, key=lambda x: x['date_added'])
    
    # Count by month
    monthly_adds = Counter()
    for item in data:
        date_added = datetime.fromisoformat(item['date_added'])
        monthly_adds[date_added.strftime('%B')] += 1
    
    # Most common genres and styles
    genres = Counter()
    styles = Counter()
    
    for item in data:
        for genre in item['genres']:
            genres[genre] += 1
        for style in item.get('styles', []):
            styles[style] += 1
    
    # Format analysis
    formats = Counter()
    for item in data:
        for format_info in item['formats']:
            format_desc = f"{format_info['name']} ({', '.join(format_info['descriptions'])})"
            formats[format_desc] += 1
    
    # Labels analysis
    labels = Counter()
    for item in data:
        for label in item['labels']:
            labels[label] += 1
    
    # Records by month (for chart)
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data = [monthly_adds[month] for month in months_order]
    
    # Group records by month for display
    records_by_month = {}
    for item in sorted_records:
        date_added = datetime.fromisoformat(item['date_added'])
        month = date_added.strftime('%B')
        if month not in records_by_month:
            records_by_month[month] = []
        records_by_month[month].append(item)
    
    # Create month IDs for linking
    month_ids = {month: create_month_id(month) for month in months_order}
    
    # Get top artists with their record counts and images
    artist_counts = {}
    artist_records = {}
    artist_images = {}
    
    for item in data:
        artists = item.get('artist', [])
        if isinstance(artists, str):
            artists = [artists]
        artist_key = ' & '.join(artists) if len(artists) > 1 else artists[0]
        
        if artist_key not in artist_counts:
            artist_counts[artist_key] = 0
            artist_records[artist_key] = []
            # Use the first artist's image for combined artists
            artist_images[artist_key] = item.get('artist_image', '')
            
        artist_counts[artist_key] += 1
        artist_records[artist_key].append(item)
    
    # Prepare top artists data
    top_artists_data = []
    for artist, count in sorted(artist_counts.items(), key=lambda x: x[1], reverse=True):
        if artist.lower() != "various":  # Skip 'Various' artists
            top_artists_data.append({
                'name': artist,
                'count': count,
                'image': artist_images[artist],
                'records': artist_records[artist]
            })
            if len(top_artists_data) == 12:  # Only take top 12 non-Various artists
                break
    
    return {
        'total_records': total_records,
        'monthly_adds': dict(monthly_adds),
        'top_genres': dict(genres.most_common(5)),
        'top_styles': dict(styles.most_common(5)),
        'top_formats': dict(formats.most_common(5)),
        'top_labels': dict(labels.most_common(5)),
        'monthly_data': monthly_data,
        'months': months_order,
        'month_ids': month_ids,
        'records_by_month': records_by_month,
        'top_artists': top_artists_data,
        'recent_additions': sorted(data, key=lambda x: x['date_added'], reverse=True)[:10],
        'year': year,
        'genres': dict(genres),
        'styles': dict(styles),
        'formats': dict(formats),
        'labels': dict(labels),
        'artists': artist_counts  # Use the new artist_counts dictionary
    }

def generate_html(stats, lastfm_data=None, template_dir='templates'):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html')
    
    # Check for existence of adjacent year folders
    current_year = stats['year']
    unwrapped_dir = Path('unwrapped')
    prev_year_exists = (unwrapped_dir / str(current_year - 1)).exists()
    next_year_exists = (unwrapped_dir / str(current_year + 1)).exists()
    
    return template.render(
        stats=stats,
        lastfm_data=lastfm_data,
        current_year=current_year,
        prev_year_exists=prev_year_exists,
        next_year_exists=next_year_exists
    )

def main(year=None, output_path=None, lastfm_data=None):
    # Use current directory if no output path provided
    if output_path is None:
        output_path = os.getcwd()
        
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Load and analyze collection from main directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    collection_file = os.path.join(base_dir, f'collection_{year}.json')
    
    logger.info(f"Loading collection from {collection_file}")
    collection = load_collection(collection_file)
    stats = analyze_collection(collection, year)
    
    # Log Last.fm data status
    logger.info(f"Generating report with Last.fm data: {lastfm_data is not None}")
    if lastfm_data:
        logger.info(f"Last.fm data includes {lastfm_data['total_scrobbles']} scrobbles")
    
    # Generate HTML
    html_content = generate_html(stats, lastfm_data, template_dir=os.path.join(os.path.dirname(__file__), 'templates'))
    
    # Write HTML file
    output_file = os.path.join(output_path, 'index.html')
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    logger.info(f"Report generated: {output_file}")

if __name__ == "__main__":
    main()
