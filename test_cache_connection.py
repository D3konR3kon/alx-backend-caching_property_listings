#!/usr/bin/env python
"""
Test script to verify Django cache and database connections
Run this script from the project root directory after setting up the environment
"""

import os
import sys
import django
from django.conf import settings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx-backend-caching_property_listings.settings')
django.setup()

from django.core.cache import cache
from django.db import connection
from properties.models import Property


def test_database_connection():
    """Test PostgreSQL database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Database connection successful")
            print(f"Database: {settings.DATABASES['default']['NAME']}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_cache_connection():
    """Test Redis cache connection"""
    try:

        cache.set('test_key', 'test_value', 30)
        value = cache.get('test_key')
        
        if value == 'test_value':
            print("✅ Cache connection successful")
            print(f"Cache backend: {settings.CACHES['default']['BACKEND']}")
            print(f"Cache location: {settings.CACHES['default']['LOCATION']}")
            
            cache.delete('test_key')
            return True
        else:
            print("❌ Cache connection failed: Value mismatch")
            return False
    except Exception as e:
        print(f"❌ Cache connection failed: {e}")
        return False


def test_model_operations():
    """Test Property model operations"""
    try:
        test_property = Property.objects.create(
            title="Test Property",
            description="A test property for verification",
            price=100000.00,
            location="Test City"
        )

        retrieved_property = Property.objects.get(id=test_property.id)
        
        print("✅ Model operations successful")
        print(f"Created property: {retrieved_property}")
        
        test_property.delete()
        return True
    except Exception as e:
        print(f"❌ Model operations failed: {e}")
        return False

def main():
    print("=== Property Listings App Setup Test ===\n")
    
    db_success = test_database_connection()
    print()
    
    cache_success = test_cache_connection()
    print()
    
    model_success = test_model_operations()
    print()
    
    if all([db_success, cache_success, model_success]):
        print("🎉 All tests passed! Your setup is working correctly.")
        print("\nNext steps:")
        print("1. Run: python manage.py createsuperuser")
        print("2. Run: python manage.py runserver")
        print("3. Visit: http://localhost:8000/admin/")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("\nTroubleshooting:")
        print("1. Ensure Docker services are running: docker-compose up -d")
        print("2. Check database settings in settings.py")
        print("3. Verify Redis is accessible on localhost:6379")
        print("4. Run migrations: python manage.py makemigrations && python manage.py migrate")

if __name__ == "__main__":
    main()