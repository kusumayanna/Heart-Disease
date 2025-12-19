#!/usr/bin/env python3
"""
Test script to verify the Heart Disease Classification deployment.
Tests both the FastAPI backend and Streamlit frontend connectivity.
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
STREAMLIT_URL = "http://localhost:8501"

def test_api_health():
    """Test API health endpoint."""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            print(f"   Model path: {data['model_path']}")
            return True
        else:
            print(f"❌ API Health failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False

def test_api_prediction():
    """Test API prediction endpoint."""
    print("\n🔍 Testing API Prediction...")
    
    # Sample patient data
    patient_data = {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict/single",
            json=patient_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Prediction: {data['prediction']} ({'Heart Disease' if data['prediction'] == 1 else 'No Heart Disease'})")
            print(f"   Probability: {data['probability'][1]*100:.1f}% disease risk")
            print(f"   Diagnosis: {data['diagnosis']}")
            return True
        else:
            print(f"❌ Prediction failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_streamlit_connectivity():
    """Test Streamlit frontend connectivity."""
    print("\n🔍 Testing Streamlit Frontend...")
    try:
        response = requests.get(STREAMLIT_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Streamlit frontend is accessible")
            print(f"   URL: {STREAMLIT_URL}")
            return True
        else:
            print(f"❌ Streamlit failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Streamlit error: {e}")
        return False

def test_api_docs():
    """Test API documentation endpoint."""
    print("\n🔍 Testing API Documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation is accessible")
            print(f"   URL: {API_BASE_URL}/docs")
            return True
        else:
            print(f"❌ API docs failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def main():
    """Run all deployment tests."""
    print("=" * 60)
    print("🚀 Heart Disease Classification - Deployment Test")
    print("=" * 60)
    
    tests = [
        ("API Health", test_api_health),
        ("API Prediction", test_api_prediction),
        ("Streamlit Frontend", test_streamlit_connectivity),
        ("API Documentation", test_api_docs),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Deployment is successful.")
        print("\n📱 Access your application:")
        print(f"   • Streamlit UI: {STREAMLIT_URL}")
        print(f"   • API Docs: {API_BASE_URL}/docs")
        print(f"   • API Health: {API_BASE_URL}/health")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) failed. Check the logs above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()