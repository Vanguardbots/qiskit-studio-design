/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

import type { Node, Edge } from "reactflow"
import type { QiskitCodeOptions } from "./types"
import { 
  QUANTUM_INFO_TEMPLATES, 
  CIRCUIT_LIBRARY_TEMPLATES, 
  TRANSPILER_TEMPLATES, 
  EXECUTION_TEMPLATES, 
  RUNTIME_TEMPLATES, 
  VISUALIZATION_TEMPLATES, 
  IMPORT_TEMPLATES, 
  GENERAL_TEMPLATES,
  MULTI_NODE_TEMPLATES
} from "./python-templates"

export function generateQiskitCode(
  nodes: Node[],
  edges: Edge[],
  options: QiskitCodeOptions = { includeImports: true, includeVisualization: true },
): string {
  // Start with imports
  let code = ""

  if (options.includeImports) {
    // Use templates from python-templates.ts
    code += IMPORT_TEMPLATES.BASIC_IMPORTS + "\n"

    // Check if we have specific node types to determine imports
    const hasQuantumInfo = nodes.some((node) => node.type === "quantumInfoNode")
    const hasCircuitLibrary = nodes.some((node) => node.type === "circuitLibraryNode")
    const hasVisualization = nodes.some((node) => node.type === "visualizationNode")

    const conditionalImports = IMPORT_TEMPLATES.CONDITIONAL_IMPORTS(hasQuantumInfo, hasCircuitLibrary, hasVisualization)
    if (conditionalImports) {
      code += conditionalImports + "\n"
    }

    code += "\n"
  }

  // Generate code based on node types
  if (nodes.length === 1) {
    // Single node selected - generate specific code for that node
    const node = nodes[0]

    switch (node.type) {
      case "quantumInfoNode":
        code += generateQuantumInfoCode(node)
        break
      case "circuitLibraryNode":
        code += generateCircuitLibraryCode(node)
        break
      case "transpilerNode":
        code += generateTranspilerCode(node)
        break
      case "transpilerPassNode":
        code += generateTranspilerPassCode(node)
        break
      case "executionNode":
        code += generateExecutionCode()
        break
      case "runtimeNode":
        code += generateRuntimeCode(node)
        break
      case "visualizationNode":
        code += generateVisualizationCode(node)
        break
      default:
        code += "# No specific code for this node type\n"
    }
  } else {
    // Multiple nodes - generate full circuit code
    code += MULTI_NODE_TEMPLATES.CIRCUIT_CREATION.DEFINE_QUBITS + "\n\n"

    // Check for circuit library nodes
    const circuitNodes = nodes.filter((node) => node.type === "circuitLibraryNode")
    if (circuitNodes.length > 0) {
      const circuitNode = circuitNodes[0]
      const category = circuitNode.data.category

      if (category === "PauliTwoDesign" || category === "Ansatz") {
        code += MULTI_NODE_TEMPLATES.CIRCUIT_CREATION.PAULI_TWO_DESIGN(category) + "\n\n"
      } else {
        code += MULTI_NODE_TEMPLATES.CIRCUIT_CREATION.BASIC_CIRCUIT + "\n\n"
      }
    } else {
      // Default circuit creation
      code += MULTI_NODE_TEMPLATES.CIRCUIT_CREATION.BASIC_CIRCUIT + "\n\n"
    }

    // Add quantum info operations if present
    const quantumInfoNodes = nodes.filter((node) => node.type === "quantumInfoNode")
    if (quantumInfoNodes.length > 0) {
      const quantumInfoNode = quantumInfoNodes[0]
      const category = quantumInfoNode.data.category

      if (category === "SparsePauliOp" || category === "Hamiltonian") {
        code += MULTI_NODE_TEMPLATES.QUANTUM_INFO_OPS.SPARSE_PAULI_OP + "\n\n"
      }
    }

    // Add transpilation if there's a transpiler node
    const hasTranspiler = nodes.some((node) => node.type === "transpilerNode")
    if (hasTranspiler) {
      code += MULTI_NODE_TEMPLATES.TRANSPILATION.BASIC + "\n\n"
    }

    // Add execution if there's a runtime node
    const runtimeNodes = nodes.filter((node) => node.type === "runtimeNode")
    if (runtimeNodes.length > 0) {
      const runtimeNode = runtimeNodes[0]
      const category = runtimeNode.data.category
      const loopCount = runtimeNode.data.loopCount || 10

      if (category === "Estimator") {
        code += MULTI_NODE_TEMPLATES.EXECUTION.ESTIMATOR + "\n\n"
      } else {
        code += MULTI_NODE_TEMPLATES.EXECUTION.SAMPLER(loopCount) + "\n\n"
      }
    } else {
      // Default execution
      code += MULTI_NODE_TEMPLATES.EXECUTION.DEFAULT + "\n\n"
    }

    // Add visualization if there's a visualization node
    const visualizationNodes = nodes.filter((node) => node.type === "visualizationNode")
    if (visualizationNodes.length > 0 && options.includeVisualization) {
      const visualizationNode = visualizationNodes[0]
      const category = visualizationNode.data.category

      if (category === "Histogram") {
        code += MULTI_NODE_TEMPLATES.VISUALIZATION.HISTOGRAM
      } else if (category === "Bloch Sphere") {
        code += MULTI_NODE_TEMPLATES.VISUALIZATION.BLOCH_SPHERE
      } else if (category === "Circuit Diagram") {
        code += MULTI_NODE_TEMPLATES.VISUALIZATION.CIRCUIT_DIAGRAM
      } else if (category === "Undirected Graph") {
        code += MULTI_NODE_TEMPLATES.VISUALIZATION.UNDIRECTED_GRAPH
      }
    } else if (options.includeVisualization) {
      code += MULTI_NODE_TEMPLATES.VISUALIZATION.DEFAULT
    }
  }

  return code
}

function generateQuantumInfoCode(node: Node): string {
  const category = node.data.category
  let code = "# Quantum Info Library Code\n"

  if (category === "Hamiltonian") {
    code += QUANTUM_INFO_TEMPLATES.HAMILTONIAN
  } else if (category === "Pauli" || category === "SparsePauliOp") {
    code += QUANTUM_INFO_TEMPLATES.SPARSE_PAULI_OP
  }

  return code
}

function generateCircuitLibraryCode(node: Node): string {
  const category = node.data.category
  let code = "# Circuit Library Code\n"

  if (category === "Ansatz" || category === "PauliTwoDesign") {
    code += CIRCUIT_LIBRARY_TEMPLATES.PAULI_TWO_DESIGN
  } else {
    code += CIRCUIT_LIBRARY_TEMPLATES.BASIC_CIRCUIT
  }

  return code
}

function generateTranspilerCode(node: Node): string {
  // Extract transpiler options from node data
  const optimizationLevel = node.data.optimizationLevel || 1
  const layout = node.data.layout || "sabre"
  const routing = node.data.routing || "stochastic"
  const translation = node.data.translation || "translator"
  const enableScheduling = node.data.enableScheduling || false

  let code = "# Transpiler Code\n"
  code += TRANSPILER_TEMPLATES.BASIC_TRANSPILER(optimizationLevel, layout, routing, translation, enableScheduling)

  return code
}

function generateExecutionCode(): string {
  let code = "# Execution Code\n"
  code += EXECUTION_TEMPLATES.BASIC_EXECUTION

  return code
}

function generateRuntimeCode(node: Node): string {
  const category = node.data.category
  const loopCount = node.data.loopCount || 10
  let code = "# Runtime Primitives Code\n"

  if (category === "Estimator") {
    code += RUNTIME_TEMPLATES.ESTIMATOR
  } else if (category === "Sampler") {
    code += RUNTIME_TEMPLATES.SAMPLER(loopCount)
  }

  return code
}

function generateVisualizationCode(node: Node): string {
  const category = node.data.category
  let code = "# Visualization Code\n"

  if (category === "Histogram") {
    code += VISUALIZATION_TEMPLATES.HISTOGRAM
  } else if (category === "Bloch Sphere") {
    code += VISUALIZATION_TEMPLATES.BLOCH_SPHERE
  } else if (category === "Circuit Diagram") {
    code += VISUALIZATION_TEMPLATES.CIRCUIT_DIAGRAM
  } else if (category === "Undirected Graph") {
    code += VISUALIZATION_TEMPLATES.UNDIRECTED_GRAPH
  }

  return code
}

// Add a new function to generate code for the TranspilerPassNode
function generateTranspilerPassCode(node: Node): string {
  const selectedPass = node.data.selectedPass || "Optimize1qGates"
  let code = "# Transpiler Pass Code\n"
  code += TRANSPILER_TEMPLATES.TRANSPILER_PASS(selectedPass)

  return code
}
