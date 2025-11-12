# Testing Framework for Qiskit Studio

This directory contains test scripts for validating the Qiskit Studio components.

## Test Categories

### Helm Chart Tests
- `helm-static-test.sh`: Validates Helm chart syntax and structure.
- `helm-icrkey-matrix.sh`: Tests image pull secret configurations for various scenarios

### Python Tests
- `python-tests.sh`: Runs Python tests for the coderun-agent.

## Running Tests Locally

### Prerequisites
- Python 3.8+
- uv (Python package manager)
- Helm 3+

To install uv:
```bash
pip install uv
```
Or visit: https://github.com/astral-sh/uv for installation instructions.

### Running Helm Tests
```bash
scripts/test/helm-static-test.sh
scripts/test/helm-icrkey-matrix.sh
```

### Running Python Tests
```bash
scripts/test/python-tests.sh
```

## Python Test Details

The Python tests include:

### Unit Tests
- `coderun-agent/tests/test_agent.py`: Tests the quantum code execution agent
- `coderun-agent/tests/test_quantum_examples.py`: Tests quantum computing examples
- `coderun-agent/tests/test_config_replacement.py`: Tests IBM Quantum config replacement

### Integration Tests
- `coderun-agent/test_token_integration.py`: Tests IBM Quantum token integration
- `coderun-agent/test_complete_integration.py`: Tests frontend-backend token integration

## Adding New Tests

### Adding New Helm Tests
1. Create a new test script in `scripts/test/`
2. Update `ci/scripts/unit-test.sh` to include your new test

### Adding New Python Tests
1. Add new test files to `coderun-agent/tests/` following pytest conventions
2. The tests will be automatically discovered by the `python-tests.sh` script

## Troubleshooting

### Agent Server Issues
For integration tests, the `python-tests.sh` script attempts to start the agent server if it's not already running. If you encounter issues with the agent server:

1. Try starting it manually:
   ```bash
   cd coderun-agent
   python agent.py --port 8000 --local
   ```

2. In a separate terminal, run the integration tests:
   ```bash
   cd coderun-agent
   python test_token_integration.py
   python test_complete_integration.py
   ```

### Dependency Issues
If you encounter dependency issues, install the required packages:
```bash
pip install pytest qiskit qiskit-aer qiskit-ibm-runtime numpy requests