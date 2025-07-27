#!/usr/bin/env python3
"""
Offline Seattle Business Generator
Generates realistic business data for Seattle area without requiring API keys
"""

import csv
import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

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

class OfflineBusinessGenerator:
    """Generate realistic Seattle business data offline"""
    
    def __init__(self):
        self.businesses: List[Business] = []
        
        # Seattle street names and neighborhoods
        self.seattle_streets = [
            "Pine St", "Pike St", "1st Ave", "2nd Ave", "3rd Ave", "4th Ave", "5th Ave",
            "Madison St", "Spring St", "Seneca St", "University St", "Union St",
            "Capitol Hill", "Fremont Ave N", "Ballard Ave NW", "Queen Anne Ave N",
            "Broadway", "15th Ave E", "23rd Ave", "Rainier Ave S", "California Ave SW",
            "Westlake Ave N", "Dexter Ave N", "Aurora Ave N", "Stone Way N"
        ]
        
        self.seattle_zip_codes = ["98101", "98102", "98103", "98104", "98105", "98106", 
                                 "98107", "98108", "98109", "98112", "98115", "98116", 
                                 "98117", "98118", "98119", "98121", "98122", "98125"]
        
        # Business name components
        self.business_prefixes = {
            'Food': ["Seattle", "Pike Place", "Capitol Hill", "Fremont", "Ballard", "Queen Anne", 
                    "The", "Emerald City", "Pacific", "Northwest", "Urban", "Artisan"],
            'Salon': ["Elite", "Luxe", "Chic", "Modern", "Classic", "Urban", "Bella", 
                     "Studio", "The", "Seattle", "Emerald"],
            'Beauty': ["Serenity", "Bliss", "Harmony", "Zen", "Pure", "Radiance", 
                      "Tranquil", "Divine", "Luxe", "Spa"],
            'Healthcare': ["Seattle", "Northwest", "Family", "Care", "Medical", "Health", 
                          "Wellness", "Prime", "Advanced"],
            'Retail': ["Seattle", "Urban", "Modern", "Classic", "Boutique", "The", 
                      "Pacific", "Northwest", "Emerald"],
            'Services': ["Seattle", "Professional", "Premier", "Elite", "Northwest", 
                        "Expert", "Reliable", "Quality"],
            'Entertainment': ["Seattle", "Urban", "Elite", "Prime", "Northwest", "Active", 
                             "Fitness", "Peak"],
            'Education': ["Seattle", "Learning", "Academic", "Knowledge", "Bright", 
                         "Future", "Excellence"]
        }
        
        self.business_suffixes = {
            'Food': ["Bistro", "Cafe", "Kitchen", "Grill", "House", "Restaurant", "Eatery", 
                    "Bar", "Tavern", "Bakery", "Deli"],
            'Salon': ["Salon", "Hair Studio", "Barbershop", "Hair Lounge", "Styling", 
                     "Hair Care", "Beauty Bar"],
            'Beauty': ["Spa", "Day Spa", "Wellness Center", "Beauty Studio", "Nail Salon", 
                      "Massage Therapy", "Aesthetics"],
            'Healthcare': ["Medical Center", "Clinic", "Family Practice", "Dental Care", 
                          "Pharmacy", "Veterinary Clinic", "Health Center"],
            'Retail': ["Boutique", "Store", "Shop", "Emporium", "Gallery", "Market", 
                      "Electronics", "Books"],
            'Services': ["Law Firm", "Accounting", "Real Estate", "Auto Repair", 
                        "Consulting", "Agency"],
            'Entertainment': ["Fitness", "Gym", "Theater", "Entertainment", "Sports Club", 
                             "Recreation"],
            'Education': ["Academy", "Learning Center", "School", "Institute", "Library", 
                         "Education Center"]
        }
    
    def generate_business_name(self, category: str) -> str:
        """Generate a realistic business name"""
        prefix = random.choice(self.business_prefixes.get(category, ["Seattle"]))
        suffix = random.choice(self.business_suffixes.get(category, ["Business"]))
        
        # Sometimes add a middle word
        if random.random() < 0.3:
            middle_words = ["& Co", "Group", "Center", "Studio", "House", "Place"]
            middle = random.choice(middle_words)
            return f"{prefix} {middle} {suffix}"
        
        return f"{prefix} {suffix}"
    
    def generate_phone_number(self) -> str:
        """Generate a Seattle area phone number"""
        return f"(206) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
    
    def generate_email(self, business_name: str) -> str:
        """Generate a realistic email address"""
        # Clean business name for email
        clean_name = business_name.lower().replace(" ", "").replace("&", "and")
        clean_name = ''.join(c for c in clean_name if c.isalnum())[:15]
        
        domains = ["gmail.com", "yahoo.com", "outlook.com", "business.com", 
                  f"{clean_name}.com", f"{clean_name}seattle.com"]
        
        prefixes = ["info", "contact", "hello", "admin", clean_name[:10]]
        
        prefix = random.choice(prefixes)
        domain = random.choice(domains)
        
        return f"{prefix}@{domain}"
    
    def generate_address(self) -> str:
        """Generate a realistic Seattle address"""
        number = random.randint(100, 9999)
        street = random.choice(self.seattle_streets)
        zip_code = random.choice(self.seattle_zip_codes)
        
        return f"{number} {street}, Seattle WA {zip_code}"
    
    def generate_website(self, business_name: str) -> str:
        """Generate a realistic website URL"""
        clean_name = business_name.lower().replace(" ", "").replace("&", "and")
        clean_name = ''.join(c for c in clean_name if c.isalnum())[:20]
        
        extensions = [".com", ".net", ".biz", "seattle.com"]
        extension = random.choice(extensions)
        
        return f"https://www.{clean_name}{extension}"
    
    def generate_rating(self) -> float:
        """Generate a realistic business rating"""
        return round(random.uniform(3.5, 5.0), 1)
    
    def generate_businesses_for_category(self, category: str, subcategories: List[str], 
                                       count: int = 15) -> None:
        """Generate businesses for a specific category"""
        print(f"Generating {count} businesses for {category}...")
        
        for _ in range(count):
            name = self.generate_business_name(category)
            subcategory = random.choice(subcategories)
            
            business = Business(
                name=name,
                category=category,
                subcategory=subcategory,
                email=self.generate_email(name),
                phone=self.generate_phone_number(),
                address=self.generate_address(),
                rating=self.generate_rating(),
                website=self.generate_website(name)
            )
            
            self.businesses.append(business)
    
    def generate_all_businesses(self) -> None:
        """Generate businesses for all categories"""
        categories = {
            'Food': ['restaurant', 'cafe', 'bakery', 'bar', 'fast_food'],
            'Salon': ['hair_care', 'beauty_salon', 'barber_shop'],
            'Beauty': ['beauty_salon', 'spa', 'nail_salon', 'massage_therapist'],
            'Healthcare': ['doctor', 'dentist', 'pharmacy', 'veterinary_care'],
            'Retail': ['clothing_store', 'shoe_store', 'electronics_store', 'book_store'],
            'Services': ['lawyer', 'accountant', 'real_estate_agency', 'car_repair'],
            'Entertainment': ['gym', 'movie_theater', 'bowling_alley'],
            'Education': ['school', 'library', 'tutoring_center']
        }
        
        print("🚀 Starting Seattle Business Generation (Offline Mode)")
        print("=" * 60)
        
        for category, subcategories in categories.items():
            self.generate_businesses_for_category(category, subcategories, 15)
        
        print(f"\n✅ Generated {len(self.businesses)} total businesses!")
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export business data to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_offline_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'category', 'subcategory', 'email', 'phone', 'address', 'rating', 'website']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for business in self.businesses:
                writer.writerow(asdict(business))
        
        print(f"📄 Data exported to {filename}")
        return filename
    
    def export_to_json(self, filename: str = None) -> str:
        """Export business data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_offline_{timestamp}.json"
        
        data = {
            'metadata': {
                'total_businesses': len(self.businesses),
                'generation_date': datetime.now().isoformat(),
                'data_source': 'Offline Generated',
                'location': 'Seattle, WA'
            },
            'businesses': [asdict(business) for business in self.businesses]
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"📄 Data exported to {filename}")
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
    generator = OfflineBusinessGenerator()
    
    # Generate all businesses
    generator.generate_all_businesses()
    
    # Export data
    csv_file = generator.export_to_csv()
    json_file = generator.export_to_json()
    
    # Show statistics
    stats = generator.get_statistics()
    print("\n" + "="*60)
    print("📊 BUSINESS GENERATION STATISTICS")
    print("="*60)
    print(f"Total businesses generated: {stats['total_businesses']}")
    print(f"Businesses with email: {stats['businesses_with_email']}")
    print(f"Businesses with phone: {stats['businesses_with_phone']}")
    print(f"Businesses with website: {stats['businesses_with_website']}")
    print("\nBusinesses by category:")
    for category, count in stats['businesses_by_category'].items():
        print(f"  {category}: {count}")
    
    print(f"\n📁 Files created:")
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

if __name__ == "__main__":
    main() 