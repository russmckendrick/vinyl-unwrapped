# Vinyl Unwrapped 💿

Generate your own personal vinyl collection report, inspired by Spotify Wrapped! 🎵

> ⚠️ **Note**: This project is specifically designed to work with [russ.fm](https://russ.fm) for album artwork and artist images. While you can modify the code for your own use, you'll need to implement your own image handling system.

## Features 🌟

- Fetches your Discogs collection data 📚
- Generates a beautiful HTML report 📊
- Shows your vinyl collecting habits by month 📅
- Displays album artwork and artist images 🎨
- Analyzes your favorite artists and labels 🏆

## Prerequisites 🛠️

- Python 3.x
- A Discogs account and API token
- Environment variables set up (see `.env.example`)

## Installation 🔧

1. Clone this repository:
```bash
git clone https://github.com/yourusername/vinyl-unwrapped.git
cd vinyl-unwrapped
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```

## Usage 🚀

There are three main scripts:

### 1. Fetch Collection (`fetch_collection.py`)
Fetches your vinyl collection data from Discogs for a specific year:
```bash
python fetch_collection.py
```

### 2. Generate Report (`generate_report.py`)
Creates an HTML report from your collection data:
```bash
python generate_report.py
```

### 3. All-in-One Script (`generate_wrap.py`)
Runs both scripts in sequence. You can specify a year or it will use the current year:
```bash
python generate_wrap.py --year=2023  # Generate for 2023
python generate_wrap.py              # Generate for current year
```

## Output 📋

The scripts will generate:
- A JSON file with your collection data (`collection_YEAR.json`)
- An HTML report (`vinyl_unwrapped_YEAR.html`)

## Customization 🎨

You can customize the report's appearance by modifying:
- `templates/report.html` - The report template
- `static/css/styles.css` - The CSS styles

## Contributing 🤝

Feel free to fork this repository and make your own modifications. Pull requests are welcome!

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- Thanks to Discogs for their excellent API
- Inspired by Spotify Wrapped
- Album artwork and artist images powered by [russ.fm](https://russ.fm)
