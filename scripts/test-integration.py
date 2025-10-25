#!/usr/bin/env python3
"""
Simple integration test for the EKart Store API
"""
import requests
import sys

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_products():
    """Test products endpoint"""
    response = requests.get(f"{API_URL}/api/products/")
    assert response.status_code == 200
    print("✓ Products endpoint passed")

def test_categories():
    """Test categories endpoint"""
    response = requests.get(f"{API_URL}/api/products/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✓ Categories endpoint passed ({len(data)} categories)")

if __name__ == "__main__":
    print("🧪 Running integration tests...")
    try:
        test_health()
        test_products()
        test_categories()
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
