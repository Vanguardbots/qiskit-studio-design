# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

"""
Test suite for the quantum computing examples.
"""

import pytest
import requests
import json
import subprocess
import time
import os
from typing import Generator


class TestQuantumExamples:
    """Test class for quantum computing examples."""
    
    @pytest.fixture(scope="class")
    def agent_server(self) -> Generator[str, None, None]:
        """Start the agent server for testing."""
        # Start server in local mode on port 8005
        process = subprocess.Popen(
            ["uv", "run", "python", "agent.py", "--port", "8005", "--local"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        base_url = "http://localhost:8005"
        
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
    
    def _load_quantum_example(self, filename: str) -> dict:
        """Load a quantum example file and return as JSON payload."""
        file_path = os.path.join("python_demos", filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
            return {"input_value": code}
        else:
            pytest.skip(f"Quantum example file {filename} not found")
    
    def test_chemistry_example(self, agent_server: str):
        """Test the quantum chemistry example."""
        payload = self._load_quantum_example("chemistry.py")
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=180  # Chemistry example can take time
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Check for key chemistry outputs
        assert "Using local simulator..." in data["output"]
        assert "Number of orbitals:" in data["output"]
        assert "Number of electrons:" in data["output"]
        assert "Qubits needed:" in data["output"]
        assert "Starting configuration recovery iteration" in data["output"]
        
        # Check for structured result
        if "RESULT:" in data["output"]:
            assert '"type":"text"' in data["output"]
            assert "Exact energy:" in data["output"]
            assert "Final SQD energy:" in data["output"]
    
    def test_chsh_example(self, agent_server: str):
        """Test the CHSH quantum example."""
        payload = self._load_quantum_example("CHSH.py")
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Check for key CHSH outputs
        assert "Using local simulator..." in data["output"]
        
        # Check for structured result
        if "RESULT:" in data["output"]:
            assert '"type"' in data["output"] and '"plot"' in data["output"]
            assert "CHSH1" in data["output"]
            assert "CHSH2" in data["output"]
    
    def test_maxcut_example(self, agent_server: str):
        """Test the MaxCut QAOA example."""
        payload = self._load_quantum_example("maxcut.py")
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300  # MaxCut optimization can take time
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Check for key MaxCut outputs
        assert "Using local simulator..." in data["output"]
        assert "Cost Function Hamiltonian:" in data["output"]
        
        # Check for optimization results
        if "success: True" in data["output"]:
            assert "fun:" in data["output"]  # Objective function value
            assert "nfev:" in data["output"]  # Number of function evaluations
        
        # Check for structured result
        if "RESULT:" in data["output"]:
            assert '"type"' in data["output"] and '"graph"' in data["output"]
            assert '"nodes"' in data["output"]
            assert '"edges"' in data["output"]
            assert '"bitstring"' in data["output"]
    
    def test_simple_quantum_circuit(self, agent_server: str):
        """Test a simple quantum circuit example."""
        payload = {
            "input_value": """
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a simple Bell state
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print(f'Created circuit with {qc.num_qubits} qubits')
print(f'Circuit depth: {qc.depth()}')
print(f'Gate count: {len(qc)}')

# Simulate
backend = AerSimulator()
job = backend.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print(f'Measurement results: {dict(counts)}')
print(f'Total shots: {sum(counts.values())}')
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Check circuit creation
        assert "Created circuit with 2 qubits" in data["output"]
        assert "Circuit depth:" in data["output"]
        assert "Gate count:" in data["output"]
        
        # Check simulation results
        assert "Measurement results:" in data["output"]
        assert "Total shots: 1000" in data["output"]
    
    def test_parametric_circuit(self, agent_server: str):
        """Test a parametric quantum circuit."""
        payload = {
            "input_value": """
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
import numpy as np

# Create parametric circuit
theta = Parameter('θ')
qc = QuantumCircuit(1, 1)
qc.ry(theta, 0)
qc.measure_all()

print(f'Created parametric circuit with {qc.num_parameters} parameters')
print(f'Parameters: {[str(p) for p in qc.parameters]}')

# Bind parameter and simulate
bound_qc = qc.assign_parameters({theta: np.pi/4})
backend = AerSimulator()
job = backend.run(bound_qc, shots=1000)
result = job.result()
counts = result.get_counts()

print(f'Results for θ=π/4: {dict(counts)}')

# Test different parameter values
for angle in [0, np.pi/2, np.pi]:
    test_qc = qc.assign_parameters({theta: angle})
    job = backend.run(test_qc, shots=100)
    result = job.result()
    counts = result.get_counts()
    prob_0 = counts.get('0', 0) / 100
    print(f'θ={angle:.3f}: P(0) = {prob_0:.2f}')
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Check parametric circuit creation
        assert "Created parametric circuit with 1 parameters" in data["output"]
        assert "Parameters: ['θ']" in data["output"]
        
        # Check parameter binding and results
        assert "Results for θ=π/4:" in data["output"]
        assert "P(0)" in data["output"]  # Probability outputs
    
    def test_quantum_error_handling(self, agent_server: str):
        """Test quantum code error handling."""
        payload = {
            "input_value": """
from qiskit import QuantumCircuit

# This should work
qc = QuantumCircuit(2)
qc.h(0)
print("First circuit created successfully")

# This should cause an error
qc.invalid_gate(0)  # This gate doesn't exist
print("This shouldn't print")
"""
        }
        
        response = requests.post(
            f"{agent_server}/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        
        # Should have error about invalid gate
        assert "Error executing code" in data["output"]
        assert "invalid_gate" in data["output"]