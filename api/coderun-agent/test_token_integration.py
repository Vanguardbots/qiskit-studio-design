#!/usr/bin/env python3

# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0


"""
Test script to verify IBM Quantum token integration
"""

import requests
import json

# Test data
test_code_with_aer = """
from qiskit_aer import AerSimulator

backend = AerSimulator()
print("Using local simulator...")

print("Test successful!")
"""

test_code_with_ibm = """
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

print("Test successful!")
"""

def test_without_token():
    """Test without IBM token - should use local simulator"""
    print("Testing WITHOUT IBM token...")
    
    payload = {
        "input_value": test_code_with_ibm
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_with_token():
    """Test with IBM token - should use IBM Quantum Runtime Service"""
    print("Testing WITH IBM token...")
    
    # Using a fake token for testing - in real use, this would be a valid IBM token
    fake_token = "fake_token_for_testing"
    
    payload = {
        "input_value": test_code_with_aer,
        "ibm_token": fake_token
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_token_replacement():
    """Test that code gets properly replaced when token is provided"""
    print("Testing code replacement with token...")
    
    fake_token = "test_token_123"
    
    payload = {
        "input_value": test_code_with_aer,
        "ibm_token": fake_token
    }
    
    try:
        response = requests.post("http://localhost:8000/run", json=payload)
        result = response.json()
        
        # Check if the response contains evidence of IBM Quantum usage
        output = result.get("output", "")
        print(f"Output contains token replacement: {fake_token in output or 'IBM Quantum' in output}")
        print(f"Full output: {output}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("IBM Quantum Token Integration Test")
    print("=" * 50)
    
    test_without_token()
    test_with_token()
    test_token_replacement()
    
    print("\nTest completed. Make sure the agent.py server is running on port 8000.")