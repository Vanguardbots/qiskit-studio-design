# API Service Documentation

This document describes the reusable API service that can be used by any component in the Qiskit Studio application for AI-powered code generation and chat functionality.

## Overview

The API service provides a centralized way to interact with the Maestro AI backend for:
- Parameter-based code generation
- Code improvements based on user prompts
- General chat responses via RAG-enhanced chat agent

## Files

- `lib/api-service.ts` - Main API service functions
- `hooks/useAICodeGeneration.ts` - React hook for managing AI code generation state

## API Functions

### 1. generateAICodeForParameterChange

Generates AI-powered code updates when node parameters change. Now includes automatic Qiskit Pattern Step detection.

```typescript
import { generateAICodeForParameterChange } from '@/lib/api-service'

const response = await generateAICodeForParameterChange({
  nodeId: 'runtime-1',
  nodeType: 'runtimeNode',
  currentCode: existingPythonCode,
  parameterName: 'resilience_level',
  newValue: 2,
  nodeLabel: 'Runtime Configuration',
  sessionId: 'param-update-runtime-1',
  // Optional: specify Qiskit Pattern Step (auto-detected if not provided)
  qiskitPatternStep: 'STEP 3', // STEP 1, STEP 2, STEP 3, or STEP 4
  // Optional: additional flags
  preserveStructure: true,
  optimize: false
})

if (response.success) {
  console.log('New code:', response.code)
} else {
  console.error('Error:', response.error)
}
```

#### Qiskit Pattern Step Auto-Detection

The service automatically determines the appropriate Qiskit Pattern Step based on node type:
- **STEP 1 (Mapping)**: Circuit nodes, quantum info nodes, chemistry mapping
- **STEP 2 (Optimize)**: Transpiler nodes, transpiler passes
- **STEP 3 (Execute)**: Runtime nodes, execution nodes
- **STEP 4 (Post-process)**: Visualization nodes

### 2. generateAICodeImprovement

Generates AI-powered code improvements based on user prompts.

```typescript
import { generateAICodeImprovement } from '@/lib/api-service'

const response = await generateAICodeImprovement({
  nodeId: 'circuit-1',
  nodeType: 'circuitNode',
  currentCode: existingPythonCode,
  userPrompt: 'Add error handling and optimize the circuit',
  sessionId: 'improvement-circuit-1'
})

if (response.success) {
  console.log('Improved code:', response.code)
} else {
  console.error('Error:', response.error)
}
```

### 3. generateAIChatResponse

Generates AI chat responses for general queries.

```typescript
import { generateAIChatResponse } from '@/lib/api-service'

const response = await generateAIChatResponse({
  message: 'How do I implement a quantum fourier transform?',
  sessionId: 'user_1'
})

if (response.success) {
  console.log('AI response:', response.message)
} else {
  console.error('Error:', response.error)
}
```

## React Hook

### useAICodeGeneration

A custom hook that manages AI code generation state and provides loading indicators.

```typescript
import { useAICodeGeneration } from '@/hooks/useAICodeGeneration'

function MyComponent() {
  const {
    isGenerating,
    generatingNodeIds,
    lastError,
    generateCodeForParameter,
    generateCodeImprovement,
    setNodeUpdating,
    clearError,
    isNodeUpdating
  } = useAICodeGeneration()

  const handleParameterChange = async (nodeId: string, paramName: string, value: any) => {
    const response = await generateCodeForParameter({
      nodeId,
      nodeType: 'runtimeNode',
      currentCode: currentCode,
      parameterName: paramName,
      newValue: value
    })

    if (response.success) {
      // Update your state with response.code
      updateNodeCode(nodeId, response.code!)
    }
  }

  return (
    <div>
      {isNodeUpdating('node-1') && <span>Updating...</span>}
      {lastError && <div className="error">{lastError}</div>}
      {/* Your component content */}
    </div>
  )
}
```

## Usage Examples

### In Node Components

```typescript
// In a node component (e.g., runtime-node.tsx)
import { useAICodeGeneration } from '@/hooks/useAICodeGeneration'

export const RuntimeNode = memo(({ id, data, isConnectable }: NodeProps<RuntimeNodeData>) => {
  const { generateCodeForParameter, isNodeUpdating } = useAICodeGeneration()

  const handleResilienceChange = async (value: number[]) => {
    const level = value[0]
    
    // Generate Python code immediately
    const optionsString = generateOptionsString(level)
    data.onInputChange?.(id || '', optionsString)
    
    // Trigger AI-powered code enhancement
    const response = await generateCodeForParameter({
      nodeId: id || '',
      nodeType: 'runtimeNode',
      currentCode: data.pythonCode || '',
      parameterName: 'resilience_level',
      newValue: level
    })

    if (response.success) {
      // Code will be updated via the parent component
    }
  }

  return (
    <div>
      {isNodeUpdating(id || '') && <span>Updating...</span>}
      {/* Node content */}
    </div>
  )
})
```

### In Chat Components

```typescript
// In a chat component (e.g., code-panel.tsx)
import { generateAIChatResponse } from '@/lib/api-service'

const handleSendMessage = async (message: string) => {
  const response = await generateAIChatResponse({
    message,
    sessionId: 'user_1'
  })

  if (response.success) {
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response.message
    }])
  } else {
    // Handle error
    console.error('Chat error:', response.error)
  }
}
```

## Configuration

The API service supports multiple Maestro agent endpoints for different operations:

```bash
# Chat Agent endpoint (for general queries with RAG support)
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/chat

# Code Generation Agent endpoint (for parameter updates and code improvements)
NEXT_PUBLIC_PARAMETER_UPDATE_API_URL=http://127.0.0.1:8001/chat

# Code Execution Agent endpoint (for running Python/Qiskit code)
NEXT_PUBLIC_RUNCODE_URL=http://127.0.0.1:8002/run
```

### API Endpoint Usage

- **Chat Responses**: Uses `NEXT_PUBLIC_API_URL` (Chat Agent on port 8000)
- **Parameter Updates**: Uses `NEXT_PUBLIC_PARAMETER_UPDATE_API_URL` (Code Generation Agent on port 8001)
- **Code Improvements**: Uses `NEXT_PUBLIC_PARAMETER_UPDATE_API_URL` (Code Generation Agent on port 8001)
- **Code Execution**: Uses `NEXT_PUBLIC_RUNCODE_URL` (Code Execution Agent on port 8002)

## Error Handling

All API functions return a response object with `success` boolean and either `code`/`message` or `error` properties:

```typescript
interface AICodeGenerationResponse {
  success: boolean
  code?: string
  error?: string
}

interface AIChatResponse {
  success: boolean
  message?: string
  error?: string
}
```

## Default Code Templates

The API service includes default code templates for different node types:
- `runtimeNode` - Runtime configuration with estimator and options
- `transpilerNode` - Transpiler configuration with pass manager
- `circuitNode` - Circuit construction with library imports
- `visualizationNode` - Visualization setup with plot functions
- `quantumInfoNode` - Quantum information objects

## Benefits

1. **Centralized API Logic** - All API calls go through the same service
2. **Consistent Error Handling** - Standardized error responses
3. **Type Safety** - Full TypeScript support with interfaces
4. **Reusability** - Can be used by any component
5. **Loading States** - Built-in loading state management
6. **Default Templates** - Automatic fallback for missing code
7. **Session Management** - Proper session handling for API calls

## Migration Guide

If you have existing components with direct API calls, migrate them to use the new service:

1. Replace direct `fetch()` calls with service functions
2. Update response handling to use the new response format
3. Use the `useAICodeGeneration` hook for loading states
4. Remove duplicate API logic and error handling

This provides a much more maintainable and consistent approach to AI integration across the entire application.

## Utility Functions

### API Configuration Utilities

```typescript
import { 
  isAPIConfigured, 
  isParameterUpdateAPIConfigured, 
  getAPIStatus, 
  getAPIUrl 
} from '@/lib/api-service'

// Check if main API is configured
const isMainAPIReady = isAPIConfigured()

// Check if parameter update API is configured
const isParamAPIReady = isParameterUpdateAPIConfigured()

// Get full API status
const status = getAPIStatus()
console.log('Main API:', status.configured, status.url)
console.log('Parameter API:', status.parameterUpdateConfigured, status.parameterUpdateUrl)

// Get URL for specific operation
const paramUpdateUrl = getAPIUrl('parameter-update')
const chatUrl = getAPIUrl('chat')
const improvementUrl = getAPIUrl('code-improvement')
```

### Environment Variables

Add these to your `.env.local` file:

```bash
# Required: Chat Agent endpoint (RAG-enhanced chat)
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/chat

# Required: Code Generation Agent endpoint (parameter updates and improvements)
NEXT_PUBLIC_PARAMETER_UPDATE_API_URL=http://127.0.0.1:8001/chat

# Required: Code Execution Agent endpoint (Python/Qiskit code execution)
NEXT_PUBLIC_RUNCODE_URL=http://127.0.0.1:8002/run

# Debug mode
NEXT_PUBLIC_DEBUG=false
```

All three Maestro agents should be running for full functionality. See [api/README.md](../api/README.md) for setup instructions.

## Query Format for Parameter Updates

When you change a parameter in any node, the API service sends a structured query to the Parameter Update API endpoint:

### Example Query Structure

```
Original Code Snippet:
```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1

options = {
    "resilience_level": 1,
    "optimization_level": 3
}
```

Qiskit Pattern Step: STEP 3

Parameters:
- resilience_level: 2

Target Specifications:
Update the code to reflect the new parameter value while maintaining functionality and following Qiskit best practices.
```

### Qiskit Pattern Step Mapping

The service automatically determines the correct Qiskit Pattern Step:

| Node Type | Parameters | Pattern Step | Focus |
|-----------|------------|--------------|-------|
| `circuitNode` | circuit_type, num_qubits | STEP 1 | Problem mapping, circuit structure |
| `transpilerNode` | optimization_level, layout_method | STEP 2 | Circuit optimization, transpilation |
| `runtimeNode` | resilience_level, shots, error mitigation | STEP 3 | Execution, backend configuration |
| `visualizationNode` | visualization_type, plot_type | STEP 4 | Result processing, visualization |

### Response Format

The Code Generation Agent returns only the updated Qiskit Python code:

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 2

options = {
    "resilience_level": 2,
    "optimization_level": 3,
    "resilience": {
        "measure_mitigation": True,
        "zne_mitigation": True,
        "gate_twirling": True
    }
}
```