/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

// Define the mapping from demo IDs to Python files
const DEMO_PYTHON_FILES: Record<string, string> = {
  'chemistry-simulation': 'chemistry-SQD.py',
  'max-cut': 'MAX-CUT.py',
  'chsh-inequality': 'CHSH.py',
};

/**
 * Load Python code for a specific demo via API
 * @param demoId - The ID of the demo to load Python code for
 * @returns A promise that resolves to the Python code as a string, or null if not found
 */
export async function loadDemoPythonCode(demoId: string): Promise<string | null> {
  const fileName = DEMO_PYTHON_FILES[demoId];
  if (!fileName) {
    return null;
  }

  try {
    const response = await fetch(`/api/demo-python/${demoId}`);
    if (!response.ok) {
      console.error(`Failed to load Python file for demo ${demoId}: ${response.status}`);
      return null;
    }
    
    const data = await response.json();
    return data.code;
  } catch (error) {
    console.error(`Failed to load Python file for demo ${demoId}:`, error);
    return null;
  }
}

/**
 * Check if a demo has an associated Python file
 * @param demoId - The ID of the demo to check
 * @returns True if the demo has an associated Python file
 */
export function hasDemoPythonCode(demoId: string): boolean {
  return demoId in DEMO_PYTHON_FILES;
}

/**
 * Get all available demo Python file mappings
 * @returns Object mapping demo IDs to Python file names
 */
export function getDemoPythonFiles(): Record<string, string> {
  return { ...DEMO_PYTHON_FILES };
}