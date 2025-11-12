/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Example usage and testing of the API service with the new parameter update endpoint
 * This is an example file showing how to use and test the API service configuration
 */

import { 
  generateAICodeForParameterChange, 
  generateAIChatResponse,
  getAPIStatus,
  getAPIUrl,
  isParameterUpdateAPIConfigured 
} from './api-service'

// Example: Check API configuration
export function testAPIConfiguration() {
  const status = getAPIStatus()
  
  console.log('API Configuration Status:')
  console.log('- Main API configured:', status.configured)
  console.log('- Main API URL:', status.url)
  console.log('- Parameter Update API configured:', status.parameterUpdateConfigured)
  console.log('- Parameter Update URL:', status.parameterUpdateUrl)
  
  return status
}

// Example: Test parameter update with new endpoint
export async function testParameterUpdate() {
  const response = await generateAICodeForParameterChange({
    nodeId: 'runtime-1',
    nodeType: 'runtimeNode',
    currentCode: `# Runtime Configuration
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1

options = {
    "resilience_level": 1,
    "optimization_level": 3
}`,
    parameterName: 'resilience_level',
    newValue: 2,
    nodeLabel: 'Runtime Configuration',
    sessionId: 'test-param-update'
  })

  console.log('Parameter Update Test Result:')
  console.log('- Success:', response.success)
  console.log('- Error:', response.error)
  console.log('- Code Length:', response.code?.length || 0)
  
  return response
}

// Example: Test which endpoint is being used
export function testEndpointSelection() {
  const paramUpdateUrl = getAPIUrl('parameter-update')
  const chatUrl = getAPIUrl('chat')
  const improvementUrl = getAPIUrl('code-improvement')
  
  console.log('Endpoint Selection:')
  console.log('- Parameter Updates will use:', paramUpdateUrl)
  console.log('- Chat will use:', chatUrl)
  console.log('- Code Improvements will use:', improvementUrl)
  
  const usingDedicatedEndpoint = isParameterUpdateAPIConfigured()
  console.log('- Using dedicated parameter endpoint:', usingDedicatedEndpoint)
  
  return {
    paramUpdateUrl,
    chatUrl,
    improvementUrl,
    usingDedicatedEndpoint
  }
}

// Example: Test both endpoints work correctly
export async function testBothEndpoints() {
  console.log('Testing both API endpoints...')
  
  // Test parameter update (uses new endpoint)
  console.log('1. Testing parameter update endpoint...')
  const paramResult = await testParameterUpdate()
  
  // Test chat (uses main endpoint)
  console.log('2. Testing chat endpoint...')
  const chatResult = await generateAIChatResponse({
    message: 'What is quantum computing?',
    sessionId: 'test-chat'
  })
  
  console.log('Chat Test Result:')
  console.log('- Success:', chatResult.success)
  console.log('- Error:', chatResult.error)
  console.log('- Message Length:', chatResult.message?.length || 0)
  
  return {
    parameterUpdate: paramResult,
    chat: chatResult
  }
}

// Example usage in a React component
export const ExampleUsage = `
// In your component
import { useAICodeGeneration } from '@/hooks/useAICodeGeneration'
import { getAPIStatus } from '@/lib/api-service'

function MyComponent() {
  const { generateCodeForParameter, isNodeUpdating } = useAICodeGeneration()
  
  // Check API configuration on mount
  useEffect(() => {
    const status = getAPIStatus()
    if (status.parameterUpdateConfigured) {
      console.log('Using dedicated parameter update endpoint:', status.parameterUpdateUrl)
    } else {
      console.log('Using main API endpoint for parameter updates:', status.url)
    }
  }, [])
  
  const handleParameterChange = async (nodeId: string, param: string, value: any) => {
    // This will automatically use the correct endpoint
    const response = await generateCodeForParameter({
      nodeId,
      nodeType: 'runtimeNode',
      currentCode: currentCode,
      parameterName: param,
      newValue: value
    })
    
    if (response.success) {
      // Update your state with the new code
      updateCode(response.code!)
    }
  }
  
  return (
    <div>
      {isNodeUpdating('node-1') && <span>Updating with new endpoint...</span>}
      {/* Your component */}
    </div>
  )
}
`