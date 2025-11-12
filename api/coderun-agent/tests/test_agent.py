# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

"""
Test suite for the Quantum Code Execution Agent.
"""

import pytest
import requests
import json
import subprocess
import time
import os
import signal
from typing import Generator


class TestAgent:
    """Test class for the quantum code execution agent."""
    
    @pytest.fixture(scope="class")
    def agent_server(self) -> Generator[str, None, None]:
        """Start the agent server for testing."""
        # Start server in local mode on port 8003
        process = subprocess.Popen(
            ["uv", "run", "python", "agent.py", "--port", "8003", "--local"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        base_url = "http://localhost:8003"
        
        # Verify server is running
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            assert response.status_code == 200
        except Exception as e:
            process.terminate()
            raise e
        
        yield base_url
        
        # Cleanup
        process.terminate()
        process.wait()
    
    def test_basic_python_execution(self, agent_server: str):
        """Test basic Python code execution."""
        payload = {
            "input_value": "print('Hello World!')\nprint(2 + 3)"
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Hello World!" in data["output"]
        assert "5" in data["output"]
    
    def test_python_error_handling(self, agent_server: str):
        """Test error handling for invalid Python code."""
        payload = {
            "input_value": "print('Hello')\nundefined_variable"
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Error executing code" in data["output"]
        assert "undefined_variable" in data["output"]
    
    def test_quantum_config_replacement_local_mode(self, agent_server: str):
        """Test IBM Quantum Config replacement in local mode."""
        payload = {
            "input_value": """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f'Using backend: {backend.name}')

## STEP 1 : Test
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
print('Created Bell state circuit')
print(f'Circuit depth: {qc.depth()}')"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Using local simulator..." in data["output"]
        assert "Created Bell state circuit" in data["output"]
        assert "Circuit depth: 2" in data["output"]
    
    def test_quantum_circuit_creation(self, agent_server: str):
        """Test quantum circuit creation and manipulation."""
        payload = {
            "input_value": """
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# Create a simple quantum circuit
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure_all()

print(f'Circuit has {qc.num_qubits} qubits')
print(f'Circuit depth: {qc.depth()}')
print(f'Number of operations: {len(qc)}')

# Simulate
backend = AerSimulator()
job = backend.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()
print(f'Got {len(counts)} different measurement outcomes')
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Circuit has 3 qubits" in data["output"]
        assert "Circuit depth:" in data["output"]
        assert "Number of operations:" in data["output"]
        assert "Got" in data["output"] and "different measurement outcomes" in data["output"]
    
    def test_numpy_operations(self, agent_server: str):
        """Test numpy operations work correctly."""
        payload = {
            "input_value": """
import numpy as np

# Test basic numpy operations
arr = np.array([1, 2, 3, 4, 5])
print(f'Array: {arr}')
print(f'Mean: {np.mean(arr)}')
print(f'Sum: {np.sum(arr)}')

# Test matrix operations
matrix = np.array([[1, 2], [3, 4]])
print(f'Matrix shape: {matrix.shape}')
print(f'Matrix determinant: {np.linalg.det(matrix)}')
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Array: [1 2 3 4 5]" in data["output"]
        assert "Mean: 3.0" in data["output"]
        assert "Sum: 15" in data["output"]
        assert "Matrix shape: (2, 2)" in data["output"]
    
    def test_json_output_parsing(self, agent_server: str):
        """Test structured JSON output from quantum code."""
        payload = {
            "input_value": """
import json
import numpy as np

# Simulate structured output like CHSH example
data = {
    "CHSH1": [1.0, 0.5, -0.3, -1.2, -0.8],
    "CHSH2": [0.8, 1.1, 0.2, -0.9, -1.3]
}

output_plot = {"CHSH1": data["CHSH1"], "CHSH2": data["CHSH2"]}
print(f'RESULT: {json.dumps({"type":"plot","content":output_plot})}')
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "RESULT:" in data["output"]
        assert '"type"' in data["output"] and '"plot"' in data["output"]
        assert '"content"' in data["output"]
        assert "CHSH1" in data["output"]
        assert "CHSH2" in data["output"]
    
    def test_long_running_code(self, agent_server: str):
        """Test code that takes some time to execute."""
        payload = {
            "input_value": """
import time

print("Starting long computation...")
for i in range(5):
    time.sleep(0.1)  # Short sleep to simulate work
    print(f"Step {i+1} completed")

print("Computation finished!")
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Starting long computation..." in data["output"]
        assert "Step 1 completed" in data["output"]
        assert "Step 5 completed" in data["output"]
        assert "Computation finished!" in data["output"]
    
    def test_empty_code(self, agent_server: str):
        """Test handling of empty code."""
        payload = {
            "input_value": ""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert "Code executed successfully (no output)" in data["output"]
    
    def test_invalid_json_request(self, agent_server: str):
        """Test handling of invalid JSON requests."""
        response = requests.post(
            f"{agent_server}/run",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return an error status
        assert response.status_code == 422 or response.status_code == 400


class TestCloudMode:
    """Test class for cloud mode functionality."""
    
    @pytest.fixture(scope="class")
    def cloud_agent_server(self) -> Generator[str, None, None]:
        """Start the agent server in cloud mode for testing."""
        # Start server in cloud mode on port 8004
        process = subprocess.Popen(
            ["uv", "run", "python", "agent.py", "--port", "8004", "--cloud"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        base_url = "http://localhost:8004"
        
        # Verify server is running
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            assert response.status_code == 200
        except Exception as e:
            process.terminate()
            raise e
        
        yield base_url
        
        # Cleanup
        process.terminate()
        process.wait()
    
    def test_cloud_mode_no_replacement(self, cloud_agent_server: str):
        """Test that cloud mode doesn't replace IBM Quantum Config."""
        payload = {
            "input_value": """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f'Using backend: {backend.name}')"""
        }
        
        response = requests.post(
            f"{cloud_agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        # Should get IBM Quantum error, not local simulator message
        assert "Error executing code" in data["output"]
        # Accept any error message, but make sure it's not the local simulator message
        assert "Using local simulator..." not in data["output"]