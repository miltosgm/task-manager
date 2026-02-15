#!/usr/bin/env node
/**
 * Test the auto-logging system
 */

const { writeFileLogged, logTask, logSearch, logExec } = require('./auto-log.js');
const path = require('path');

async function demo() {
  console.log('🔄 Testing auto-logging system...\n');
  
  // Test 1: Log a search
  await logSearch('OpenClaw documentation', 15, 'local files');
  console.log('✅ Test 1: Search logged\n');
  
  // Test 2: Create a file with logging
  const testFile = path.join(__dirname, 'test-output.txt');
  const content = 'This is a test file created by auto-logging system.\n';
  await writeFileLogged(testFile, content);
  console.log('✅ Test 2: File creation logged\n');
  
  // Test 3: Log a task
  await logTask('Auto-logging demonstration', 'success', 'All tests passed');
  console.log('✅ Test 3: Task logged\n');
  
  // Test 4: Log an exec
  await logExec('npm run build', 0, 1250);
  console.log('✅ Test 4: Exec logged\n');
  
  console.log('✨ Auto-logging system working! Check Mission Control dashboard.\n');
}

demo().catch(console.error);
