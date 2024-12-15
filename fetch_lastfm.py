#!/usr/bin/env python3

import os
import json
from datetime import datetime
import pylast
from dotenv import load_dotenv
from collections import Counter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_lastfm_client():
    """Initialize and return Last.fm client"""
    load_dotenv()
    
    api_key = os.getenv('LASTFM_API_KEY')
    username = os.getenv('LASTFM_USERNAME')
    
    if not api_key or not username:
        raise ValueError("Please set LASTFM_API_KEY and LASTFM_USERNAME in your .env file")
    
    return pylast.LastFMNetwork(api_key=api_key), username

def fetch_lastfm_data(year):
    """Fetch Last.fm data for a specific year"""
    try:
        network, username = get_lastfm_client()
        user = network.get_user(username)
        
        # Get all tracks for the year
        from_date = int(datetime(year, 1, 1).timestamp())
        to_date = int(datetime(year, 12, 31, 23, 59, 59).timestamp())
        
        logger.info(f"Fetching scrobbles from {datetime.fromtimestamp(from_date)} to {datetime.fromtimestamp(to_date)}")
        
        # Get recent tracks with the from/to timestamps
        tracks = user.get_recent_tracks(limit=None, time_from=from_date, time_to=to_date)
        
        # Process track data
        artists = Counter()
        albums = Counter()
        total_scrobbles = 0
        
        logger.info("Processing scrobbles...")
        for track in tracks:
            artists[track.track.artist.name] += 1
            # Some tracks might not have album info
            if track.album:
                albums[f"{track.track.artist.name} - {track.album}"] += 1
            total_scrobbles += 1
        
        logger.info(f"Processed {total_scrobbles} scrobbles")
        
        return {
            'top_artists': artists.most_common(10),
            'top_albums': albums.most_common(10),
            'total_scrobbles': total_scrobbles,
            'fetched_at': datetime.now().isoformat(),
            'year': year
        }
    except Exception as e:
        logger.error(f"Error fetching Last.fm data: {str(e)}")
        return None

def save_lastfm_data(data, output_file):
    """Save Last.fm data to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved Last.fm data to {output_file}")

def load_lastfm_data(json_file):
    """Load Last.fm data from JSON file"""
    with open(json_file, 'r') as f:
        return json.load(f)

def main(year=None, output_file=None, force=False):
    """Main function to fetch and save Last.fm data"""
    if year is None:
        year = datetime.now().year
    if output_file is None:
        output_file = f"lastfm_{year}.json"
    
    # Check if data file exists and is not forced to refresh
    if os.path.exists(output_file) and not force:
        logger.info(f"Using existing Last.fm data from {output_file}")
        return load_lastfm_data(output_file)
    
    # Fetch new data
    logger.info(f"Fetching Last.fm data for {year}...")
    data = fetch_lastfm_data(year)
    
    if data:
        save_lastfm_data(data, output_file)
        return data
    
    return None

if __name__ == "__main__":
    main()
