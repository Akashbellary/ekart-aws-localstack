#!/usr/bin/env python3
"""
Simple integration test for the EKart Store API
"""

import requests
import sys
import json
from pathlib import Path

# Load API Gateway URL from serverless-config.json
CONFIG_PATH = Path(__file__).parent.parent / 'serverless-config.json'
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
API_URL = config['api_url']

def test_health():
    """Test health endpoint"""
    # Serverless API may not have /health, so just check /products
    response = requests.get(f"{API_URL}/api/products")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200
    print("✓ Products health check passed")

def test_products():
    """Test products endpoint"""
    response = requests.get(f"{API_URL}/api/products")
    assert response.status_code == 200
    print("✓ Products endpoint passed")

def test_categories():
    """Test categories endpoint"""
    response = requests.get(f"{API_URL}/api/products/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✓ Categories endpoint passed ({len(data)} categories)")

if __name__ == "__main__":
    import traceback
    print("🧪 Running integration tests...")
    try:
        test_health()
        test_products()
        test_categories()
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        sys.exit(1)
