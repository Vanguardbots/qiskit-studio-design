# Parameter Update API Examples

This document shows examples of how the new Parameter Update API works with the Qiskit Code Updater AI Agent system prompt.

## Example 1: Runtime Node - Resilience Level Change

### User Action
User changes resilience level from 1 to 2 in a Runtime Node.

### Query Sent to Parameter Update API

```
Original Code Snippet:
```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1

options = {
    "resilience_level": 1,
    "optimization_level": 3,
    "resilience": {
        "measure_mitigation": True,
        "zne_mitigation": False,
        "pec_mitigation": False
    }
}
```

Qiskit Pattern Step: STEP 3

Parameters:
- resilience_level: 2

Target Specifications:
Update the code to reflect the new parameter value while maintaining functionality and following Qiskit best practices.
```

### Expected Response
```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 2

options = {
    "resilience_level": 2,
    "optimization_level": 3,
    "resilience": {
        "measure_mitigation": True,
        "zne_mitigation": True,
        "gate_twirling": True
    }
}
```

## Example 2: Transpiler Node - Optimization Level Change

### User Action
User changes optimization level from 1 to 3 in a Transpiler Node.

### Query Sent to Parameter Update API

```
Original Code Snippet:
```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

transpiler_options = {
    "optimization_level": 1,
    "layout_method": "sabre",
    "routing_method": "stochastic"
}

pass_manager = generate_preset_pass_manager(**transpiler_options)
```

Qiskit Pattern Step: STEP 2

Parameters:
- optimization_level: 3

Target Specifications:
Update the code to reflect the new parameter value while maintaining functionality and following Qiskit best practices.
```

### Expected Response
```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

transpiler_options = {
    "optimization_level": 3,
    "layout_method": "sabre",
    "routing_method": "stochastic"
}

pass_manager = generate_preset_pass_manager(**transpiler_options)
```

## Example 3: Circuit Node - Circuit Type Change

### User Action
User changes circuit type from "TwoLocal" to "PauliTwoDesign" in a Circuit Node.

### Query Sent to Parameter Update API

```
Original Code Snippet:
```python
from qiskit.circuit.library import TwoLocal

circuit_type = "TwoLocal"
circuit = TwoLocal(num_qubits=2, rotation_blocks='ry', entanglement_blocks='cz')
```

Qiskit Pattern Step: STEP 1

Parameters:
- circuit_type: PauliTwoDesign

Target Specifications:
Update the code to reflect the new parameter value while maintaining functionality and following Qiskit best practices.
```

### Expected Response
```python
from qiskit.circuit.library import PauliTwoDesign

circuit_type = "PauliTwoDesign"
circuit = PauliTwoDesign(num_qubits=2, reps=2)
```

## Example 4: Visualization Node - Visualization Type Change

### User Action
User changes visualization type from "Histogram" to "Bloch Sphere" in a Visualization Node.

### Query Sent to Parameter Update API

```
Original Code Snippet:
```python
from qiskit.visualization import plot_histogram

visualization_type = "Histogram"
plot_histogram(counts)
```

Qiskit Pattern Step: STEP 4

Parameters:
- visualization_type: Bloch Sphere

Target Specifications:
Update the code to reflect the new parameter value while maintaining functionality and following Qiskit best practices.
```

### Expected Response
```python
from qiskit.visualization import plot_bloch_multivector

visualization_type = "Bloch Sphere"
plot_bloch_multivector(quantum_state)
```

## Qiskit Pattern Step Mapping

| Node Type | Auto-Detected Step | Reasoning |
|-----------|-------------------|-----------|
| `circuitNode` | STEP 1 | Focuses on circuit structure and quantum state preparation |
| `circuitLibraryNode` | STEP 1 | Handles pre-built circuit templates and ansatz construction |
| `quantumInfoNode` | STEP 1 | Manages quantum information objects and problem encoding |
| `chemistryNode` / `chemistryMapNode` | STEP 1 | Maps molecular problems to quantum representations |
| `transpilerNode` | STEP 2 | Handles circuit optimization and transpilation settings |
| `transpilerPassNode` | STEP 2 | Manages specific optimization passes |
| `runtimeNode` | STEP 3 | Configures execution parameters and error mitigation |
| `executionNode` | STEP 3 | Handles job submission and backend configuration |
| `visualizationNode` | STEP 4 | Processes results and creates visualizations |
| `pythonNode` | STEP 1* | Auto-detects based on parameter type |

*Python nodes use parameter-based detection:
- Optimization parameters → STEP 2
- Execution parameters → STEP 3  
- Visualization parameters → STEP 4
- Default → STEP 1

## Key Benefits

1. **Accurate Context**: Each query includes the appropriate Qiskit Pattern Step
2. **Minimal Output**: AI returns only the necessary code changes
3. **Smart Detection**: Automatic step detection based on node type and parameter
4. **Consistent Format**: Structured query format matches the AI agent's expectations
5. **Focused Updates**: AI focuses on the right aspect of the code (mapping, optimization, execution, or post-processing)

## Configuration

To use the Parameter Update API, add this to your `.env.local`:

```bash
NEXT_PUBLIC_PARAMETER_UPDATE_API_URL=http://127.0.0.1:8001/chat
```

The system will automatically use this endpoint for all parameter updates while using the main API for chat and code improvements.