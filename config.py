"""
Configuration file for Seattle Business Scraper
"""

import os
from typing import Dict, List

class Config:
    """Configuration class for the scraper"""
    
    # API Configuration
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '')
    
    # Seattle coordinates (downtown Seattle)
    SEATTLE_COORDS = "47.6062,-122.3321"
    SEARCH_RADIUS = 25000  # 25km radius to cover Seattle metro area
    
    # Rate limiting (seconds between requests)
    REQUEST_DELAY = 1.0
    DETAILS_REQUEST_DELAY = 0.5
    PAGINATION_DELAY = 2.0
    
    # Timeout settings
    WEBSITE_TIMEOUT = 10
    API_TIMEOUT = 30
    
    # Export settings
    EXPORT_FORMATS = ['csv', 'json']
    INCLUDE_PLACE_ID_IN_CSV = False
    
    # Business categories to search for
    BUSINESS_CATEGORIES = {
        'Food': [
            'restaurant', 'cafe', 'bakery', 'bar', 'fast_food',
            'meal_takeaway', 'meal_delivery', 'food_truck', 'pizza_delivery'
        ],
        'Salon': [
            'hair_care', 'beauty_salon', 'barber_shop'
        ],
        'Beauty': [
            'beauty_salon', 'spa', 'nail_salon', 'cosmetics_store',
            'massage_therapist', 'eyebrow_threading', 'tanning_salon'
        ],
        'Healthcare': [
            'doctor', 'dentist', 'pharmacy', 'hospital', 'veterinary_care',
            'physiotherapist', 'chiropractor', 'medical_clinic'
        ],
        'Retail': [
            'clothing_store', 'shoe_store', 'jewelry_store', 'electronics_store',
            'book_store', 'furniture_store', 'home_goods_store', 'florist',
            'pet_store', 'bicycle_store'
        ],
        'Services': [
            'lawyer', 'accountant', 'real_estate_agency', 'insurance_agency',
            'bank', 'atm', 'car_repair', 'locksmith', 'plumber', 'electrician',
            'dry_cleaning', 'laundry'
        ],
        'Entertainment': [
            'movie_theater', 'bowling_alley', 'gym', 'amusement_park',
            'night_club', 'casino', 'art_gallery', 'museum'
        ],
        'Education': [
            'school', 'university', 'library', 'driving_school', 'tutoring_center'
        ],
        'Automotive': [
            'car_dealer', 'car_rental', 'car_wash', 'gas_station', 'auto_parts_store'
        ],
        'Professional': [
            'consulting_agency', 'marketing_agency', 'advertising_agency',
            'graphic_designer', 'photographer', 'event_planner'
        ]
    }
    
    # Fields to extract from Google Places API
    PLACE_DETAILS_FIELDS = [
        'name',
        'formatted_phone_number',
        'formatted_address',
        'website',
        'rating',
        'types',
        'opening_hours',
        'price_level'
    ]
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'seattle_business_scraper.log'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.GOOGLE_PLACES_API_KEY:
            print("ERROR: GOOGLE_PLACES_API_KEY environment variable is not set!")
            return False
        
        if cls.SEARCH_RADIUS <= 0:
            print("ERROR: SEARCH_RADIUS must be positive!")
            return False
        
        return True
    
    @classmethod
    def get_categories_for_search(cls, selected_categories: List[str] = None) -> Dict[str, List[str]]:
        """Get categories to search for, optionally filtered"""
        if selected_categories is None:
            return cls.BUSINESS_CATEGORIES
        
        return {
            category: subcategories 
            for category, subcategories in cls.BUSINESS_CATEGORIES.items()
            if category in selected_categories
        } 