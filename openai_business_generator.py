#!/usr/bin/env python3
"""
Seattle Business Generator using OpenAI API
Generates realistic business data for Seattle area
"""

import os
import json
import csv
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seattle_business_generator.log'),
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

class OpenAIBusinessGenerator:
    """Generate realistic Seattle business data using OpenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.businesses: List[Business] = []
        
        # Business categories to generate
        self.categories = {
            'Food': ['restaurant', 'cafe', 'bakery', 'bar', 'fast_food'],
            'Salon': ['hair_care', 'beauty_salon', 'barber_shop'],
            'Beauty': ['beauty_salon', 'spa', 'nail_salon', 'massage_therapist'],
            'Healthcare': ['doctor', 'dentist', 'pharmacy', 'veterinary_care'],
            'Retail': ['clothing_store', 'shoe_store', 'electronics_store', 'book_store'],
            'Services': ['lawyer', 'accountant', 'real_estate_agency', 'car_repair'],
            'Entertainment': ['gym', 'movie_theater', 'bowling_alley'],
            'Education': ['school', 'library', 'tutoring_center']
        }
    
    def generate_businesses_for_category(self, category: str, subcategories: List[str], count: int = 10) -> List[Dict]:
        """Generate businesses for a specific category using OpenAI"""
        
        prompt = f"""Generate {count} realistic businesses in Seattle for the category "{category}".
        
For each business, provide:
- name: Creative, realistic business name
- subcategory: One of {subcategories}
- email: Realistic email address
- phone: Seattle area phone number (206 area code)
- address: Real Seattle street address
- rating: Rating between 3.5 and 5.0
- website: Realistic website URL

Format as JSON array with this structure:
[
  {{
    "name": "Business Name",
    "subcategory": "subcategory",
    "email": "email@business.com",
    "phone": "(206) 555-0123",
    "address": "123 Main St Seattle WA 98101",
    "rating": 4.2,
    "website": "https://www.business.com"
  }}
]

Make the businesses diverse and realistic for Seattle area."""

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 2000,
            'temperature': 0.8
        }
        
        try:
            logger.info(f"Generating {count} businesses for {category}")
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            businesses_data = json.loads(content)
            
            logger.info(f"Generated {len(businesses_data)} businesses for {category}")
            return businesses_data
            
        except requests.RequestException as e:
            logger.error(f"API request failed for {category}: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for {category}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error for {category}: {e}")
            return []
    
    def generate_all_businesses(self, businesses_per_category: int = 15) -> None:
        """Generate businesses for all categories"""
        logger.info("Starting Seattle business generation with OpenAI...")
        start_time = datetime.now()
        
        for category, subcategories in self.categories.items():
            logger.info(f"Processing category: {category}")
            
            # Generate businesses for this category
            businesses_data = self.generate_businesses_for_category(
                category, subcategories, businesses_per_category
            )
            
            # Convert to Business objects
            for business_data in businesses_data:
                try:
                    business = Business(
                        name=business_data.get('name', 'Unknown Business'),
                        category=category,
                        subcategory=business_data.get('subcategory', subcategories[0]),
                        email=business_data.get('email'),
                        phone=business_data.get('phone'),
                        address=business_data.get('address'),
                        rating=business_data.get('rating'),
                        website=business_data.get('website')
                    )
                    self.businesses.append(business)
                    logger.info(f"Added: {business.name}")
                    
                except Exception as e:
                    logger.error(f"Error processing business data: {e}")
            
            # Rate limiting - be respectful to OpenAI API
            time.sleep(2)
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Generation completed in {duration}. Created {len(self.businesses)} businesses.")
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export business data to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_openai_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'category', 'subcategory', 'email', 'phone', 'address', 'rating', 'website']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for business in self.businesses:
                writer.writerow(asdict(business))
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    def export_to_json(self, filename: str = None) -> str:
        """Export business data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_openai_{timestamp}.json"
        
        data = {
            'metadata': {
                'total_businesses': len(self.businesses),
                'generation_date': datetime.now().isoformat(),
                'categories': list(self.categories.keys()),
                'data_source': 'OpenAI Generated'
            },
            'businesses': [asdict(business) for business in self.businesses]
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    def get_statistics(self) -> Dict:
        """Get statistics about generated businesses"""
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
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("Please set OPENAI_API_KEY environment variable")
        print("\nTo get an OpenAI API key:")
        print("1. Go to https://platform.openai.com/api-keys")
        print("2. Sign up or log in to your OpenAI account")
        print("3. Create a new API key")
        print("4. Set the environment variable: export OPENAI_API_KEY='your_key_here'")
        return
    
    # Initialize generator
    generator = OpenAIBusinessGenerator(api_key)
    
    try:
        # Generate businesses (15 per category = ~120 total businesses)
        generator.generate_all_businesses(businesses_per_category=15)
        
        # Export data
        csv_file = generator.export_to_csv()
        json_file = generator.export_to_json()
        
        # Show statistics
        stats = generator.get_statistics()
        print("\n" + "="*50)
        print("BUSINESS GENERATION STATISTICS")
        print("="*50)
        print(f"Total businesses generated: {stats['total_businesses']}")
        print(f"Businesses with email: {stats['businesses_with_email']}")
        print(f"Businesses with phone: {stats['businesses_with_phone']}")
        print(f"Businesses with website: {stats['businesses_with_website']}")
        print("\nBusinesses by category:")
        for category, count in stats['businesses_by_category'].items():
            print(f"  {category}: {count}")
        
        print(f"\nData exported to:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        
        # Show sample businesses
        if generator.businesses:
            print(f"\n🏪 Sample businesses generated:")
            for i, business in enumerate(generator.businesses[:5]):
                print(f"\n{i+1}. {business.name}")
                print(f"   Category: {business.category} - {business.subcategory}")
                print(f"   Phone: {business.phone}")
                print(f"   Email: {business.email}")
                print(f"   Address: {business.address}")
                print(f"   Website: {business.website}")
                print(f"   Rating: {business.rating}")
        
    except KeyboardInterrupt:
        logger.info("Generation interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 