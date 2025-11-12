/**
 * Copyright contributors to the Qiskit Studio project
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Browser console utilities for debugging
 * These functions will be available in the browser console for easy debug control
 */

import { setDebugMode, getDebugMode } from './debug';

// Make debug utilities available in browser console
if (typeof window !== 'undefined') {
  (window as any).QiskitStudioDebug = {
    // Enable debug logging
    enable: () => {
      setDebugMode(true);
      console.log('🔍 Qiskit Studio Debug Mode ENABLED');
      console.log('💡 Available categories: API, COMPOSER, NODES, PYTHON_CODE, ALL');
    },
    
    // Disable debug logging
    disable: () => {
      setDebugMode(false);
      console.log('🔍 Qiskit Studio Debug Mode DISABLED');
    },
    
    // Check current debug status
    status: () => {
      const enabled = getDebugMode();
      console.log(`🔍 Debug Mode: ${enabled ? 'ENABLED' : 'DISABLED'}`);
      return enabled;
    },
    
    // Show help
    help: () => {
      console.log(`
🔍 Qiskit Studio Debug Utilities
================================

Available commands:
• QiskitStudioDebug.enable()  - Enable debug logging
• QiskitStudioDebug.disable() - Disable debug logging  
• QiskitStudioDebug.status()  - Check debug status
• QiskitStudioDebug.help()    - Show this help

Debug Categories:
• API          - API calls and responses
• COMPOSER     - Quantum composer operations
• NODES        - Node component operations
• PYTHON_CODE  - Python code loading and updates
• ALL          - All debug categories

Environment Variable:
Set NEXT_PUBLIC_DEBUG=true in .env.local for persistent debug mode

Browser Storage:
Debug mode is stored in localStorage as 'qiskit-studio-debug'
      `);
    }
  };

  // Show available debug utilities on page load
  console.log('🔍 Qiskit Studio Debug Utilities loaded. Type QiskitStudioDebug.help() for commands.');
}

export {};