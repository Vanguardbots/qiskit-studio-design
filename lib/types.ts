/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

export interface NodeItem {
  id: string
  name: string
  data: any
}

export interface NodeCategory {
  id: string
  name: string
  items: NodeItem[]
}

export interface CircuitData {
  nodes: any[]
  edges: any[]
}

export interface QiskitCodeOptions {
  includeImports: boolean
  includeVisualization: boolean
}
