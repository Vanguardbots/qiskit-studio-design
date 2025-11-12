# API Prompt Example for Runtime Node

## Example of what the Parameter Update API will receive when resilience_level changes from 1 to 3:

```
###[Sampler]

```
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)

# Set resilience level to 1
estimator.options.resilience_level = 1

pub = (
    chsh_isa_circuit,  # ISA circuit
    [[isa_observable1], [isa_observable2]],  # ISA Observables
    individual_phases,  # Parameter values
)

###[Execute Job]
job_result = estimator.run(pubs=[pub]).result()
```

NEW PARAMETERS:

    resilience_level: 3
    trex: true
    zne: true
    pec: false
    pea: false
    dynamical_decoupling: false
    gate_twirling: true
    measurement_mitigation: true
```

## Expected API Response Format:

The API should return updated Python code that reflects the new resilience configuration. For example:

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)

# Set resilience level to 3 with enhanced error mitigation
estimator.options.resilience_level = 3

# Configure advanced error mitigation options
estimator.options.resilience.measure_mitigation = True
estimator.options.resilience.zne_mitigation = True
estimator.options.resilience.gate_twirling = True

pub = (
    chsh_isa_circuit,  # ISA circuit
    [[isa_observable1], [isa_observable2]],  # ISA Observables
    individual_phases,  # Parameter values
)

###[Execute Job]
job_result = estimator.run(pubs=[pub]).result()
```

## Key Changes Made:

1. **Prompt Format**: Updated to match your specified format with `###[NodeLabel]` and proper parameter formatting
2. **Comprehensive Parameters**: Now sends all resilience-related parameters together, not just the level
3. **Optimized API Calls**: Sliders only trigger API calls when user releases mouse button (onValueCommit), preventing excessive calls during dragging
4. **Immediate Visual Feedback**: UI updates instantly while dragging for smooth user experience
5. **Consistent Updates**: All runtime node controls (slider + switches) now trigger the same comprehensive update
6. **Proper Node Code**: The current Python code from the node is sent in the prompt for context

### User Experience Improvements:

- **Slider Behavior**: API calls only made on final value commit, not during dragging
- **Visual Updates**: UI updates immediately for responsive feel
- **Reduced API Load**: Fewer unnecessary API calls during user interaction
- **Better Performance**: Smoother interaction without lag from constant API requests

This ensures the API receives both the current code and all the new parameter values needed to generate updated Python code, while providing an optimal user experience.