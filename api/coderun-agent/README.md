# Quantum Code Execution Agent

This project contains a FastAPI application that executes Python quantum computing code with automatic backend selection. The agent can run in two modes: local simulation or cloud execution with IBM Quantum.

## Features

- **Real Python Code Execution**: Executes actual Python code and returns live output
- **Automatic Backend Selection**: Intelligently switches between local simulators and IBM Quantum hardware
- **Quantum Computing Support**: Optimized for Qiskit quantum computing workflows
- **Structured Output**: Returns formatted results for different data types (text, plots, graphs)
- **Error Handling**: Captures both stdout and stderr with proper error reporting

## Running Locally

### Installation

```bash
uv sync
```

### Basic Usage

**Default (Local Mode)**:
```bash
uv run python agent.py
```

**With Custom Port**:
```bash
uv run python agent.py --port 8082
```

### Execution Modes

#### Local Mode (Default)
Uses local quantum simulators (AerSimulator) for development and testing:

```bash
uv run python agent.py --local
# OR
uv run python agent.py  # defaults to local mode
```

- Automatically replaces IBM Quantum Config sections with local simulators
- No IBM Quantum credentials required
- Perfect for development and testing

#### Cloud Mode  
Uses IBM Quantum hardware when available:

```bash
uv run python agent.py --cloud
```

- Executes original IBM Quantum code
- Requires valid IBM Quantum credentials
- For production quantum computing workloads

## API Usage

The agent exposes a single endpoint for code execution:

### POST /run

Execute Python code and return the output.

**Request Body**:
```json
{
  "input_value": "print('Hello World!')\nprint(2 + 3)"
}
```

**Response**:
```json
{
  "output": "Hello World!\n5\n"
}
```

### Quantum Code Examples

The agent automatically handles quantum code with IBM Quantum Config sections:

**Input**:
```json
{
  "input_value": "## STEP 0 : IBM Quantum Config\nfrom qiskit_ibm_runtime import QiskitRuntimeService\n\nservice = QiskitRuntimeService()\nbackend = service.least_busy(operational=True, simulator=False)\n\n## STEP 1 : Create Circuit\nfrom qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0, 1)\nprint(f'Created Bell state circuit with depth: {qc.depth()}')"
}
```

**Local Mode Response**:
```json
{
  "output": "Using local simulator...\nCreated Bell state circuit with depth: 2\n"
}
```

## Testing

### Running Tests

**Run all tests**:
```bash
uv run pytest tests/ -v
```

**Run specific test categories**:
```bash
# Unit tests only (fast)
uv run pytest tests/test_config_replacement.py -v

# Integration tests (require server startup)
uv run pytest tests/test_agent.py -v
uv run pytest tests/test_quantum_examples.py -v

# Run tests with coverage
uv run pytest tests/ --cov=agent --cov-report=html
```

### Test Structure

- `test_config_replacement.py` - Unit tests for IBM Quantum Config replacement logic
- `test_agent.py` - Integration tests for basic agent functionality 
- `test_quantum_examples.py` - Integration tests for quantum computing examples

### Manual Testing

Test the agent with curl:

```bash
# Start the agent in local mode
uv run python agent.py --port 8002 --local

# Test basic Python execution
curl -X POST -H "Content-Type: application/json" \
  -d '{"input_value": "print(\"Hello World!\")"}' \
  http://localhost:8002/run

# Test quantum circuit creation
curl -X POST -H "Content-Type: application/json" \
  -d '{"input_value": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0,1)\nprint(f\"Circuit depth: {qc.depth()}\")"}' \
  http://localhost:8002/run

# Test IBM Quantum Config replacement
curl -X POST -H "Content-Type: application/json" \
  -d '{"input_value": "## STEP 0 : IBM Quantum Config\nfrom qiskit_ibm_runtime import QiskitRuntimeService\nservice = QiskitRuntimeService()\nbackend = service.least_busy(operational=True, simulator=False)\nprint(\"Backend selected\")"}' \
  http://localhost:8002/run
```

### Testing Different Modes

```bash
# Test local mode (default)
uv run python agent.py --port 8002 --local

# Test cloud mode  
uv run python agent.py --port 8002 --cloud

# Test with quantum examples
curl -X POST -H "Content-Type: application/json" -d @test_simple_quantum.json http://localhost:8002/run
```

## Running the Application with Kubernetes (kind)

This guide explains how to run the application on a local Kubernetes cluster using `kind`.

### Prerequisites

Make sure you have the following tools installed:

*   [Docker](https://docs.docker.com/get-docker/)
*   [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
*   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### Steps

1.  **Build the Docker image:**

    ```bash
    docker build -t coderun-agent:latest .
    ```

1.  **Create a kind cluster (if you don't already have one):**

    ```bash
    kind create cluster
    ```

1.  **Load the Docker image into your kind cluster:**

    This command makes the locally built image available to the kind cluster, so you don't need to push it to a container registry.

    ```bash
    kind load docker-image coderun-agent:latest
    ```

1.  **Deploy the application to the cluster:**

    This will create a Deployment and a Service for the application.

    ```bash
    kubectl apply -f deployment.yaml
    ```

1.  **Verify the deployment:**

    Check that the pod is running. It might take a moment for the status to become `Running`.

    ```bash
    kubectl get pods
    ```

    You should see output similar to this:

    ```
    NAME                                      READY   STATUS    RESTARTS   AGE
    coderun-agent-deployment-XXXXXXXXXX-XXXXX   1/1     Running   0          ...
    ```

1.  **Port-forward the service to access it locally:**

    This command forwards a local port (e.g., 8080) to the service running inside the cluster.

    ```bash
    kubectl port-forward service/coderun-agent-service 8080:80
    ```

1.  **Test the endpoint:**

    Open a new terminal and use `curl` to send a request to the `/run` endpoint.

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"input_value": "s=\"test\"\nprint(s)"}' http://localhost:8080/run
    ```

    You should receive the following JSON response:

    ```json
    {"output":"test\n"}
    ```

### Cleanup

1.  **Remove the deployment and service:**

    ```bash
    kubectl delete -f deployment.yaml
    ```

1.  **Delete the kind cluster (optional):**

    If you no longer need the cluster, you can delete it.

    ```bash
    kind delete cluster
    ```
