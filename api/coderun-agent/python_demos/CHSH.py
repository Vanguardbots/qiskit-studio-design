# Copyright contributors to the Qiskit Studio project
# SPDX-License-Identifier: Apache-2.0

## STEP 0 : IBM Quantum Config
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print(f"Using IBM backend: {backend.name}")


## STEP 1 : Mapping the problem

###[Bell State Circuit]
import numpy as np

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp


theta = Parameter("$\\theta$")

chsh_circuit = QuantumCircuit(2)
chsh_circuit.h(0)
chsh_circuit.cx(0, 1)
chsh_circuit.ry(theta, 0)

number_of_phases = 21
phases = np.linspace(0, 2 * np.pi, number_of_phases)
# Phases need to be expressed as list of lists in order to work
individual_phases = [[ph] for ph in phases]

###[CHSH Observables]
# <CHSH1> = <AB> - <Ab> + <aB> + <ab> -> <ZZ> - <ZX> + <XZ> + <XX>
observable1 = SparsePauliOp.from_list([("ZZ", 1), ("ZX", -1), ("XZ", 1), ("XX", 1)])

# <CHSH2> = <AB> + <Ab> - <aB> + <ab> -> <ZZ> + <ZX> - <XZ> + <XX>
observable2 = SparsePauliOp.from_list([("ZZ", 1), ("ZX", 1), ("XZ", -1), ("XX", 1)])

## STEP 2 : Optimize Circuit
###[Transpiler]
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)

chsh_isa_circuit = pm.run(chsh_circuit)

isa_observable1 = observable1.apply_layout(layout=chsh_isa_circuit.layout)
isa_observable2 = observable2.apply_layout(layout=chsh_isa_circuit.layout)

## STEP 3 : Execute
###[Estimator]
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)

# Set resilience level to 1
estimator.options.resilience_level = 1

pub = (
    chsh_isa_circuit,  # ISA circuit
    [[isa_observable1], [isa_observable2]],  # ISA Observables
    individual_phases,  # Parameter values
)

###[Exectute Job]
job_result = estimator.run(pubs=[pub]).result()

## STEP 4 : Post-process
###[RAW]
chsh1_est = job_result[0].data.evs[0]
chsh2_est = job_result[0].data.evs[1]

output_plot = {"CHSH1": chsh1_est.tolist(), "CHSH2": chsh2_est.tolist()}

import json

print(f'RESULT: {json.dumps({"type":"plot","content":output_plot})}')
