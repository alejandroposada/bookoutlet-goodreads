# BookOutlet-Goodreads Matcher

Find what books from your Goodreads to-read list are available on BookOutlet.

## Overview

This project helps you find deals on your to-read list. It works by:

1. Reading your exported Goodreads library CSV file
2. Extracting books on your "to-read" shelf
3. Searching for each book on BookOutlet
4. Outputting matches with score information

## Features

- **Smart Title Matching**: Uses multiple fuzzy matching algorithms to handle different title variations
- **Series & Edition Recognition**: Normalizes titles by removing series indicators, edition information, etc.
- **Subtitle Handling**: Properly handles books with colons and subtitles
- **Match Scoring**: Shows confidence level for each match as a percentage

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/bookoutlet-goodreads.git
cd bookoutlet-goodreads

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Exporting your Goodreads Library
1. Go to Goodreads.com → My Books
2. Click on "Import and Export" (bottom left)
3. Select "Export Library"
4. Download the CSV file (usually named "goodreads_library_export.csv")

### Running the Tool
```bash
python run.py --csv path/to/your/goodreads_library_export.csv --output results.txt --threshold 90
```

### Arguments
- `--csv`: Path to your Goodreads library export (CSV file)
- `--output`: Where to save the results 
- `--threshold`: Match confidence threshold (0-100)
  - Higher values (95-100): Fewer false positives but might miss some matches
  - Lower values (80-90): More matches but may include some incorrect ones
  - Recommended: 85-95

## Example Output

The output file will contain matched books in the format:
```
BookOutlet: The Song of Achilles by Madeline Miller, Goodreads: The Song of Achilles, Match Score: 98%
BookOutlet: Project Hail Mary by Andy Weir, Goodreads: Project Hail Mary, Match Score: 100%
```

## How It Works

The matching algorithm:
1. Preprocesses titles by removing common variations (editions, series indicators)
2. Separates titles and subtitles
3. Generates multiple variations for each title
4. Uses a weighted combination of four different fuzzy matching algorithms:
   - Exact character matching (15%)
   - Partial string matching (20%) 
   - Token sort ratio (25%)
   - Token set ratio (40%)
5. Applies special handling for very long titles and short titles
6. Uses different weighting for different title types

## Troubleshooting

If you're getting too many false matches:
- Increase the threshold value (try 95 or higher)

If it's missing books you know exist on BookOutlet:
- Lower the threshold value (try 80-85)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) for fuzzy string matching
- [CloudScraper](https://github.com/VeNoMouS/cloudscraper) for web scraping with bot protection bypass
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
