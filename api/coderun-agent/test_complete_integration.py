#!/usr/bin/env python3

# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0


"""
Test script to verify complete frontend-backend token integration
"""

import requests
import json

# Test data - simulates what frontend sends
test_code_aer = """
from qiskit_aer import AerSimulator

backend = AerSimulator()
print("Using local simulator...")

print("Test successful!")
"""

test_code_ibm = """
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

print("Test successful!")
"""

def test_without_token():
    """Test without IBM token - should use local simulator"""
    print("Testing WITHOUT IBM token (should use AerSimulator)...")
    
    payload = {
        "input_value": test_code_ibm
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Output: {result.get('output', 'No output')}")
        
        # Check if it used local simulator
        output = result.get('output', '')
        if 'Using local simulator' in output:
            print("✅ Correctly using local simulator")
        else:
            print("❌ Not using local simulator as expected")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_with_token():
    """Test with IBM token - should inject token into code"""
    print("Testing WITH IBM token (should inject token)...")
    
    fake_token = "fake_test_token_123456"
    
    payload = {
        "input_value": test_code_aer,  # Start with AerSimulator code
        "ibm_token": fake_token
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Output: {result.get('output', 'No output')}")
        
        # Check if token was injected
        output = result.get('output', '')
        if fake_token in output or 'QiskitRuntimeService(token=' in output:
            print("✅ Token correctly injected")
        else:
            print("❌ Token not injected as expected")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_token_injection_in_ibm_code():
    """Test token injection in existing IBM code"""
    print("Testing token injection in existing IBM code...")
    
    fake_token = "another_fake_token_456"
    
    payload = {
        "input_value": test_code_ibm,  # IBM code without token
        "ibm_token": fake_token
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        result = response.json()
        output = result.get('output', '')
        
        print(f"Token in output: {fake_token in output}")
        print(f"Modified output snippet: {output[:200]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Complete Frontend-Backend Token Integration Test")
    print("=" * 60)
    
    test_without_token()
    test_with_token() 
    test_token_injection_in_ibm_code()
    
    print("\n✨ Integration test completed!")
    print("🔧 Make sure the agent.py server is running on port 8000")
    print("🌐 Frontend should now send tokens correctly via the Run button")