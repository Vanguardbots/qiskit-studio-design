/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

// Python template constants - extracted from Python files
// This allows us to avoid dynamic file reading and keep templates easily accessible

export const QUANTUM_INFO_TEMPLATES = {
  HAMILTONIAN: `from qiskit.quantum_info import SparsePauliOp

# Define number of qubits
num_qubits = 30

# Create a Hamiltonian using SparsePauliOp
obs = SparsePauliOp('I' + 'Z' + 'I' * (num_qubits-2))`,

  SPARSE_PAULI_OP: `from qiskit.quantum_info import SparsePauliOp

# Define number of qubits
num_qubits = 30

# Create a Sparse Pauli Operator
obs = SparsePauliOp('I' + 'Z' + 'I' * (num_qubits-2))`,

  TIME_EVOLUTION: `from qiskit.circuit.library import PauliEvolutionGate
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

# Prepare initial state
num_qubits = 3
state = QuantumCircuit(num_qubits)
state.h(1)

# Define Hamiltonian for time evolution
hamiltonian = SparsePauliOp(["ZZI", "IZZ"])
evolution_time = 1.0
evolution = PauliEvolutionGate(hamiltonian, time=evolution_time)

# Evolve state
state.compose(evolution, inplace=True)`,

  STATEVECTOR: `from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

# Create quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Get statevector
state = Statevector.from_instruction(qc)
print(f"Probabilities: {state.probabilities()}")`,

  DENSITY_MATRIX: `from qiskit.quantum_info import DensityMatrix
from qiskit import QuantumCircuit

# Create quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Get density matrix
rho = DensityMatrix.from_instruction(qc)
print(f"Trace: {rho.trace()}")
print(f"Purity: {rho.purity()}")`,

  ENTANGLEMENT_MEASURES: `from qiskit.quantum_info import entanglement_of_formation, concurrence
from qiskit.quantum_info import DensityMatrix
from qiskit import QuantumCircuit

# Create entangled state
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Calculate quantum information measures
rho = DensityMatrix.from_instruction(qc)
concur = concurrence(rho)
ent_form = entanglement_of_formation(rho)

print(f"Concurrence: {concur}")
print(f"Entanglement of Formation: {ent_form}")`
}

export const CIRCUIT_LIBRARY_TEMPLATES = {
  PAULI_TWO_DESIGN: `from qiskit.circuit.library import PauliTwoDesign

# Define number of qubits
num_qubits = 30

# Create a circuit using PauliTwoDesign
qc = PauliTwoDesign(num_qubits=num_qubits, reps=4, seed=5, insert_barriers=True)
parameters = qc.parameters`,

  BASIC_CIRCUIT: `from qiskit import QuantumCircuit

# Define number of qubits
num_qubits = 30

# Create a quantum circuit
qc = QuantumCircuit(num_qubits)`,

  // Standard Gates
  STANDARD_GATES: `from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, MCXGate

# Create gates
mcx_gate = MCXGate(3)
hadamard_gate = HGate()

# Create circuit and add gates
qc = QuantumCircuit(4)
qc.append(hadamard_gate, [0])
qc.append(mcx_gate, [0, 1, 2, 3])`,

  // N-Local Circuits
  N_LOCAL: `from qiskit.circuit.library import TwoLocal

# Create a two-local circuit with RX and CZ gates
num_qubits = 3
two_local = TwoLocal(num_qubits, 'rx', 'cz', reps=2)
parameters = two_local.parameters`,

  REAL_AMPLITUDES: `from qiskit.circuit.library import RealAmplitudes

# Create RealAmplitudes ansatz (common in VQE)
num_qubits = 4
ansatz = RealAmplitudes(num_qubits, reps=2)
parameters = ansatz.parameters`,

  EFFICIENT_SU2: `from qiskit.circuit.library import EfficientSU2

# Create EfficientSU2 ansatz (hardware-efficient)
num_qubits = 3
ansatz = EfficientSU2(num_qubits, reps=2)
parameters = ansatz.parameters`,

  // Data Encoding
  ZZ_FEATURE_MAP: `from qiskit.circuit.library import ZZFeatureMap

# Prepare data to encode
features = [0.2, 0.4, 0.8]
feature_map = ZZFeatureMap(feature_dimension=len(features), reps=2)
encoded_circuit = feature_map.assign_parameters(features)`,

  PAULI_FEATURE_MAP: `from qiskit.circuit.library import PauliFeatureMap

# Create Pauli feature map
data = [1.2, 0.5, -0.3, 0.8]
pauli_map = PauliFeatureMap(
    feature_dimension=len(data),
    reps=2,
    paulis=['Z', 'ZZ', 'ZZZ']
)
encoded = pauli_map.assign_parameters(data)`,

  // Benchmarking
  QUANTUM_VOLUME: `from qiskit.circuit.library import QuantumVolume

# Create quantum volume circuit for benchmarking
num_qubits = 4
qv_circuit = QuantumVolume(num_qubits)`,

  IQP_CIRCUIT: `from qiskit.circuit.library import IQP
import numpy as np

# Create IQP circuit (hard to simulate classically)
num_qubits = 4
interactions = np.random.rand(num_qubits, num_qubits)
iqp_circuit = IQP(interactions)`,

  GROVER_OPERATOR: `from qiskit.circuit.library import GroverOperator
from qiskit import QuantumCircuit

# Define oracle and create Grover operator
oracle = QuantumCircuit(2)
oracle.cz(0, 1)
grover_op = GroverOperator(oracle)`,

  // Arithmetic
  RIPPLE_CARRY_ADDER: `from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Create 3-bit ripple carry adder
num_bits = 3
adder = CDKMRippleCarryAdder(num_bits)

# Setup registers and initialize numbers
reg_a = QuantumRegister(num_bits, "a")
reg_b = QuantumRegister(num_bits, "b")
qc = QuantumCircuit(reg_a, reg_b)
qc.initialize(2, reg_a)  # A=2
qc.initialize(3, reg_b)  # B=3`,

  MULTIPLIER: `from qiskit.circuit.library import HRSCumulativeMultiplier
from qiskit import QuantumCircuit, QuantumRegister

# Create 2-bit multiplier
num_bits = 2
multiplier = HRSCumulativeMultiplier(num_bits)
qc = QuantumCircuit(2*num_bits + 2*num_bits)  # Inputs + result`,

  COMPARATOR: `from qiskit.circuit.library import IntegerComparator

# Create comparator for 3-bit numbers
num_bits = 3
value = 5
comparator = IntegerComparator(num_bits, value, geq=True)`
}

export const TRANSPILER_TEMPLATES = {
  BASIC_TRANSPILER: (optimizationLevel: number, layout: string, routing: string, translation: string, enableScheduling: boolean) => `from qiskit import transpile, Aer, QuantumCircuit

# Define a circuit (placeholder)
qc = QuantumCircuit(5)

# Add some gates
qc.h(0)
qc.cx(0, 1)

# Transpile the circuit with custom options
simulator = Aer.get_backend('qasm_simulator')
transpiled_circuit = transpile(
    qc,
    backend=simulator,
    optimization_level=${optimizationLevel},
    layout_method='${layout}',
    routing_method='${routing}',
    translation_method='${translation}',
    scheduling=${enableScheduling ? 'True' : 'False'}
)`,

  TRANSPILER_PASS: (selectedPass: string) => `from qiskit import transpile, Aer, QuantumCircuit
from qiskit.transpiler.passes import ${selectedPass}
from qiskit.transpiler import PassManager

# Define a circuit (placeholder)
qc = QuantumCircuit(5)

# Add some gates
qc.h(0)
qc.cx(0, 1)

# Create the ${selectedPass} pass
pass_ = ${selectedPass}()

# Create a PassManager and append the pass
pm = PassManager()
pm.append(pass_)

# Run the pass on the circuit
optimized_circuit = pm.run(qc)

# Transpile the circuit for the chosen backend
simulator = Aer.get_backend('qasm_simulator')
transpiled_circuit = transpile(optimized_circuit, simulator)`
}

export const EXECUTION_TEMPLATES = {
  BASIC_EXECUTION: `from qiskit import Aer, execute, QuantumCircuit

# Define a circuit (placeholder)
qc = QuantumCircuit(5)

# Add some gates
qc.h(0)
qc.cx(0, 1)

# Execute the circuit
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1024)
result = job.result()
counts = result.get_counts()`
}

export const RUNTIME_TEMPLATES = {
  ESTIMATOR: `from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliTwoDesign

# Define number of qubits
num_qubits = 30

# Create a circuit
qc = PauliTwoDesign(num_qubits=num_qubits, reps=4, seed=5, insert_barriers=True)

# Define an observable
obs = SparsePauliOp('I' + 'Z' + 'I' * (num_qubits-2))

# Use the Estimator primitive
estimator = Estimator()
job = estimator.run(qc, obs)
result = job.result()`,

  SAMPLER: (loopCount: number) => `from qiskit import Aer, execute
from qiskit.circuit.library import PauliTwoDesign

# Define number of qubits
num_qubits = 30

# Create a circuit
qc = PauliTwoDesign(num_qubits=num_qubits, reps=4, seed=5, insert_barriers=True)

# Execute the circuit
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=${loopCount * 1024})
result = job.result()
counts = result.get_counts()`
}

export const VISUALIZATION_TEMPLATES = {
  HISTOGRAM: `from qiskit import Aer, execute, QuantumCircuit
from qiskit.visualization import plot_histogram

# Create and run a simple circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1024)
result = job.result()
counts = result.get_counts()

# Visualize the results as a histogram
plot_histogram(counts)`,

  BLOCH_SPHERE: `from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector

# Create a simple circuit
qc = QuantumCircuit(1)
qc.h(0)

# Get the statevector
state = Statevector.from_instruction(qc)

# Visualize on the Bloch sphere
plot_bloch_multivector(state)`,

  CIRCUIT_DIAGRAM: `from qiskit import QuantumCircuit

# Create a circuit
qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)

# Draw the circuit
qc.draw(output='mpl')`,

  UNDIRECTED_GRAPH: `from qiskit import Aer, execute, QuantumCircuit
from qiskit.visualization import plot_graph_state

# Create a graph state
qc = QuantumCircuit(5)
for i in range(5):
    qc.h(i)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)
qc.cx(4, 0)

# Visualize as an undirected graph
plot_graph_state(qc)`
}

export const IMPORT_TEMPLATES = {
  BASIC_IMPORTS: `# Import necessary Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, execute
import numpy as np`,

  CONDITIONAL_IMPORTS: (hasQuantumInfo: boolean, hasCircuitLibrary: boolean, hasVisualization: boolean) => {
    const imports = []
    if (hasQuantumInfo) imports.push("from qiskit.quantum_info import SparsePauliOp")
    if (hasCircuitLibrary) imports.push("from qiskit.circuit.library import PauliTwoDesign") 
    if (hasVisualization) imports.push("from qiskit.visualization import plot_histogram")
    return imports.join("\n")
  }
}

export const GENERAL_TEMPLATES = {
  FULL_CIRCUIT: (numQubits: number = 30) => `# Define the number of qubits
num_qubits = ${numQubits}

# Create a quantum circuit
qc = QuantumCircuit(num_qubits)

# Execute the circuit and get counts
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1024)
result = job.result()
counts = result.get_counts()

# Draw the circuit
qc.draw(output='text')`
}

// Multi-node workflow templates
export const MULTI_NODE_TEMPLATES = {
  CIRCUIT_CREATION: {
    PAULI_TWO_DESIGN: (category: string) => `# Create a circuit using the ${category} from the circuit library
qc = PauliTwoDesign(num_qubits=num_qubits, reps=4, seed=5, insert_barriers=True)
parameters = qc.parameters`,

    BASIC_CIRCUIT: `# Create a quantum circuit
qc = QuantumCircuit(num_qubits)`,

    DEFINE_QUBITS: `# Define the number of qubits
num_qubits = 30`
  },

  QUANTUM_INFO_OPS: {
    SPARSE_PAULI_OP: `# Define a Sparse Pauli Operator
obs = SparsePauliOp('I' + 'Z' + 'I' * (num_qubits-2))`
  },

  TRANSPILATION: {
    BASIC: `# Transpile the circuit for the chosen backend
simulator = Aer.get_backend('qasm_simulator')
transpiled_circuit = transpile(qc, simulator)`
  },

  EXECUTION: {
    ESTIMATOR: `# Execute the circuit using the Estimator primitive
from qiskit.primitives import Estimator
estimator = Estimator()
job = estimator.run(transpiled_circuit if 'transpiled_circuit' in locals() else qc, obs)
result = job.result()`,

    SAMPLER: (loopCount: number) => `# Execute the circuit and get counts
job = execute(transpiled_circuit if 'transpiled_circuit' in locals() else qc, simulator, shots=${loopCount * 1024})
result = job.result()
counts = result.get_counts()`,

    DEFAULT: `# Execute the circuit and get counts
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1024)
result = job.result()
counts = result.get_counts()`
  },

  VISUALIZATION: {
    HISTOGRAM: `# Visualize the results as a histogram
plot_histogram(counts)`,

    BLOCH_SPHERE: `# Visualize the state on the Bloch sphere
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
state = Statevector.from_instruction(qc)
plot_bloch_multivector(state)`,

    CIRCUIT_DIAGRAM: `# Draw the circuit
qc.draw(output='mpl')`,

    UNDIRECTED_GRAPH: `# Visualize as an undirected graph
from qiskit.visualization import plot_graph_state
plot_graph_state(counts)`,

    DEFAULT: `# Draw the circuit
qc.draw(output='text')`
  }
}