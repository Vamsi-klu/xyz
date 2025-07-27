#!/usr/bin/env python3
"""
Seattle Business Scraper
A robust pipeline to fetch local business details in Seattle city

Features:
- Fetches business name, category, email, phone, address
- Categorizes businesses (Food, Salon, Beauty, etc.)
- Exports data to CSV and JSON formats
- Rate limiting and error handling
- Progress tracking and logging

Author: Business Data Pipeline
"""

import requests
import json
import csv
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os
from urllib.parse import quote_plus
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seattle_business_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Business:
    """Data class to represent a business"""
    name: str
    category: str
    subcategory: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    website: Optional[str] = None
    place_id: Optional[str] = None

class SeattleBusinessScraper:
    """Main scraper class for Seattle businesses"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.businesses: List[Business] = []
        
        # Business categories to search for
        self.categories = {
            'Food': [
                'restaurant', 'cafe', 'bakery', 'bar', 'fast_food',
                'meal_takeaway', 'meal_delivery', 'food_truck'
            ],
            'Salon': [
                'hair_care', 'beauty_salon', 'barber_shop'
            ],
            'Beauty': [
                'beauty_salon', 'spa', 'nail_salon', 'cosmetics_store',
                'massage_therapist', 'eyebrow_threading'
            ],
            'Healthcare': [
                'doctor', 'dentist', 'pharmacy', 'hospital', 'veterinary_care',
                'physiotherapist', 'chiropractor'
            ],
            'Retail': [
                'clothing_store', 'shoe_store', 'jewelry_store', 'electronics_store',
                'book_store', 'furniture_store', 'home_goods_store'
            ],
            'Services': [
                'lawyer', 'accountant', 'real_estate_agency', 'insurance_agency',
                'bank', 'atm', 'car_repair', 'locksmith', 'plumber', 'electrician'
            ],
            'Entertainment': [
                'movie_theater', 'bowling_alley', 'gym', 'amusement_park',
                'night_club', 'casino'
            ],
            'Education': [
                'school', 'university', 'library', 'driving_school'
            ]
        }
        
        # Seattle coordinates and radius
        self.seattle_coords = "47.6062,-122.3321"
        self.radius = 25000  # 25km radius to cover Seattle metro area
        
    def search_businesses_by_category(self, category: str, subcategories: List[str]) -> List[Dict]:
        """Search for businesses in a specific category"""
        all_results = []
        
        for subcategory in subcategories:
            logger.info(f"Searching for {subcategory} businesses in {category}")
            
            url = f"{self.base_url}/nearbysearch/json"
            params = {
                'location': self.seattle_coords,
                'radius': self.radius,
                'type': subcategory,
                'key': self.api_key
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'OK':
                    results = data.get('results', [])
                    all_results.extend(results)
                    logger.info(f"Found {len(results)} {subcategory} businesses")
                    
                    # Handle pagination
                    while 'next_page_token' in data:
                        time.sleep(2)  # Required delay for next_page_token
                        next_params = {
                            'pagetoken': data['next_page_token'],
                            'key': self.api_key
                        }
                        response = requests.get(url, params=next_params)
                        response.raise_for_status()
                        data = response.json()
                        
                        if data.get('status') == 'OK':
                            results = data.get('results', [])
                            all_results.extend(results)
                            logger.info(f"Found {len(results)} more {subcategory} businesses")
                        else:
                            break
                            
                else:
                    logger.warning(f"API returned status: {data.get('status')} for {subcategory}")
                    
            except requests.RequestException as e:
                logger.error(f"Error searching for {subcategory}: {e}")
                
            # Rate limiting
            time.sleep(1)
            
        return all_results
    
    def get_business_details(self, place_id: str) -> Dict:
        """Get detailed information for a specific business"""
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,formatted_address,website,rating,types',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            else:
                logger.warning(f"Failed to get details for place_id {place_id}: {data.get('status')}")
                return {}
                
        except requests.RequestException as e:
            logger.error(f"Error getting details for place_id {place_id}: {e}")
            return {}
    
    def extract_email_from_website(self, website: str) -> Optional[str]:
        """Try to extract email from business website (basic implementation)"""
        if not website:
            return None
            
        try:
            # This is a basic implementation - in production, you'd want more sophisticated scraping
            response = requests.get(website, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            content = response.text
            
            # Simple regex to find email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, content)
            
            if emails:
                # Return the first email found
                return emails[0]
                
        except Exception as e:
            logger.debug(f"Could not extract email from {website}: {e}")
            
        return None
    
    def process_business_data(self, raw_data: List[Dict], category: str, subcategory: str) -> None:
        """Process raw business data and create Business objects"""
        for item in raw_data:
            place_id = item.get('place_id')
            if not place_id:
                continue
                
            # Get detailed information
            details = self.get_business_details(place_id)
            if not details:
                continue
                
            # Extract email from website if available
            website = details.get('website')
            email = self.extract_email_from_website(website) if website else None
            
            business = Business(
                name=details.get('name', 'N/A'),
                category=category,
                subcategory=subcategory,
                email=email,
                phone=details.get('formatted_phone_number'),
                address=details.get('formatted_address'),
                rating=details.get('rating'),
                website=website,
                place_id=place_id
            )
            
            self.businesses.append(business)
            logger.info(f"Processed: {business.name}")
            
            # Rate limiting
            time.sleep(0.5)
    
    def scrape_all_businesses(self) -> None:
        """Main method to scrape all business categories"""
        logger.info("Starting Seattle business scraping...")
        start_time = datetime.now()
        
        for category, subcategories in self.categories.items():
            logger.info(f"Processing category: {category}")
            
            # Search for businesses in this category
            raw_results = self.search_businesses_by_category(category, subcategories)
            
            # Remove duplicates based on place_id
            unique_results = {}
            for result in raw_results:
                place_id = result.get('place_id')
                if place_id and place_id not in unique_results:
                    unique_results[place_id] = result
            
            logger.info(f"Found {len(unique_results)} unique businesses in {category}")
            
            # Process each unique business
            for subcategory in subcategories:
                relevant_businesses = [
                    business for business in unique_results.values()
                    if subcategory in business.get('types', [])
                ]
                
                if relevant_businesses:
                    self.process_business_data(relevant_businesses, category, subcategory)
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Scraping completed in {duration}. Found {len(self.businesses)} businesses.")
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export business data to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'category', 'subcategory', 'email', 'phone', 'address', 'rating', 'website']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for business in self.businesses:
                row = asdict(business)
                # Remove place_id from CSV export
                row.pop('place_id', None)
                writer.writerow(row)
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    def export_to_json(self, filename: str = None) -> str:
        """Export business data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_{timestamp}.json"
        
        data = {
            'metadata': {
                'total_businesses': len(self.businesses),
                'export_date': datetime.now().isoformat(),
                'categories': list(self.categories.keys())
            },
            'businesses': [asdict(business) for business in self.businesses]
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    def get_statistics(self) -> Dict:
        """Get statistics about scraped businesses"""
        stats = {
            'total_businesses': len(self.businesses),
            'businesses_by_category': {},
            'businesses_with_email': len([b for b in self.businesses if b.email]),
            'businesses_with_phone': len([b for b in self.businesses if b.phone]),
            'businesses_with_website': len([b for b in self.businesses if b.website]),
        }
        
        for business in self.businesses:
            category = business.category
            if category not in stats['businesses_by_category']:
                stats['businesses_by_category'][category] = 0
            stats['businesses_by_category'][category] += 1
        
        return stats

def main():
    """Main execution function"""
    # Check for API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logger.error("Please set GOOGLE_PLACES_API_KEY environment variable")
        print("\nTo get a Google Places API key:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable the Places API")
        print("4. Create credentials (API key)")
        print("5. Set the environment variable: export GOOGLE_PLACES_API_KEY='your_key_here'")
        return
    
    # Initialize scraper
    scraper = SeattleBusinessScraper(api_key)
    
    try:
        # Scrape all businesses
        scraper.scrape_all_businesses()
        
        # Export data
        csv_file = scraper.export_to_csv()
        json_file = scraper.export_to_json()
        
        # Show statistics
        stats = scraper.get_statistics()
        print("\n" + "="*50)
        print("SCRAPING STATISTICS")
        print("="*50)
        print(f"Total businesses found: {stats['total_businesses']}")
        print(f"Businesses with email: {stats['businesses_with_email']}")
        print(f"Businesses with phone: {stats['businesses_with_phone']}")
        print(f"Businesses with website: {stats['businesses_with_website']}")
        print("\nBusinesses by category:")
        for category, count in stats['businesses_by_category'].items():
            print(f"  {category}: {count}")
        
        print(f"\nData exported to:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 