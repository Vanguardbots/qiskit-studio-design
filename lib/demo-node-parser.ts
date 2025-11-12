/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

export interface ParsedNode {
  id: string;
  title: string;
  pythonCode: string;
  inputCode?: string;
  step: number;
  category: string;
  position: { x: number; y: number };
}

export interface ParsedDemo {
  nodes: ParsedNode[];
  step0Config?: string;
}

export function parseDemoNodes(pythonCode: string, demoId: string): ParsedDemo {
  const lines = pythonCode.split('\n');
  const nodes: ParsedNode[] = [];
  let currentStep = 0;
  let step0Config = '';
  
  // Extract STEP 0 config
  const step0Match = pythonCode.match(/## STEP 0 : IBM Quantum Config[\s\S]*?(?=\n##|$)/);
  if (step0Match) {
    step0Config = step0Match[0];
  }
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Track current step
    const stepMatch = line.match(/^## STEP (\d+)/);
    if (stepMatch) {
      currentStep = parseInt(stepMatch[1]);
      continue;
    }
    
    // Find node markers ###[NodeTitle]
    const nodeMatch = line.match(/^###\[(.+)\]$/);
    if (nodeMatch) {
      const title = nodeMatch[1];
      const nodeId = `${demoId}-${title.toLowerCase().replace(/\s+/g, '-')}`;
      
      // Extract Python code for this node (from ###[title] to next ###[ or ##)
      let pythonCode = '';
      let inputCode = '';
      let j = i + 1;
      let insideInputSection = false;
      
      while (j < lines.length) {
        const nextLine = lines[j];
        
        // Stop at next node or step
        if (nextLine.match(/^###\[/) || nextLine.match(/^## STEP/)) {
          break;
        }
        
        // Check for INPUT PYTHON sections
        if (nextLine.includes('#### INPUT PYTHON') || nextLine.includes('##### INPUT PYTHON')) {
          insideInputSection = true;
          j++;
          continue;
        }
        
        if (nextLine.includes('#### END INPUT PYTHON') || nextLine.includes('###### END INPUT PYTHON')) {
          insideInputSection = false;
          j++;
          continue;
        }
        
        // Collect input code separately
        if (insideInputSection) {
          inputCode += nextLine + '\n';
        }
        
        // Collect all Python code for this node
        pythonCode += nextLine + '\n';
        j++;
      }
      
      // Determine category based on step and title
      let category = 'general';
      if (currentStep === 1) {
        // Special case for Graph to Hamiltonian - use Python node
        if (title.toLowerCase().includes('graph to hamiltonian')) {
          category = 'Python';
        } else {
          category = title.toLowerCase().includes('mapping') ? 'Molecular System' : 
                    title.toLowerCase().includes('hamiltonian') ? 'Hamiltonian' :
                    title.toLowerCase().includes('circuit') ? 'Ansatz' : 'Map';
        }
      } else if (currentStep === 2) {
        category = 'Optimize';
      } else if (currentStep === 3) {
        category = title.toLowerCase().includes('estimator') ? 'Estimator' : 
                  title.toLowerCase().includes('sampler') ? 'Sampler' : 'Execute';
      } else if (currentStep === 4) {
        category = 'Post-process';
      }
      
      // Calculate position based on step and index
      const stepNodes = nodes.filter(n => n.step === currentStep).length;
      const baseX = 100 + (currentStep * 300);
      const baseY = 100 + (stepNodes * 200);
      
      nodes.push({
        id: nodeId,
        title,
        pythonCode: pythonCode.trim(),
        inputCode: inputCode.trim() || undefined,
        step: currentStep,
        category,
        position: { x: baseX, y: baseY }
      });
    }
  }
  
  return { nodes, step0Config };
}

export function convertToReactFlowNodes(parsedNodes: ParsedNode[]) {
  return parsedNodes.map(node => ({
    id: node.id,
    type: getNodeType(node.category),
    data: {
      label: node.title,
      category: node.category,
      pythonCode: node.pythonCode,
      inputCode: node.inputCode,
      step: node.step
    },
    position: node.position
  }));
}

function getNodeType(category: string): string {
  const categoryMap: { [key: string]: string } = {
    'Molecular System': 'chemistryNode',
    'Hamiltonian': 'quantumInfoNode',
    'Ansatz': 'circuitLibraryNode',
    'Map': 'quantumInfoNode',
    'Python': 'pythonNode',
    'Optimize': 'transpilerNode',
    'Estimator': 'runtimeNode',
    'Sampler': 'runtimeNode',
    'Execute': 'executionNode',
    'Post-process': 'visualizationNode'
  };
  
  return categoryMap[category] || 'quantumInfoNode';
}