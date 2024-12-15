from datetime import datetime
from collections import Counter
import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def create_month_id(month):
    """Create a valid HTML ID from a month name"""
    return f"month-{month.lower().replace(' ', '-')}"

def load_collection(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def analyze_collection(data):
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
    artists = Counter()
    for item in data:
        for genre in item['genres']:
            genres[genre] += 1
        for style in item.get('styles', []):
            styles[style] += 1
        for artist in item['artist']:
            artists[artist] += 1
    
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
    
    # Get top artists with their record counts
    top_artists_data = []
    for artist, count in artists.most_common(10):
        artist_records = [record for record in data if artist in record['artist']]
        top_artists_data.append({
            'name': artist,
            'count': count,
            'records': artist_records  # Pass the full record data
        })
    
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
        'recent_additions': sorted(data, key=lambda x: x['date_added'], reverse=True)[:10]
    }

def generate_html(stats, template_dir='templates'):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html')
    
    return template.render(
        stats=stats,
        year=2024,
        generated_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

def main():
    # Create necessary directories if they don't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/css')
        os.makedirs('static/js')
    
    # Load collection data
    collection_data = load_collection('collection_2024.json')
    
    # Analyze collection
    stats = analyze_collection(collection_data)
    
    # Generate HTML report
    html_content = generate_html(stats)
    
    # Write the HTML file
    with open('vinyl_unwrapped_2024.html', 'w') as f:
        f.write(html_content)
    
    print("Report generated successfully!")

if __name__ == "__main__":
    main()
