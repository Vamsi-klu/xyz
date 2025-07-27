# Seattle Business Scraper - Setup Instructions

## Overview
This script scrapes local business information from Seattle using the Google Places API. It fetches business names, categories, email addresses, phone numbers, and addresses, organizing them by business type (Food, Salon, Beauty, etc.).

## Prerequisites

### 1. Python Requirements
- Python 3.7 or higher
- Required packages (install via pip):

```bash
pip install requests
```

### 2. Google Places API Key
You need a Google Places API key to use this scraper.

#### Steps to get API key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Places API
   - Places API (New)
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key
6. (Optional but recommended) Restrict the key to only Places API

#### API Costs:
- Places Nearby Search: $32 per 1000 requests
- Place Details: $17 per 1000 requests
- Estimated cost for full Seattle scrape: $50-$100 depending on number of businesses

## Installation

### Step 1: Download the files
Save these files to your project directory:
- `seattle_business_scraper.py` (main script)
- `config.py` (configuration file)

### Step 2: Set up environment variable
Set your Google Places API key as an environment variable:

#### On macOS/Linux:
```bash
export GOOGLE_PLACES_API_KEY="AIzaSyAXcMk591rNptrC-IL8PjIMOmvsdm1w9dU"
```

#### On Windows:
```cmd
set GOOGLE_PLACES_API_KEY=your_api_key_here
```

#### Or create a .env file:
Create a `.env` file in your project directory:
```
GOOGLE_PLACES_API_KEY=your_api_key_here
```

### Step 3: Install dependencies
```bash
pip install requests
```

## Usage

### Basic Usage
Run the script to scrape all business categories:
```bash
python seattle_business_scraper.py
```

### Advanced Usage
You can modify the `config.py` file to:
- Change search radius
- Add/remove business categories
- Adjust rate limiting
- Modify export formats

### Customizing Categories
Edit the `BUSINESS_CATEGORIES` in `config.py` to focus on specific business types:

```python
BUSINESS_CATEGORIES = {
    'Food': ['restaurant', 'cafe', 'bakery'],
    'Salon': ['hair_care', 'beauty_salon'],
    'Beauty': ['spa', 'nail_salon']
}
```

## Output

The script generates two files:
1. **CSV file**: `seattle_businesses_YYYYMMDD_HHMMSS.csv`
   - Easy to open in Excel/Google Sheets
   - Contains: name, category, subcategory, email, phone, address, rating, website

2. **JSON file**: `seattle_businesses_YYYYMMDD_HHMMSS.json`
   - Machine-readable format
   - Includes metadata and full business details

## Features

### Data Collected
- ✅ Business name
- ✅ Business category (Food, Salon, Beauty, etc.)
- ✅ Subcategory (restaurant, cafe, spa, etc.)
- ✅ Phone number
- ✅ Address
- ✅ Website
- ✅ Rating
- ⚠️ Email address (extracted from websites when available)

### Built-in Features
- **Rate limiting**: Respects Google API limits
- **Error handling**: Continues scraping even if some requests fail
- **Progress logging**: Shows real-time progress
- **Duplicate removal**: Eliminates duplicate businesses
- **Statistics**: Shows summary of scraped data
- **Resume capability**: Can be stopped and restarted

## Troubleshooting

### Common Issues

#### "API key not set" error
Make sure you've set the environment variable correctly:
```bash
echo $GOOGLE_PLACES_API_KEY  # Should show your key
```

#### "API quota exceeded" error
- You've hit your daily API limit
- Wait 24 hours or increase your quota in Google Cloud Console

#### "REQUEST_DENIED" error
- Your API key might not have Places API enabled
- Check that Places API is enabled in Google Cloud Console

#### Slow performance
- This is normal - the script respects API rate limits
- Full Seattle scrape can take 2-4 hours
- You can reduce the search radius in `config.py` for faster results

#### Few email addresses found
- Email extraction depends on business websites
- Many businesses don't publish emails publicly
- Consider supplementing with manual research

## Customization Options

### Search Area
Change the coordinates and radius in `config.py`:
```python
SEATTLE_COORDS = "47.6062,-122.3321"  # Downtown Seattle
SEARCH_RADIUS = 25000  # 25km radius
```

### Rate Limiting
Adjust delays between requests:
```python
REQUEST_DELAY = 1.0  # Seconds between API calls
DETAILS_REQUEST_DELAY = 0.5  # Seconds between detail requests
```

### Business Types
Add custom business types to search for:
```python
BUSINESS_CATEGORIES = {
    'Your_Category': ['google_place_type1', 'google_place_type2']
}
```

## Legal and Ethical Considerations

1. **Google Terms of Service**: Ensure compliance with Google Places API terms
2. **Rate Limits**: Don't exceed API quotas
3. **Data Usage**: Use scraped data responsibly and in compliance with privacy laws
4. **Website Scraping**: Email extraction from websites should respect robots.txt

## Support

For issues or questions:
1. Check the log file: `seattle_business_scraper.log`
2. Review Google Places API documentation
3. Verify your API key permissions

## Example Output

After running, you'll see statistics like:
```
SCRAPING STATISTICS
==================================================
Total businesses found: 1,247
Businesses with email: 342
Businesses with phone: 1,198
Businesses with website: 891

Businesses by category:
  Food: 456
  Retail: 234
  Services: 198
  Beauty: 123
  Salon: 87
  Healthcare: 149
``` 

# API Keys
GOOGLE_PLACES_API_KEY='AIzaSyAXcMk591rNptrC-IL8PjIMOmvsdm1w9dU'

# Search Parameters
SEARCH_RADIUS=25000
SEATTLE_COORDS=47.6062,-122.3321

# Rate Limiting (in seconds)
REQUEST_DELAY=1.0
PAGINATION_DELAY=2.0

# Export Settings
EXPORT_FORMAT=csv,json
LOG_LEVEL=INFO
LOG_FILE=seattle_business_scraper.log

# Timeout Settings (in seconds)
API_TIMEOUT=30
WEBSITE_TIMEOUT=10 