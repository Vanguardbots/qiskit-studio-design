# Qiskit Studio - Node Reference

This document provides comprehensive documentation for all available nodes in Qiskit Studio. Each node represents a specialized quantum computing component that can be connected to create complex quantum workflows.

## Node Categories

### Circuit Construction Nodes
- [Circuit Library Node](#circuit-library-node)
- [Circuit Node](#circuit-node)
- [Gate Node](#gate-node)
- [Python Node](#python-node)

### Execution Nodes
- [Execution Node](#execution-node)
- [Runtime Node](#runtime-node)

### Optimization Nodes
- [Transpiler Node](#transpiler-node)
- [Transpiler AI Passes Node](#transpiler-ai-passes-node)
- [Transpiler Pass Node](#transpiler-pass-node)

### Analysis Nodes
- [Quantum Info Node](#quantum-info-node)
- [Visualization Node](#visualization-node)

### Specialized Nodes
- [Chemistry Mapping Node](#chemistry-mapping-node)

---

## Circuit Library Node

**Purpose**: Provides access to pre-built quantum circuit templates from Qiskit's circuit library.

### Features
- **Circuit Types**: Ansatz, PauliTwoDesign, TwoLocal, NLocal
- **Configurable Parameters**: Qubit count, repetitions, and rotation gates
- **Automatic Code Generation**: Generates Python/Qiskit code for selected circuits
- **Parameterized Circuits**: Supports variational quantum algorithms

### Usage
1. Select circuit type from dropdown
2. Configure parameters (qubits, repetitions)
3. The node automatically generates the corresponding Qiskit code
4. Connect to execution or transpiler nodes

### Generated Code Example
```python
from qiskit.circuit.library import TwoLocal

# Create a TwoLocal circuit
circuit = TwoLocal(
    num_qubits=4,
    rotation_blocks=['ry', 'rz'],
    entanglement_blocks='cz',
    entanglement='linear',
    reps=2
)
```

### Input/Output
- **Input**: Configuration parameters
- **Output**: Configured quantum circuit object

---

## Circuit Node

**Purpose**: Basic quantum circuit creation and configuration with streamlined interface.

### Features
- **Circuit Types**: Ansatz, PauliTwoDesign, TwoLocal, NLocal
- **Compact Design**: Blue-themed UI for easy identification
- **Quick Setup**: Minimal configuration for rapid prototyping
- **Standard Integration**: Compatible with all other nodes

### Usage
Similar to Circuit Library Node but with simplified interface focusing on core functionality.

### Input/Output
- **Input**: Circuit type and basic parameters
- **Output**: Quantum circuit object

---

## Gate Node

**Purpose**: Represents individual quantum gates in circuit construction.

### Features
- **Gate Types**: H, X, Y, Z, CX, CCX, and more
- **Color Coding**: 
  - H (Hadamard): Blue
  - X (Pauli-X): Red
  - Y (Pauli-Y): Yellow
  - Z (Pauli-Z): Purple
  - CX (CNOT): Green
  - CCX (Toffoli): Orange
- **Visual Identification**: Compact design for easy recognition
- **Parameterized Gates**: Support for rotation gates with parameters

### Usage
1. Drag gate nodes into the workspace
2. Connect to circuit or other gate nodes
3. Configure gate parameters if applicable
4. Gates are automatically added to the circuit in order

### Input/Output
- **Input**: Gate parameters (angles for rotation gates)
- **Output**: Gate operation to be added to circuit

---

## Python Node

**Purpose**: Allows insertion of custom Python code in quantum workflows.

### Features
- **Code Editor**: Large, resizable textarea with syntax highlighting
- **AI Integration**: AI-powered code generation and improvement
- **Flexible Execution**: Supports any Python code, not just quantum
- **Context Awareness**: Can access variables from connected nodes
- **Error Handling**: Displays execution errors and debugging information

### Usage
1. Write or paste Python code in the editor
2. Use AI assistance for code generation and improvement
3. Access variables from connected nodes
4. Execute code and view results

### AI Capabilities
- **Code Generation**: Generate quantum algorithms from descriptions
- **Code Improvement**: Optimize and enhance existing code
- **Error Correction**: Identify and fix common programming errors
- **Documentation**: Generate comments and documentation

### Input/Output
- **Input**: Python code and variables from connected nodes
- **Output**: Execution results and modified variables

---

## Execution Node

**Purpose**: Executes quantum circuits on quantum hardware or simulators.

### Features
- **Simple Interface**: Minimal configuration for quick execution
- **Backend Agnostic**: Works with any Qiskit-compatible backend
- **Result Handling**: Manages job submission and result retrieval
- **Error Management**: Handles execution errors gracefully

### Usage
1. Connect circuit nodes to the input
2. Configure execution parameters if needed
3. Execute the circuit
4. View results or connect to visualization nodes

### Input/Output
- **Input**: Quantum circuit to execute
- **Output**: Execution results or job reference

---

## Runtime Node

**Purpose**: Configures IBM Quantum Runtime execution with advanced error mitigation.

### Features
- **Resilience Levels**: Slider from 0-2 for error mitigation strength
- **Error Mitigation Options**:
  - TREX (Twirled Readout Error eXtinction)
  - ZNE (Zero Noise Extrapolation)
  - PEC (Probabilistic Error Cancellation)
  - PEA (Pauli Error Amplification)
  - Gate Twirling
  - Measurement Twirling
- **Primitive Support**: Both Estimator and Sampler primitives
- **Advanced Configuration**: Fine-tuned resilience settings

### Usage
1. Select resilience level using slider
2. Configure specific error mitigation techniques
3. Choose primitive type (Estimator/Sampler)
4. Connect to circuit and execution nodes

### Error Mitigation Techniques

#### TREX (Twirled Readout Error eXtinction)
- Mitigates readout errors through randomized measurements
- Effective for reducing measurement noise

#### ZNE (Zero Noise Extrapolation)
- Extrapolates to zero noise limit
- Particularly useful for NISQ devices

#### PEC (Probabilistic Error Cancellation)
- Cancels errors through probabilistic methods
- High accuracy but increased circuit overhead

### Input/Output
- **Input**: Runtime configuration and resilience settings
- **Output**: Configured runtime options for quantum execution

---

## Transpiler Node

**Purpose**: Configures quantum circuit transpilation for hardware optimization.

### Features
- **Optimization Levels**: Slider from 0-3
  - Level 0: No optimization
  - Level 1: Basic optimization
  - Level 2: Medium optimization
  - Level 3: Heavy optimization
- **Layout Methods**: 
  - Trivial, Dense, NoiseAdaptive, SabreLayout
- **Routing Methods**:
  - Basic, LookaheadSwap, StochasticSwap, SabreSwap
- **Translation Methods**:
  - Translator, BasisTranslator, UnitarySynthesis
- **Scheduling Options**: ASAP, ALAP scheduling
- **Seed Control**: Reproducible transpilation results

### Usage
1. Set optimization level with slider
2. Configure layout, routing, and translation methods
3. Set scheduling options if needed
4. Connect to circuit nodes for transpilation

### Optimization Levels Explained

#### Level 0 - No Optimization
- No circuit optimization
- Only basic mapping to hardware
- Fastest compilation

#### Level 1 - Light Optimization
- Basic gate cancellation
- Simple circuit optimizations
- Good balance of speed and optimization

#### Level 2 - Medium Optimization
- More aggressive optimization
- Commutative cancellation
- Better depth reduction

#### Level 3 - Heavy Optimization
- Maximum optimization
- Extensive circuit analysis
- Best performance but slower compilation

### Input/Output
- **Input**: Transpilation configuration parameters
- **Output**: Optimized quantum circuit for specific hardware

---

## Transpiler AI Passes Node

**Purpose**: Simplified transpiler configuration with AI-optimized passes.

### Features
- **AI Optimization**: Machine learning-enhanced transpilation
- **Simplified Interface**: Focus on essential options
- **Intelligent Defaults**: AI-selected optimal settings
- **Performance Focused**: Optimized for best results with minimal configuration

### Usage
1. Enable AI-optimized transpilation
2. Let AI select optimal passes
3. Review and adjust if needed
4. Connect to circuit for transpilation

### Input/Output
- **Input**: Basic transpiler parameters
- **Output**: AI-optimized transpiler configuration

---

## Transpiler Pass Node

**Purpose**: Provides access to individual transpiler optimization passes.

### Features
- **Extensive Library**: 33+ individual transpiler passes
- **Categorized Passes**:
  - **Optimization**: CircuitOptimization, Optimize1qGates, CXCancellation
  - **Layout**: DenseLayout, NoiseAdaptiveLayout, SabreLayout
  - **Routing**: BasicSwap, LookaheadSwap, SabreSwap
  - **Analysis**: ResourceEstimation, DepthAnalysis, WidthAnalysis
- **Detailed Descriptions**: Each pass includes explanation of functionality
- **Custom Workflows**: Build custom transpilation pipelines

### Pass Categories

#### Optimization Passes
- **Optimize1qGates**: Optimizes single-qubit gates
- **CXCancellation**: Cancels consecutive CX gates
- **CommutationAnalysis**: Analyzes gate commutation relationships
- **ConsolidateBlocks**: Combines blocks of gates

#### Layout Passes
- **TrivialLayout**: Simple qubit mapping
- **DenseLayout**: Dense connectivity mapping
- **NoiseAdaptiveLayout**: Noise-aware qubit placement
- **SabreLayout**: SABRE algorithm for layout

#### Routing Passes
- **BasicSwap**: Basic SWAP insertion
- **LookaheadSwap**: Lookahead SWAP routing
- **StochasticSwap**: Stochastic SWAP placement
- **SabreSwap**: SABRE routing algorithm

### Usage
1. Select specific transpiler pass from library
2. Configure pass parameters
3. Chain multiple passes for custom pipelines
4. Connect to circuit for transpilation

### Input/Output
- **Input**: Transpiler pass selection and parameters
- **Output**: Specific optimization pass configuration

---

## Quantum Info Node

**Purpose**: Handles quantum information objects and operators.

### Features
- **Object Types**:
  - **Hamiltonian**: Quantum system energy operators
  - **Pauli**: Pauli operator representations
  - **SparsePauliOp**: Sparse Pauli operator format
  - **Operator**: General quantum operators
- **Automatic Generation**: Creates quantum information objects from specifications
- **Integration**: Works with Qiskit's quantum_info module
- **Format Support**: Multiple quantum information formats

### Usage
1. Select quantum information type
2. Specify operator parameters
3. Generate quantum information object
4. Connect to algorithms or analysis nodes

### Quantum Information Types

#### Hamiltonian
- Represents system energy
- Used in VQE and quantum simulation
- Supports molecular and spin Hamiltonians

#### Pauli Operators
- Fundamental quantum operators
- Basis for many quantum algorithms
- Efficient representation for quantum systems

#### SparsePauliOp
- Memory-efficient Pauli operator storage
- Optimized for large quantum systems
- Compatible with Qiskit algorithms

### Input/Output
- **Input**: Quantum information type and parameters
- **Output**: Quantum information objects (operators, states, etc.)

---

## Visualization Node

**Purpose**: Renders quantum computation results in various visual formats.

### Features
- **Visualization Types**:
  - **Histogram**: Measurement result distributions
  - **Bloch Sphere**: Qubit state visualization
  - **Circuit Diagram**: Circuit structure display
  - **Raw Output**: Unprocessed result data
- **Dynamic Display**: Updates based on connected results
- **Interactive Elements**: Zoom, pan, and explore visualizations
- **Export Options**: Save visualizations as images

### Visualization Types

#### Histogram
- Shows measurement outcome probabilities
- Useful for analyzing quantum algorithm results
- Supports both classical and quantum register results

#### Bloch Sphere
- 3D visualization of single-qubit states
- Shows quantum state evolution
- Interactive rotation and exploration

#### Circuit Diagram
- Visual representation of quantum circuits
- Shows gate sequence and qubit connectivity
- Useful for circuit analysis and debugging

#### Raw Output
- Unprocessed quantum computation results
- Detailed job information and metadata
- Useful for debugging and analysis

### Usage
1. Select visualization type
2. Connect to result-producing nodes
3. Configure display options
4. View and interact with visualizations

### Input/Output
- **Input**: Quantum computation results
- **Output**: Visual representations of quantum data

---

## Chemistry Mapping Node

**Purpose**: Maps molecular structures to quantum Hamiltonians for quantum chemistry applications.

### Features
- **Molecular Input**: PySCF-compatible molecular specifications
- **Basis Set Support**: Various quantum chemistry basis sets
- **Hamiltonian Generation**: Automatic quantum Hamiltonian creation
- **AI Integration**: AI-powered molecular structure optimization
- **Template Systems**: Common molecular examples (N₂, H₂O, etc.)

### Usage
1. Input molecular structure using PySCF syntax
2. Specify basis set (6-31g, cc-pVDZ, etc.)
3. Configure symmetry and other parameters
4. Generate quantum Hamiltonian
5. Connect to VQE or other quantum chemistry algorithms

### Molecular Specification Format
```python
# Example N₂ molecule
N 0.0 0.0 0.0
N 0.0 0.0 1.1
```

### Supported Features
- **Atoms**: All periodic table elements
- **Basis Sets**: Standard quantum chemistry basis sets
- **Symmetry**: Point group symmetry handling
- **Optimization**: Geometry optimization capabilities

### Input/Output
- **Input**: Molecular structure and parameters
- **Output**: Quantum Hamiltonian for molecular system

---

## Node Connection Guidelines

### General Connection Rules
1. **Data Flow**: Nodes should be connected in logical data flow order
2. **Type Compatibility**: Ensure output types match input requirements
3. **Error Handling**: Improper connections will show error messages
4. **Performance**: Minimize unnecessary connections for better performance

### Common Connection Patterns

#### Basic Circuit Execution
```
Circuit Library → Transpiler → Execution → Visualization
```

#### Quantum Chemistry Workflow
```
Chemistry Mapping → Python (VQE) → Runtime → Visualization
```

#### Circuit Optimization
```
Circuit → Transpiler Pass → Transpiler → Execution
```

#### AI-Assisted Development
```
Python (AI) → Circuit Library → Transpiler AI → Runtime
```

### Best Practices
1. **Start Simple**: Begin with basic connections, add complexity gradually
2. **Test Incrementally**: Test each connection as you build
3. **Use Visualization**: Always connect visualization nodes to see results
4. **Document Workflows**: Use Python nodes to add documentation
5. **Error Checking**: Include error handling in custom Python code

---

## Troubleshooting

### Common Issues

#### Connection Errors
- **Problem**: Nodes won't connect
- **Solution**: Check input/output type compatibility

#### Execution Failures
- **Problem**: Code doesn't execute
- **Solution**: Check for syntax errors and missing imports

#### Performance Issues
- **Problem**: Slow execution
- **Solution**: Optimize transpiler settings and reduce circuit complexity

#### AI Not Responding
- **Problem**: AI features not working
- **Solution**: Check API configuration and network connectivity

### Debug Tips
1. **Use Print Statements**: Add debugging prints in Python nodes
2. **Check Console**: Browser console shows detailed error messages
3. **Incremental Testing**: Test individual nodes before complex workflows
4. **Review Generated Code**: Examine auto-generated Python code for issues

---

## Advanced Usage

### Custom Node Development
While not directly supported, you can extend functionality through:
1. **Python Nodes**: Implement custom logic
2. **API Integration**: Connect to external services
3. **Data Processing**: Custom data transformation pipelines

### Integration with External Tools
- **Qiskit Optimization**: Use with quantum optimization algorithms
- **Qiskit Machine Learning**: Integrate ML algorithms
- **Third-party Libraries**: Import additional Python libraries

### Performance Optimization
1. **Circuit Depth**: Minimize circuit depth for NISQ devices
2. **Gate Count**: Reduce total gate count through optimization
3. **Parallelization**: Use multiple execution nodes for parallel processing
4. **Caching**: Cache expensive computations in Python nodes

For more advanced usage patterns and examples, see the [usage guide](usage.md).