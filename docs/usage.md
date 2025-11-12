# Qiskit Studio - Usage Guide

This guide covers how to use Qiskit Studio effectively, from basic circuit building to advanced quantum algorithms.

## Getting Started

### First Steps

1. **Launch Qiskit Studio**
   - Open `http://localhost:3000` in your browser
   - Ensure the Maestro AI agents are running (see [api/README.md](../api/README.md) for setup)

2. **Interface Overview**
   - **Canvas**: Central area for building quantum workflows
   - **Sidebar**: Node library and tools
   - **Code Panel**: Generated Python code display
   - **Settings**: Configuration and preferences

3. **Basic Navigation**
   - **Drag and Drop**: Add nodes from sidebar to canvas
   - **Connect Nodes**: Click and drag between node handles
   - **Zoom**: Mouse wheel or trackpad gestures
   - **Pan**: Click and drag on empty canvas space

## Basic Workflows

### Creating Your First Circuit

1. **Add a Circuit Library Node**
   ```
   Sidebar → Circuit → Circuit Library
   ```
   - Select circuit type (e.g., "TwoLocal")
   - Configure parameters (qubits: 4, reps: 2)

2. **Add Visualization**
   ```
   Sidebar → Analysis → Visualization
   ```
   - Select "Circuit Diagram" visualization
   - Connect Circuit Library output to Visualization input

3. **View Generated Code**
   - Check the code panel for auto-generated Python
   - Copy code for external use

### Running a Quantum Circuit

1. **Build Circuit**
   ```
   Circuit Library → Transpiler → Execution → Visualization
   ```

2. **Configure Execution**
   - **Transpiler**: Set optimization level (0-3)
   - **Execution**: Choose backend (simulator/hardware)
   - **Visualization**: Select "Histogram" for results

3. **Execute Workflow**
   - Click "Run" on any node to execute the entire flow
   - Monitor execution progress in status indicators

## Advanced Features

### Quantum Chemistry Simulation

#### VQE (Variational Quantum Eigensolver)
```
Chemistry Mapping → Python (VQE) → Runtime → Visualization
```

1. **Molecule Definition**
   - Use Chemistry Mapping node
   - Input molecular structure (e.g., H2O)
   - Configure basis set (6-31g)

2. **VQE Implementation**
   - Add Python node
   - Use AI to generate VQE code
   - Configure optimizer and ansatz

3. **Execution with Error Mitigation**
   - Add Runtime node
   - Set resilience level (1-2)
   - Enable error mitigation techniques

#### Example: H2 Molecule
```python
# In Chemistry Mapping node
H 0.0 0.0 0.0
H 0.0 0.0 0.735
```

### Quantum Machine Learning

#### Quantum Kernel Training
```
Circuit Library → Python (Kernel) → Execution → Visualization
```

1. **Feature Map Circuit**
   - Use Circuit Library with "NLocal" ansatz
   - Configure for data encoding

2. **Kernel Implementation**
   - Python node with quantum kernel code
   - Use AI assistance for implementation
   - Configure training parameters

3. **Results Analysis**
   - Visualization node for accuracy metrics
   - Compare with classical methods

### Quantum Optimization

#### QAOA (Quantum Approximate Optimization Algorithm)
```
Python (Problem) → Circuit Library → Transpiler → Runtime → Visualization
```

1. **Problem Definition**
   - Python node to define optimization problem
   - Use Max-Cut or other combinatorial problems

2. **QAOA Circuit**
   - Circuit Library with parametrized ansatz
   - Configure mixing and cost operators

3. **Optimization Loop**
   - Runtime node for iterative optimization
   - Monitor convergence in visualization

## AI-Powered Development

### Code Generation

#### Using AI in Python Nodes
1. **Natural Language Input**
   ```
   "Create a quantum circuit for Grover's algorithm with 4 qubits"
   ```

2. **AI Processing**
   - Click "Generate with AI" button
   - Review generated code
   - Modify as needed

3. **Code Improvement**
   - Select existing code
   - Click "Improve with AI"
   - AI suggests optimizations

#### Example AI Prompts
- "Implement Shor's algorithm for factoring 15"
- "Create a quantum teleportation circuit"
- "Generate VQE code for molecular hydrogen"
- "Optimize this circuit for IBM hardware"

### Context-Aware Assistance

#### Smart Suggestions
- AI analyzes connected nodes
- Suggests appropriate next steps
- Provides context-aware code completion

#### Error Detection
- AI identifies common quantum programming errors
- Suggests fixes for circuit issues
- Provides debugging assistance

## Node-Specific Usage

### Circuit Construction

#### Gate Node Usage
```
Gate (H) → Gate (CX) → Measurement
```
- Color-coded gates for easy identification
- Drag gates to build custom circuits
- Parameters for rotation gates

#### Custom Circuit Building
- Start with basic gates
- Add entangling operations
- Include measurement operations
- Connect to execution nodes

### Transpilation and Optimization

#### Transpiler Node Configuration
1. **Optimization Level**
   - Level 0: No optimization (fastest)
   - Level 1: Basic optimization
   - Level 2: Medium optimization
   - Level 3: Heavy optimization (slowest)

2. **Hardware Mapping**
   - Choose target backend
   - Configure layout method
   - Set routing algorithm

3. **Advanced Options**
   - Scheduling: ASAP/ALAP
   - Seed for reproducibility
   - Custom basis gates

#### Transpiler Pass Node
- Select specific optimization passes
- Chain multiple passes
- Fine-tune optimization pipeline

### Execution and Runtime

#### IBM Quantum Runtime
1. **Primitive Selection**
   - **Estimator**: For expectation values
   - **Sampler**: For probability distributions

2. **Error Mitigation**
   - **Resilience Level**: 0 (none) to 2 (maximum)
   - **Techniques**: ZNE, PEC, TREX, Gate Twirling
   - **Configuration**: Automatic or manual

3. **Execution Options**
   - **Shots**: Number of measurements
   - **Optimization**: Runtime optimization level
   - **Monitoring**: Real-time job status

### Visualization and Analysis

#### Visualization Types
1. **Histogram**
   - Shows measurement results
   - Probability distributions
   - Statistical analysis

2. **Bloch Sphere**
   - Single-qubit state visualization
   - State evolution tracking
   - Interactive 3D display

3. **Circuit Diagram**
   - Visual circuit representation
   - Gate sequence display
   - Debugging assistance

4. **Raw Output**
   - Detailed execution results
   - Job metadata
   - Performance metrics

## Workflow Patterns

### Educational Workflows

#### Quantum Basics
```
Gate (H) → Gate (CX) → Execution → Visualization
```
- Start with simple gates
- Explore quantum phenomena
- Visualize results immediately

#### Algorithm Learning
```
Circuit Library → Python (Study) → Visualization
```
- Pre-built algorithm templates
- Study implementation details
- Experiment with parameters

### Research Workflows

#### Algorithm Development
```
Python (Research) → Circuit Library → Transpiler → Runtime → Visualization
```
- Implement new algorithms
- Test on simulators
- Optimize for hardware

#### Performance Analysis
```
Circuit → Multiple Transpilers → Multiple Runtimes → Comparison
```
- Compare different optimization strategies
- Analyze error mitigation effectiveness
- Benchmark across backends

### Production Workflows

#### Application Development
```
Problem Definition → Algorithm → Optimization → Execution → Results
```
- Define quantum application
- Implement and optimize
- Deploy to production hardware
- Monitor and analyze results

## Best Practices

### Circuit Design

#### Efficient Circuits
1. **Minimize Depth**: Reduce circuit depth for NISQ devices
2. **Gate Count**: Use fewer gates when possible
3. **Connectivity**: Consider hardware connectivity
4. **Error Rates**: Account for gate error rates

#### Debugging Strategies
1. **Incremental Building**: Test each component
2. **Simulation First**: Use simulators before hardware
3. **Visualization**: Always visualize intermediate results
4. **Error Checking**: Validate circuit construction

### Performance Optimization

#### Transpilation
1. **Choose Appropriate Level**: Balance optimization vs. compilation time
2. **Hardware-Specific**: Optimize for target backend
3. **Basis Gates**: Use native gate sets when possible
4. **Layout Awareness**: Consider qubit connectivity

#### Execution
1. **Shot Optimization**: Use appropriate number of shots
2. **Error Mitigation**: Enable for production workloads
3. **Batching**: Group similar circuits
4. **Monitoring**: Track execution metrics

### AI Integration

#### Effective Prompts
1. **Be Specific**: Provide detailed requirements
2. **Include Context**: Mention target hardware or constraints
3. **Iterative Refinement**: Refine prompts based on results
4. **Code Review**: Always review AI-generated code

#### Code Quality
1. **Validation**: Test AI-generated code thoroughly
2. **Documentation**: Document AI-assisted development
3. **Version Control**: Track code changes
4. **Peer Review**: Have others review AI contributions

## Troubleshooting

### Common Issues

#### Connection Problems
- **Symptom**: Nodes won't connect
- **Solution**: Check input/output type compatibility
- **Prevention**: Follow connection guidelines

#### Execution Errors
- **Symptom**: Code doesn't run
- **Solution**: Check syntax and imports
- **Prevention**: Use incremental testing

#### Performance Issues
- **Symptom**: Slow execution
- **Solution**: Optimize circuit and transpiler settings
- **Prevention**: Use appropriate optimization levels

### Debugging Techniques

#### Code Analysis
1. **Generated Code Review**: Check auto-generated Python
2. **Console Logs**: Monitor browser console
3. **Network Inspection**: Check API communications
4. **Error Messages**: Read error messages carefully

#### Testing Strategies
1. **Unit Testing**: Test individual nodes
2. **Integration Testing**: Test node connections
3. **End-to-End Testing**: Test complete workflows
4. **Performance Testing**: Monitor execution times

## Advanced Topics

### Custom Node Development

#### Python Node Extensions
- Import custom libraries
- Implement complex algorithms
- Create reusable functions
- Share code between nodes

#### API Integration
- Connect to external services
- Implement custom backends
- Create data pipelines
- Monitor external resources

### Workflow Automation

#### Batch Processing
- Process multiple circuits
- Parameter sweeps
- Parallel execution
- Result aggregation

#### Monitoring and Logging
- Track execution metrics
- Log workflow progress
- Performance monitoring
- Error tracking

### Integration with External Tools

#### Jupyter Notebooks
- Export workflows to notebooks
- Import existing code
- Interactive development
- Documentation generation

#### Version Control
- Track workflow changes
- Collaborate on projects
- Manage experiment versions
- Share reproducible results

## Examples and Templates

### Template Workflows

#### Quantum Teleportation
```
Bell State → Measurement → Classical Communication → Reconstruction
```

#### Quantum Fourier Transform
```
Circuit Library (QFT) → Transpiler → Execution → Visualization
```

#### Variational Quantum Eigensolver
```
Chemistry Mapping → Ansatz → Optimizer → Runtime → Analysis
```

### Example Problems

#### Max-Cut QAOA
- Graph problem definition
- QAOA circuit construction
- Parameter optimization
- Result interpretation

#### Quantum Machine Learning
- Data encoding circuits
- Variational classifiers
- Training loops
- Performance evaluation

For more examples and detailed tutorials, visit the [examples repository](https://github.com/AI4quantum/qiskit-studio/tree/main/examples).
