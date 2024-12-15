import os
import shutil
from datetime import datetime
import re

def setup_directory_structure():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unwrapped')
    
    # Ensure base directories exist
    for dir_name in ['css', 'js']:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)

def copy_static_files():
    # Copy static files from source to unwrapped directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    unwrapped_dir = os.path.join(base_dir, 'unwrapped')
    
    # Copy CSS files
    if os.path.exists(os.path.join(static_dir, 'css', 'style.css')):
        shutil.copy2(
            os.path.join(static_dir, 'css', 'style.css'),
            os.path.join(unwrapped_dir, 'css', 'style.css')
        )
    
    # Copy JS files
    if os.path.exists(os.path.join(static_dir, 'js', 'charts.js')):
        shutil.copy2(
            os.path.join(static_dir, 'js', 'charts.js'),
            os.path.join(unwrapped_dir, 'js', 'charts.js')
        )

def organize_reports():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    unwrapped_dir = os.path.join(base_dir, 'unwrapped')
    
    # Find all vinyl_unwrapped files
    for file in os.listdir(base_dir):
        if file.startswith('vinyl_unwrapped_') and file.endswith('.html'):
            year_match = re.search(r'vinyl_unwrapped_(\d{4})\.html', file)
            if year_match:
                year = year_match.group(1)
                year_dir = os.path.join(unwrapped_dir, year)
                os.makedirs(year_dir, exist_ok=True)
                
                # Copy and rename the file
                shutil.copy2(
                    os.path.join(base_dir, file),
                    os.path.join(year_dir, 'index.html')
                )

def main():
    setup_directory_structure()
    copy_static_files()
    organize_reports()

if __name__ == "__main__":
    main()
