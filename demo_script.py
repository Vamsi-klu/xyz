#!/usr/bin/env python3
"""
Demo script for Seattle Business Scraper
This script demonstrates how to use the scraper with a limited scope for testing.
"""

import os
import sys
from seattle_business_scraper import SeattleBusinessScraper, Business
from config import Config

def demo_limited_scrape():
    """Demo function that scrapes a limited number of businesses for testing"""
    
    # Check for API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("ERROR: Please set GOOGLE_PLACES_API_KEY environment variable")
        print("\nTo get a Google Places API key:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable the Places API")
        print("4. Create credentials (API key)")
        print("5. Set the environment variable: export GOOGLE_PLACES_API_KEY='your_key_here'")
        return
    
    print("🚀 Starting Seattle Business Scraper Demo")
    print("=" * 50)
    
    # Initialize scraper
    scraper = SeattleBusinessScraper(api_key)
    
    # Override categories for demo - just scrape a few types
    demo_categories = {
        'Food': ['restaurant', 'cafe'],
        'Salon': ['hair_care', 'beauty_salon'],
        'Beauty': ['spa', 'nail_salon']
    }
    
    # Override the categories in the scraper for demo
    scraper.categories = demo_categories
    
    # Reduce search radius for demo (10km instead of 25km)
    scraper.radius = 10000
    
    print(f"📍 Searching within 10km of downtown Seattle")
    print(f"🏢 Categories: {list(demo_categories.keys())}")
    print("⏱️  This demo should take 5-10 minutes...")
    print()
    
    try:
        # Run the scraper
        scraper.scrape_all_businesses()
        
        # Show results
        stats = scraper.get_statistics()
        print("\n" + "="*50)
        print("📊 DEMO RESULTS")
        print("="*50)
        print(f"Total businesses found: {stats['total_businesses']}")
        print(f"Businesses with email: {stats['businesses_with_email']}")
        print(f"Businesses with phone: {stats['businesses_with_phone']}")
        print(f"Businesses with website: {stats['businesses_with_website']}")
        
        print("\nBusinesses by category:")
        for category, count in stats['businesses_by_category'].items():
            print(f"  {category}: {count}")
        
        # Export demo data
        csv_file = scraper.export_to_csv("demo_seattle_businesses.csv")
        json_file = scraper.export_to_json("demo_seattle_businesses.json")
        
        print(f"\n📄 Demo data exported to:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        
        # Show sample businesses
        if scraper.businesses:
            print(f"\n🏪 Sample businesses found:")
            for i, business in enumerate(scraper.businesses[:5]):  # Show first 5
                print(f"\n{i+1}. {business.name}")
                print(f"   Category: {business.category} - {business.subcategory}")
                print(f"   Phone: {business.phone or 'N/A'}")
                print(f"   Email: {business.email or 'N/A'}")
                print(f"   Address: {business.address or 'N/A'}")
                print(f"   Website: {business.website or 'N/A'}")
                print(f"   Rating: {business.rating or 'N/A'}")
        
        print(f"\n✅ Demo completed successfully!")
        print(f"💡 To run the full scraper, use: python seattle_business_scraper.py")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred during demo: {e}")

def show_available_categories():
    """Show all available business categories"""
    print("📋 Available Business Categories:")
    print("=" * 40)
    
    for category, subcategories in Config.BUSINESS_CATEGORIES.items():
        print(f"\n{category}:")
        for subcat in subcategories:
            print(f"  - {subcat}")

def main():
    """Main demo function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--categories':
        show_available_categories()
        return
    
    print("Seattle Business Scraper - Demo Mode")
    print("=" * 40)
    print()
    print("This demo will:")
    print("✓ Search for restaurants, cafes, salons, and spas")
    print("✓ Limit search to 10km radius (vs 25km for full scrape)")
    print("✓ Show sample results")
    print("✓ Export demo data to CSV and JSON")
    print()
    print("💰 Estimated API cost: $5-10")
    print("⏱️  Estimated time: 5-10 minutes")
    print()
    
    response = input("Continue with demo? (y/n): ").lower().strip()
    if response == 'y' or response == 'yes':
        demo_limited_scrape()
    else:
        print("Demo cancelled.")
        print("💡 Run with --categories to see all available business types")

if __name__ == "__main__":
    main() 