#!/usr/bin/env python3
"""
Large Seattle Business Generator
Generates a large dataset of realistic business data for Seattle area
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

class LargeBusinessGenerator:
    """Generate large dataset of realistic Seattle business data"""
    
    def __init__(self):
        self.businesses: List[Business] = []
        
        # Expanded Seattle street names and neighborhoods
        self.seattle_streets = [
            "Pine St", "Pike St", "1st Ave", "2nd Ave", "3rd Ave", "4th Ave", "5th Ave", "6th Ave",
            "Madison St", "Spring St", "Seneca St", "University St", "Union St", "Stewart St",
            "Capitol Hill", "Fremont Ave N", "Ballard Ave NW", "Queen Anne Ave N", "Magnolia Blvd W",
            "Broadway", "15th Ave E", "23rd Ave", "Rainier Ave S", "California Ave SW", "Alki Ave SW",
            "Westlake Ave N", "Dexter Ave N", "Aurora Ave N", "Stone Way N", "Greenwood Ave N",
            "Roosevelt Way NE", "Sand Point Way NE", "Lake City Way NE", "Bothell Way NE",
            "Martin Luther King Jr Way S", "Beacon Ave S", "Georgetown", "Industrial Way S",
            "West Seattle Bridge", "Highland Park Way SW", "Delridge Way SW", "35th Ave SW"
        ]
        
        self.seattle_zip_codes = ["98101", "98102", "98103", "98104", "98105", "98106", 
                                 "98107", "98108", "98109", "98112", "98115", "98116", 
                                 "98117", "98118", "98119", "98121", "98122", "98125",
                                 "98126", "98133", "98136", "98144", "98146", "98154"]
        
        # Expanded business name components
        self.business_prefixes = {
            'Food': ["Seattle", "Pike Place", "Capitol Hill", "Fremont", "Ballard", "Queen Anne", 
                    "The", "Emerald City", "Pacific", "Northwest", "Urban", "Artisan", "Gourmet",
                    "Fresh", "Local", "Farm", "Organic", "Craft", "Rustic", "Modern", "Classic"],
            'Salon': ["Elite", "Luxe", "Chic", "Modern", "Classic", "Urban", "Bella", "Glamour",
                     "Studio", "The", "Seattle", "Emerald", "Platinum", "Gold", "Diamond", "Premier"],
            'Beauty': ["Serenity", "Bliss", "Harmony", "Zen", "Pure", "Radiance", "Tranquil", 
                      "Divine", "Luxe", "Spa", "Rejuvenate", "Refresh", "Glow", "Beauty", "Elegant"],
            'Healthcare': ["Seattle", "Northwest", "Family", "Care", "Medical", "Health", "Wellness", 
                          "Prime", "Advanced", "Complete", "Comprehensive", "Professional", "Expert"],
            'Retail': ["Seattle", "Urban", "Modern", "Classic", "Boutique", "The", "Pacific", 
                      "Northwest", "Emerald", "Trendy", "Chic", "Style", "Fashion", "Unique"],
            'Services': ["Seattle", "Professional", "Premier", "Elite", "Northwest", "Expert", 
                        "Reliable", "Quality", "Trusted", "Superior", "Excellence", "Prime"],
            'Entertainment': ["Seattle", "Urban", "Elite", "Prime", "Northwest", "Active", "Fitness", 
                             "Peak", "Ultimate", "Power", "Energy", "Dynamic", "Strong"],
            'Education': ["Seattle", "Learning", "Academic", "Knowledge", "Bright", "Future", 
                         "Excellence", "Success", "Achievement", "Discovery", "Wisdom"]
        }
        
        self.business_suffixes = {
            'Food': ["Bistro", "Cafe", "Kitchen", "Grill", "House", "Restaurant", "Eatery", "Bar", 
                    "Tavern", "Bakery", "Deli", "Pizzeria", "Steakhouse", "Brewery", "Lounge"],
            'Salon': ["Salon", "Hair Studio", "Barbershop", "Hair Lounge", "Styling", "Hair Care", 
                     "Beauty Bar", "Hair Gallery", "Style Studio", "Cut & Color"],
            'Beauty': ["Spa", "Day Spa", "Wellness Center", "Beauty Studio", "Nail Salon", 
                      "Massage Therapy", "Aesthetics", "Skincare", "Beauty Lounge", "Retreat"],
            'Healthcare': ["Medical Center", "Clinic", "Family Practice", "Dental Care", "Pharmacy", 
                          "Veterinary Clinic", "Health Center", "Medical Group", "Urgent Care"],
            'Retail': ["Boutique", "Store", "Shop", "Emporium", "Gallery", "Market", "Electronics", 
                      "Books", "Apparel", "Outlet", "Fashion", "Goods"],
            'Services': ["Law Firm", "Accounting", "Real Estate", "Auto Repair", "Consulting", 
                        "Agency", "Solutions", "Services", "Group", "Associates"],
            'Entertainment': ["Fitness", "Gym", "Theater", "Entertainment", "Sports Club", 
                             "Recreation", "Center", "Studio", "Arena", "Complex"],
            'Education': ["Academy", "Learning Center", "School", "Institute", "Library", 
                         "Education Center", "Training", "College", "University"]
        }
    
    def generate_business_name(self, category: str) -> str:
        """Generate a realistic business name"""
        prefix = random.choice(self.business_prefixes.get(category, ["Seattle"]))
        suffix = random.choice(self.business_suffixes.get(category, ["Business"]))
        
        # Sometimes add a middle word or number
        if random.random() < 0.4:
            middle_options = ["& Co", "Group", "Center", "Studio", "House", "Place", "Express", "Plus"]
            middle = random.choice(middle_options)
            return f"{prefix} {middle} {suffix}"
        elif random.random() < 0.1:
            number = random.randint(1, 99)
            return f"{prefix} {suffix} {number}"
        
        return f"{prefix} {suffix}"
    
    def generate_phone_number(self) -> str:
        """Generate a Seattle area phone number"""
        area_codes = ["206", "425", "253"]  # Seattle metro area codes
        area_code = random.choice(area_codes)
        return f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
    
    def generate_email(self, business_name: str) -> str:
        """Generate a realistic email address"""
        clean_name = business_name.lower().replace(" ", "").replace("&", "and").replace("+", "plus")
        clean_name = ''.join(c for c in clean_name if c.isalnum())[:15]
        
        domains = ["gmail.com", "yahoo.com", "outlook.com", "business.com", "hotmail.com",
                  f"{clean_name}.com", f"{clean_name}seattle.com", f"{clean_name}.net"]
        
        prefixes = ["info", "contact", "hello", "admin", "support", clean_name[:10], "office"]
        
        prefix = random.choice(prefixes)
        domain = random.choice(domains)
        
        return f"{prefix}@{domain}"
    
    def generate_address(self) -> str:
        """Generate a realistic Seattle address"""
        number = random.randint(100, 9999)
        street = random.choice(self.seattle_streets)
        zip_code = random.choice(self.seattle_zip_codes)
        
        # Sometimes add suite/unit numbers
        if random.random() < 0.3:
            suite = random.choice(["Suite", "Unit", "Ste", "#"])
            suite_num = random.randint(1, 500)
            return f"{number} {street} {suite} {suite_num}, Seattle WA {zip_code}"
        
        return f"{number} {street}, Seattle WA {zip_code}"
    
    def generate_website(self, business_name: str) -> str:
        """Generate a realistic website URL"""
        clean_name = business_name.lower().replace(" ", "").replace("&", "and").replace("+", "plus")
        clean_name = ''.join(c for c in clean_name if c.isalnum())[:25]
        
        extensions = [".com", ".net", ".biz", ".org", "seattle.com"]
        extension = random.choice(extensions)
        
        return f"https://www.{clean_name}{extension}"
    
    def generate_rating(self) -> float:
        """Generate a realistic business rating"""
        return round(random.uniform(3.2, 5.0), 1)
    
    def generate_businesses_for_category(self, category: str, subcategories: List[str], 
                                       count: int = 25) -> None:
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
            'Food': ['restaurant', 'cafe', 'bakery', 'bar', 'fast_food', 'pizza', 'asian', 'mexican'],
            'Salon': ['hair_care', 'beauty_salon', 'barber_shop', 'nail_salon'],
            'Beauty': ['beauty_salon', 'spa', 'nail_salon', 'massage_therapist', 'skincare', 'aesthetics'],
            'Healthcare': ['doctor', 'dentist', 'pharmacy', 'veterinary_care', 'urgent_care', 'clinic'],
            'Retail': ['clothing_store', 'shoe_store', 'electronics_store', 'book_store', 'jewelry', 'furniture'],
            'Services': ['lawyer', 'accountant', 'real_estate_agency', 'car_repair', 'plumbing', 'electrical'],
            'Entertainment': ['gym', 'movie_theater', 'bowling_alley', 'yoga_studio', 'dance_studio'],
            'Education': ['school', 'library', 'tutoring_center', 'music_lessons', 'art_classes'],
            'Automotive': ['car_dealer', 'auto_repair', 'car_wash', 'gas_station', 'tire_shop'],
            'Professional': ['marketing_agency', 'consulting', 'photography', 'graphic_design', 'web_design']
        }
        
        print("🚀 Starting Large Seattle Business Generation")
        print("=" * 70)
        
        for category, subcategories in categories.items():
            self.generate_businesses_for_category(category, subcategories, 25)
        
        print(f"\n✅ Generated {len(self.businesses)} total businesses!")
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export business data to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seattle_businesses_large_{timestamp}.csv"
        
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
            filename = f"seattle_businesses_large_{timestamp}.json"
        
        data = {
            'metadata': {
                'total_businesses': len(self.businesses),
                'generation_date': datetime.now().isoformat(),
                'data_source': 'Large Dataset Generated',
                'location': 'Seattle, WA Metro Area'
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
            'average_rating': round(sum(b.rating for b in self.businesses) / len(self.businesses), 2)
        }
        
        for business in self.businesses:
            category = business.category
            if category not in stats['businesses_by_category']:
                stats['businesses_by_category'][category] = 0
            stats['businesses_by_category'][category] += 1
        
        return stats

def main():
    """Main execution function"""
    generator = LargeBusinessGenerator()
    
    # Generate all businesses (25 per category = 250 total)
    generator.generate_all_businesses()
    
    # Export data
    csv_file = generator.export_to_csv()
    json_file = generator.export_to_json()
    
    # Show statistics
    stats = generator.get_statistics()
    print("\n" + "="*70)
    print("📊 LARGE BUSINESS GENERATION STATISTICS")
    print("="*70)
    print(f"Total businesses generated: {stats['total_businesses']}")
    print(f"Businesses with email: {stats['businesses_with_email']}")
    print(f"Businesses with phone: {stats['businesses_with_phone']}")
    print(f"Businesses with website: {stats['businesses_with_website']}")
    print(f"Average rating: {stats['average_rating']}")
    print("\nBusinesses by category:")
    for category, count in stats['businesses_by_category'].items():
        print(f"  {category}: {count}")
    
    print(f"\n📁 Files created:")
    print(f"  CSV: {csv_file}")
    print(f"  JSON: {json_file}")
    
    # Show sample businesses
    if generator.businesses:
        print(f"\n🏪 Sample businesses generated:")
        for i, business in enumerate(generator.businesses[:8]):
            print(f"\n{i+1}. {business.name}")
            print(f"   Category: {business.category} - {business.subcategory}")
            print(f"   Phone: {business.phone}")
            print(f"   Email: {business.email}")
            print(f"   Address: {business.address}")
            print(f"   Website: {business.website}")
            print(f"   Rating: {business.rating}")

if __name__ == "__main__":
    main() 