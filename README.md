# Seattle Business Scraper

A comprehensive Python-based data pipeline for scraping and generating Seattle local business information. This project provides multiple approaches to collect business data including names, categories, contact information, addresses, and ratings.

## 📊 Dataset Overview

**Total Businesses Generated: 509+**
- **250 businesses** (Large dataset)
- **240 businesses** (Multiple smaller datasets)
- **19 businesses** (Hand-crafted samples)

## 🏢 Business Categories

- **Food** (75+ businesses): restaurants, cafes, bars, bakeries, fast food, pizza, Asian, Mexican
- **Salon** (50+ businesses): hair care, beauty salons, barbershops, nail salons
- **Beauty** (50+ businesses): spas, nail salons, massage therapy, skincare, aesthetics
- **Healthcare** (50+ businesses): doctors, dentists, pharmacies, veterinary care, urgent care
- **Retail** (50+ businesses): clothing, shoes, electronics, books, jewelry, furniture
- **Services** (50+ businesses): lawyers, accountants, real estate, car repair, plumbing
- **Entertainment** (50+ businesses): gyms, theaters, bowling, yoga studios, dance studios
- **Education** (50+ businesses): schools, libraries, tutoring, music lessons, art classes
- **Automotive** (25 businesses): car dealers, auto repair, car wash, gas stations
- **Professional** (25 businesses): marketing, consulting, photography, graphic design

## 📋 Data Fields

Each business record contains:
- ✅ **Business name** (realistic Seattle-style names)
- ✅ **Category & subcategory** (properly organized)
- ✅ **Email address** (realistic business emails)
- ✅ **Phone number** (Seattle area codes: 206, 425, 253)
- ✅ **Address** (real Seattle streets and zip codes)
- ✅ **Rating** (3.2-5.0 stars)
- ✅ **Website** (realistic business websites)

## 🚀 Scripts Included

### 1. Google Places API Scraper
- `seattle_business_scraper.py` - Main scraper using Google Places API
- `demo_script.py` - Demo version with limited scope
- `test_api_key.py` - API key testing utility
- `config.py` - Configuration settings

### 2. Offline Generators
- `offline_business_generator.py` - Generates 120 businesses without API
- `large_business_generator.py` - Generates 250 businesses with expanded categories

### 3. OpenAI Integration
- `openai_business_generator.py` - Uses OpenAI API for realistic data generation

## 📁 Generated Files

### CSV Files
- `seattle_businesses_large_20250726_185021.csv` - **250 businesses** (Main dataset)
- `seattle_businesses_offline_20250726_184829.csv` - 120 businesses
- `seattle_businesses_offline_20250726_184908.csv` - 120 businesses
- `sample_seattle_businesses.csv` - 19 hand-crafted samples

### JSON Files
- Corresponding JSON files with metadata for each CSV

## 🛠️ Setup Instructions

### Prerequisites
```bash
pip install requests
```

### For Google Places API (Real Data)
1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Places API (New)
3. Set environment variable:
```bash
export GOOGLE_PLACES_API_KEY="your_key_here"
```

### For OpenAI Integration
```bash
export OPENAI_API_KEY="your_openai_key_here"
```

## 📊 Usage Examples

### Generate Large Dataset (Offline)
```bash
python large_business_generator.py
```

### Generate Standard Dataset (Offline)
```bash
python offline_business_generator.py
```

### Test Google Places API
```bash
python test_api_key.py
```

### Run Demo with Google Places API
```bash
python demo_script.py
```

## 📈 Sample Data

```csv
name,category,subcategory,email,phone,address,rating,website
Pike Place Chowder,Food,restaurant,info@pikeplacebowder.com,(206) 267-2537,"1530 Post Alley Seattle WA 98101",4.5,https://www.pikeplacebowder.com
Gene Juarez Salon & Spa,Salon,beauty_salon,info@genejuarez.com,(206) 326-6000,"607 Pine St Seattle WA 98101",4.1,https://www.genejuarez.com
```

## 🔧 Features

- **Multiple Data Sources**: Google Places API, OpenAI, Offline generation
- **Rate Limiting**: Respects API limits
- **Error Handling**: Robust error management
- **Data Validation**: Ensures data quality
- **Export Options**: CSV and JSON formats
- **Statistics**: Comprehensive data analysis
- **Logging**: Detailed operation logs

## 📊 Statistics

- **Total Records**: 509+ businesses
- **Data Completeness**: 100% for offline generated data
- **Geographic Coverage**: Seattle metro area (25km radius)
- **Category Diversity**: 10 major business categories
- **Contact Information**: Phone numbers, emails, websites, addresses

## 🚨 Important Notes

- **Google Places API**: Requires valid API key and billing setup
- **Rate Limits**: Built-in delays to respect API quotas
- **Data Privacy**: Use scraped data responsibly
- **Cost Estimation**: Google Places API usage can cost $50-100 for full scrape

## 📝 License

This project is for educational and research purposes. Please comply with all applicable terms of service when using external APIs.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Generated on**: July 26, 2025  
**Last Updated**: July 26, 2025  
**Version**: 1.0 