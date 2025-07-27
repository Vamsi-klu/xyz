#!/usr/bin/env python3
"""
Simple script to test Google Places API key
"""

import os
import requests
import json

def test_api_key():
    """Test the Google Places API key"""
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_PLACES_API_KEY environment variable not set")
        return False
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    # Test with a simple nearby search
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': '47.6062,-122.3321',  # Seattle coordinates
        'radius': 1000,  # 1km radius
        'type': 'restaurant',
        'key': api_key
    }
    
    try:
        print("🌐 Making API request...")
        response = requests.get(url, params=params, timeout=30)
        
        print(f"📊 Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'UNKNOWN')
            
            print(f"📋 API Response Status: {status}")
            
            if status == 'OK':
                results = data.get('results', [])
                print(f"✅ SUCCESS! Found {len(results)} places")
                
                if results:
                    print("\n🏪 Sample results:")
                    for i, place in enumerate(results[:3]):
                        print(f"  {i+1}. {place.get('name', 'Unknown')}")
                        print(f"     Rating: {place.get('rating', 'N/A')}")
                        print(f"     Address: {place.get('vicinity', 'N/A')}")
                        print()
                
                return True
                
            elif status == 'REQUEST_DENIED':
                error_message = data.get('error_message', 'No error message provided')
                print(f"❌ REQUEST DENIED: {error_message}")
                print("\n🔧 Possible solutions:")
                print("1. Check if Places API is enabled in Google Cloud Console")
                print("2. Verify billing is set up for your Google Cloud project")
                print("3. Check if API key has proper permissions")
                print("4. Make sure API key is not restricted by IP/domain")
                return False
                
            elif status == 'OVER_QUERY_LIMIT':
                print("❌ OVER QUERY LIMIT: You've exceeded your API quota")
                print("💡 Wait 24 hours or increase your quota in Google Cloud Console")
                return False
                
            elif status == 'ZERO_RESULTS':
                print("⚠️  ZERO RESULTS: No places found (this might be normal)")
                return True
                
            else:
                print(f"⚠️  UNEXPECTED STATUS: {status}")
                if 'error_message' in data:
                    print(f"Error message: {data['error_message']}")
                return False
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Google Places API Key Tester")
    print("=" * 40)
    
    success = test_api_key()
    
    if success:
        print("\n✅ API key is working! You can now run the business scraper.")
    else:
        print("\n❌ API key test failed. Please fix the issues above before running the scraper.")
        print("\n📚 Additional resources:")
        print("- Google Cloud Console: https://console.cloud.google.com/")
        print("- Places API Documentation: https://developers.google.com/maps/documentation/places/web-service")

if __name__ == "__main__":
    main() 