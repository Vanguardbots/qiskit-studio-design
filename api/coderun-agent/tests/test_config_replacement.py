# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

"""
Test suite for IBM Quantum Config replacement functionality.
"""

import pytest
import sys
import os

# Add the parent directory to the path to import agent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import replace_ibm_quantum_config


class TestConfigReplacement:
    """Test class for IBM Quantum Config replacement."""
    
    def test_replace_basic_config(self):
        """Test basic IBM Quantum config replacement."""
        # Mock LOCAL_MODE = True
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f'Using backend: {backend.name}')

## STEP 1 : Test
print('Hello World!')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should contain local simulator setup
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        assert "Using local simulator..." in replaced_code
        
        # Should not contain original IBM Quantum code
        assert "QiskitRuntimeService()" not in replaced_code
        assert "least_busy" not in replaced_code
        
        # Should preserve other sections
        assert "## STEP 1 : Test" in replaced_code
        assert "print('Hello World!')" in replaced_code
    
    def test_no_replacement_in_cloud_mode(self):
        """Test that no replacement occurs in cloud mode."""
        # Mock LOCAL_MODE = False
        import agent
        agent.LOCAL_MODE = False
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

## STEP 1 : Test
print('Hello World!')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should be identical to original
        assert replaced_code == original_code
        assert "QiskitRuntimeService()" in replaced_code
        assert "least_busy" in replaced_code
        assert "AerSimulator" not in replaced_code
    
    def test_no_config_section(self):
        """Test code without IBM Quantum config section."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
print('Circuit created')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should be unchanged
        assert replaced_code == original_code
        assert "AerSimulator" not in replaced_code
    
    def test_multiple_step_sections(self):
        """Test replacement with multiple STEP sections."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

## STEP 1 : Circuit Creation
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)

## STEP 2 : Execution
print('Running circuit')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should replace only STEP 0
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        
        # Should preserve other steps
        assert "## STEP 1 : Circuit Creation" in replaced_code
        assert "## STEP 2 : Execution" in replaced_code
        assert "from qiskit import QuantumCircuit" in replaced_code
        assert "print('Running circuit')" in replaced_code
        
        # Should not contain original config
        assert "QiskitRuntimeService()" not in replaced_code
    
    def test_config_with_subsections(self):
        """Test replacement with subsections (###)."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

###[Setup]
print('Setting up backend')

## STEP 1 : Circuit
print('Creating circuit')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should replace everything up to ## STEP 1
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        assert "## STEP 1 : Circuit" in replaced_code
        assert "print('Creating circuit')" in replaced_code
        
        # Should not contain original config or subsections
        assert "QiskitRuntimeService()" not in replaced_code
        assert "###[Setup]" not in replaced_code
        assert "Setting up backend" not in replaced_code
    
    def test_config_at_end_of_file(self):
        """Test replacement when config section is at the end."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f'Using backend: {backend.name}')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should replace the config section
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        assert "Using local simulator..." in replaced_code
        
        # Should not contain original config
        assert "QiskitRuntimeService()" not in replaced_code
        assert "least_busy" not in replaced_code
    
    def test_complex_config_section(self):
        """Test replacement of complex config section."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

# Initialize service
service = QiskitRuntimeService(channel='ibm_quantum')
available_backends = service.backends()
print(f"Available backends: {len(available_backends)}")

# Select backend
backend = service.least_busy(operational=True, simulator=False)
print(f"Selected backend: {backend.name}")
print(f"Backend status: {backend.status()}")

## STEP 1 : Next Section
print('Moving to next step')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should replace entire config section
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        assert "Using local simulator..." in replaced_code
        
        # Should preserve next section
        assert "## STEP 1 : Next Section" in replaced_code
        assert "print('Moving to next step')" in replaced_code
        
        # Should not contain any original config code
        assert "QiskitRuntimeService" not in replaced_code
        assert "available_backends" not in replaced_code
        assert "least_busy" not in replaced_code
        assert "backend.status()" not in replaced_code
    
    def test_whitespace_handling(self):
        """Test proper whitespace handling in replacement."""
        import agent
        agent.LOCAL_MODE = True
        
        original_code = """## STEP 0 : IBM Quantum Config

from qiskit_ibm_runtime import QiskitRuntimeService


service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)


## STEP 1 : Test
print('test')"""
        
        replaced_code = replace_ibm_quantum_config(original_code)
        
        # Should contain replacement
        assert "from qiskit_aer import AerSimulator" in replaced_code
        assert "backend = AerSimulator()" in replaced_code
        
        # Should preserve subsequent sections
        assert "## STEP 1 : Test" in replaced_code
        assert "print('test')" in replaced_code
        
        # Should not contain original
        assert "QiskitRuntimeService" not in replaced_code