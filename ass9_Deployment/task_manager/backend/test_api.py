import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("Testing FastAPI Backend")
print("=" * 50)

# Test 1: Health check
print("\n1. Testing health check (GET /)...")
try:
    r = requests.get(f"{BASE_URL}/")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Register
print("\n2. Testing register (POST /api/auth/register)...")
try:
    data = {"email": "testuser@example.com", "password": "password123"}
    r = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Login
print("\n3. Testing login (POST /api/auth/login)...")
try:
    data = {"username": "testuser@example.com", "password": "password123"}
    r = requests.post(f"{BASE_URL}/api/auth/login", data=data)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
