#!/usr/bin/env python3
"""Simple test script to verify the frontend-backend integration."""

import requests
import time
import subprocess
import sys
import os

def test_backend_health():
    """Test if backend service is healthy."""
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def test_backend_chat():
    """Test the chat endpoint."""
    try:
        payload = {"query": "Hello, I want to start an interview for a software engineer position."}
        response = requests.post("http://localhost:8002/chat", json=payload, timeout=10)
        return response.status_code == 200 and response.json().get("status") == "success"
    except requests.exceptions.RequestException:
        return False

def main():
    """Run integration tests."""
    print("🧪 Testing PrepWise Integration...")
    
    # Test backend health
    print("1. Testing backend health endpoint...")
    if test_backend_health():
        print("   ✅ Backend health check passed")
    else:
        print("   ❌ Backend health check failed")
        print("   Make sure to start the backend service first:")
        print("   docker-compose up backend-service")
        return False
    
    # Test backend chat
    print("2. Testing backend chat endpoint...")
    if test_backend_chat():
        print("   ✅ Backend chat endpoint working")
    else:
        print("   ❌ Backend chat endpoint failed")
        print("   Make sure Ollama is running on localhost:11434")
        return False
    
    print("\n🎉 All tests passed! The integration is working correctly.")
    print("\nTo start the full application:")
    print("docker-compose up")
    print("\nThen visit: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
