/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

export interface CodeSection {
  step: number;
  title: string;
  startLine: number;
  endLine: number;
  content: string;
  nodeMarker?: string; // For ###[NodeName] markers
}

export interface ParsedCode {
  fullCode: string;
  sections: CodeSection[];
}

/**
 * Check if a line contains actual code content (not empty, comment, or just whitespace)
 */
function isCodeLine(line: string): boolean {
  const trimmed = line.trim();
  return trimmed.length > 0 && !trimmed.startsWith('#') && !trimmed.startsWith('"""') && !trimmed.startsWith("'''");
}

/**
 * Find the first line with actual code content after a step header
 */
function findCodeStart(lines: string[], headerIndex: number, nodeMarker?: string): number {
  // Start from the marker line itself
  return headerIndex;
}

/**
 * Find the last line with actual code content before the next step header
 */
function findCodeEnd(lines: string[], startIndex: number, nextHeaderIndex: number, nodeMarker?: string): number {
  // End right before the next marker, or at end of file if no next marker
  return nextHeaderIndex >= 0 ? nextHeaderIndex - 1 : lines.length - 1;
}

/**
 * Parse Python code into sections based on both step and node markers
 * @param pythonCode - The full Python code as a string
 * @returns Parsed code with sections identified
 */
export function parsePythonCodeSections(pythonCode: string): ParsedCode {
  const lines = pythonCode.split('\n');
  const sections: CodeSection[] = [];
  
  // Regex patterns
  const stepPattern = /^## STEP (\d+) : (.+)$/;
  const nodePattern = /^###\[(.+)\]$/;
  
  // Find all markers (steps and nodes)
  const markers: { 
    index: number; 
    type: 'step' | 'node'; 
    step?: number; 
    title?: string; 
    nodeMarker?: string;
  }[] = [];
  
  let currentStep = 0;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Check for step markers
    const stepMatch = line.match(stepPattern);
    if (stepMatch) {
      currentStep = parseInt(stepMatch[1]);
      markers.push({
        index: i,
        type: 'step',
        step: currentStep,
        title: stepMatch[2].trim()
      });
      continue;
    }
    
    // Check for node markers
    const nodeMatch = line.match(nodePattern);
    if (nodeMatch) {
      markers.push({
        index: i,
        type: 'node',
        step: currentStep,
        nodeMarker: nodeMatch[1].trim()
      });
    }
  }
  
  // Process each node marker to create sections
  for (let j = 0; j < markers.length; j++) {
    const marker = markers[j];
    
    // Only process node markers
    if (marker.type !== 'node') continue;
    
    const nextMarker = markers[j + 1];
    
    // Find actual code boundaries
    const codeStartLine = findCodeStart(lines, marker.index, marker.nodeMarker);
    const codeEndLine = findCodeEnd(lines, codeStartLine, nextMarker ? nextMarker.index : -1, marker.nodeMarker);
    
    const section: CodeSection = {
      step: marker.step!,
      title: marker.nodeMarker!,
      startLine: codeStartLine,
      endLine: codeEndLine,
      content: lines.slice(codeStartLine, codeEndLine + 1).join('\n'),
      nodeMarker: marker.nodeMarker
    };
    
    sections.push(section);
  }
  
  return {
    fullCode: pythonCode,
    sections,
  };
}

/**
 * Get section content for highlighting by step
 * @param parsedCode - Parsed code structure
 * @param step - Step number (1-4)
 * @returns Section content with line numbers for highlighting
 */
export function getSectionForHighlighting(
  parsedCode: ParsedCode,
  step: number
): { content: string; startLine: number; endLine: number } | null {
  const section = parsedCode.sections.find(s => s.step === step);
  if (!section) {
    return null;
  }
  
  return {
    content: section.content,
    startLine: section.startLine,
    endLine: section.endLine,
  };
}

/**
 * Get section content for highlighting by node marker
 * @param parsedCode - Parsed code structure
 * @param nodeMarker - Node marker like "Chemistry", "UVJ Circuit", etc.
 * @returns Section content with line numbers for highlighting
 */
export function getSectionForHighlightingByNode(
  parsedCode: ParsedCode,
  nodeMarker: string
): { content: string; startLine: number; endLine: number } | null {
  const section = parsedCode.sections.find(s => s.nodeMarker === nodeMarker);
  if (!section) {
    return null;
  }
  
  return {
    content: section.content,
    startLine: section.startLine,
    endLine: section.endLine,
  };
}

/**
 * Map node types to their specific node markers for all demos
 * @param nodeType - The type of the node
 * @param nodeCategory - The category of the node
 * @param nodeLabel - The label of the node
 * @returns Node marker string or null if no mapping found
 */
export function mapNodeToMarker(
  nodeType: string,
  nodeCategory?: string,
  nodeLabel?: string
): string | null {
  // STEP 1: Mapping the problem nodes
  if (nodeType === 'quantumInfoNode') {
    if (nodeCategory === 'Bell State Circuit') return 'Bell State Circuit';
    if (nodeCategory === 'Hamiltonian') return 'Graph to Hamiltonian';
    return nodeCategory || 'Quantum Info';
  }
  
  if (nodeType === 'pythonNode') {
    if (nodeLabel === 'Graph to Hamiltonian') return 'Graph to Hamiltonian';
    return 'Python Code';
  }
  
  if (nodeType === 'circuitLibraryNode') {
    if (nodeLabel === 'UCJ Circuit') return 'UCJ Circuit';
    if (nodeLabel === 'Bell State Circuit') return 'Bell State Circuit';
    if (nodeLabel === 'QAOA Circuit') return 'QAOA Circuit';
    return 'Circuit Library';
  }
  
  if (nodeType === 'chemistryNode') {
    return 'Chemistry';
  }
  
  if (nodeType === 'chemistryMapNode') {
    return 'UCJ Circuit';
  }
  
  // For nodes with observables/Hamiltonian
  if (nodeCategory === 'CHSH Observables') {
    return 'CHSH Observables';
  }
  
  // STEP 2: Optimize Circuit nodes
  if (nodeType === 'transpilerNode') {
    return 'Transpiler';
  }
  
  // STEP 3: Execute nodes
  if (nodeType === 'executionNode') {
    if (nodeLabel === 'Hardware Execution') return 'Hardware Execution';
    if (nodeLabel === 'Execute Job') return 'Exectute Job'; // Note: matches the typo in the code marker
    return 'Execution';
  }
  
  if (nodeType === 'runtimeNode') {
    if (nodeCategory === 'Estimator') {
      // Check if it's uppercase version in MAX-CUT demo
      return nodeLabel === 'ESTIMATOR' ? 'ESTIMATOR' : 'Estimator';
    }
    if (nodeCategory === 'Sampler') {
      // Check if it's uppercase version in MAX-CUT demo  
      return nodeLabel === 'SAMPLER' ? 'SAMPLER' : 'Sampler';
    }
    return 'Hardware Execution';
  }
  
  // STEP 4: Post-process nodes
  if (nodeType === 'postProcessNode') {
    if (nodeLabel === 'SQD Post-process') return 'SQD Post-process';
    return 'Post Process';
  }
  
  if (nodeType === 'visualizationNode') {
    if (nodeLabel === 'Output') return 'Output Node';
    return 'Visualization';
  }
  
  // Output nodes (fallback)
  if (nodeType === 'outputNode') {
    return 'Output Node';
  }
  
  return null;
}

/**
 * Map node type and category to appropriate step number
 * @param nodeType - The type of the node (e.g., 'quantumInfoNode')
 * @param nodeCategory - The category of the node (e.g., 'Hamiltonian')
 * @param nodeLabel - The label of the node (e.g., 'Quantum info library')
 * @returns Step number (1-4) or null if no mapping found
 */
export function mapNodeToStep(
  nodeType: string,
  nodeCategory?: string,
  nodeLabel?: string
): number | null {
  // STEP 1: Mapping the problem
  if (nodeType === 'quantumInfoNode') {
    return 1;
  }
  if (nodeType === 'circuitLibraryNode') {
    return 1;
  }
  if (nodeType === 'chemistryNode' || nodeType === 'chemistryMapNode') {
    return 1;
  }
  if (nodeType === 'pythonNode') {
    return 1;
  }
  
  // STEP 2: Optimize Circuit
  if (nodeType === 'transpilerNode') {
    return 2;
  }
  
  // STEP 3: Execute
  if (nodeType === 'executionNode') {
    return 3;
  }
  if (nodeType === 'runtimeNode') {
    return 3;
  }
  
  // STEP 4: Post-process
  if (nodeType === 'visualizationNode') {
    return 4;
  }
  
  return null;
}

/**
 * Get highlighted code for a specific node
 * @param pythonCode - The full Python code
 * @param nodeType - The type of the clicked node
 * @param nodeCategory - The category of the clicked node
 * @param nodeLabel - The label of the clicked node
 * @returns Object with full code and highlighting information
 */
export function getHighlightedCodeForNode(
  pythonCode: string,
  nodeType: string,
  nodeCategory?: string,
  nodeLabel?: string
): {
  code: string;
  highlightSection?: { startLine: number; endLine: number; step: number };
} {
  const parsedCode = parsePythonCodeSections(pythonCode);
  
  // First, try to find a specific node marker for any demo
  const nodeMarker = mapNodeToMarker(nodeType, nodeCategory, nodeLabel);
  if (nodeMarker) {
    const section = getSectionForHighlightingByNode(parsedCode, nodeMarker);
    if (section) {
      return {
        code: pythonCode,
        highlightSection: {
          startLine: section.startLine,
          endLine: section.endLine,
          step: mapNodeToStep(nodeType, nodeCategory, nodeLabel) || 1,
        },
      };
    }
  }
  
  // Fallback to step-based highlighting if no specific node marker found
  const step = mapNodeToStep(nodeType, nodeCategory, nodeLabel);
  
  if (!step) {
    return { code: pythonCode };
  }
  
  const section = getSectionForHighlighting(parsedCode, step);
  
  if (!section) {
    return { code: pythonCode };
  }
  
  return {
    code: pythonCode,
    highlightSection: {
      startLine: section.startLine,
      endLine: section.endLine,
      step,
    },
  };
}