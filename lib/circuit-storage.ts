/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

import type { CircuitData } from "./types"

// Save circuit to localStorage
export function saveCircuit(name: string, circuitData: CircuitData): void {
  try {
    const circuits = getSavedCircuits()
    circuits[name] = circuitData
    localStorage.setItem("quantum-circuits", JSON.stringify(circuits))
  } catch (error) {
    console.error("Error saving circuit:", error)
  }
}

// Load circuit from localStorage
export function loadCircuit(name: string): CircuitData | null {
  try {
    const circuits = getSavedCircuits()
    return circuits[name] || null
  } catch (error) {
    console.error("Error loading circuit:", error)
    return null
  }
}

// Get all saved circuits
export function getSavedCircuits(): Record<string, CircuitData> {
  try {
    const circuitsJson = localStorage.getItem("quantum-circuits")
    return circuitsJson ? JSON.parse(circuitsJson) : {}
  } catch (error) {
    console.error("Error getting saved circuits:", error)
    return {}
  }
}

// Delete a saved circuit
export function deleteCircuit(name: string): void {
  try {
    const circuits = getSavedCircuits()
    delete circuits[name]
    localStorage.setItem("quantum-circuits", JSON.stringify(circuits))
  } catch (error) {
    console.error("Error deleting circuit:", error)
  }
}

// Generate a shareable URL for the circuit
export function generateShareableUrl(circuitData: CircuitData): string {
  try {
    const compressedData = btoa(JSON.stringify(circuitData))
    return `${window.location.origin}?circuit=${encodeURIComponent(compressedData)}`
  } catch (error) {
    console.error("Error generating shareable URL:", error)
    return window.location.origin
  }
}

// Load circuit from URL parameter
export function loadCircuitFromUrl(): CircuitData | null {
  try {
    const urlParams = new URLSearchParams(window.location.search)
    const circuitParam = urlParams.get("circuit")

    if (circuitParam) {
      const decompressedData = JSON.parse(atob(decodeURIComponent(circuitParam)))
      return decompressedData
    }

    return null
  } catch (error) {
    console.error("Error loading circuit from URL:", error)
    return null
  }
}
