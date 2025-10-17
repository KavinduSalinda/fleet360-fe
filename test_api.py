#!/usr/bin/env python
"""
Test script for Fleet360 API endpoints
"""

import requests
import json


class Fleet360APITester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def login(self, email="admin@example.com", password="admin123"):
        """Test user login"""
        print("Testing user login...")
        url = f"{self.base_url}/users/login"
        data = {
            "email": email,
            "password": password
        }
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                self.token = result['data']['access_token']
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                print("✓ Login successful")
                return True
            else:
                print(f"✗ Login failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def test_customers(self):
        """Test customer endpoints"""
        print("\nTesting customer endpoints...")
        
        # Create customer
        customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "contact_number": "+1234567890",
            "nic": "123456789V",
            "passport_number": "P1234567",
            "country": "USA",
            "nationality": "American",
            "address": "123 Main St, City, State",
            "documents": [
                {
                    "document_name": "Passport",
                    "document_hash": "hash123.pdf"
                }
            ]
        }
        
        try:
            response = self.session.post(f"{self.base_url}/customers/", json=customer_data)
            if response.status_code == 201:
                print("✓ Customer created successfully")
                customer_id = response.json()['data']['customer_id']
                
                # Get customer
                response = self.session.get(f"{self.base_url}/customers/{customer_id}/")
                if response.status_code == 200:
                    print("✓ Customer retrieved successfully")
                else:
                    print(f"✗ Failed to retrieve customer: {response.status_code}")
                
                return customer_id
            else:
                print(f"✗ Failed to create customer: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Customer test error: {e}")
            return None
    
    def test_vehicles(self):
        """Test vehicle endpoints"""
        print("\nTesting vehicle endpoints...")
        
        # Get vehicle categories first
        try:
            response = self.session.get(f"{self.base_url}/categories/")
            if response.status_code == 200:
                print("✓ Vehicle categories retrieved")
            else:
                print(f"✗ Failed to get categories: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Vehicle test error: {e}")
            return None
    
    def test_bookings(self):
        """Test booking endpoints"""
        print("\nTesting booking endpoints...")
        
        try:
            response = self.session.get(f"{self.base_url}/bookings/locations/")
            if response.status_code == 200:
                print("✓ Locations retrieved successfully")
            else:
                print(f"✗ Failed to get locations: {response.status_code}")
        except Exception as e:
            print(f"✗ Booking test error: {e}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("Fleet360 API Test Suite")
        print("=" * 30)
        
        # Test login
        if not self.login():
            print("Cannot proceed without authentication")
            return
        
        # Test endpoints
        self.test_customers()
        self.test_vehicles()
        self.test_bookings()
        
        print("\n" + "=" * 30)
        print("API tests completed!")


if __name__ == '__main__':
    tester = Fleet360APITester()
    tester.run_all_tests()
