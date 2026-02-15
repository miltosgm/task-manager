#!/usr/bin/env node
/**
 * Quick logging helper for agent operations
 * Usage: require and call after each operation
 */

const { execSync } = require('child_process');
const path = require('path');

const LOG_BIN = path.join(__dirname, 'log-activity.js');

// Log in background, don't block
function logBg(type, description, result) {
  try {
    const cmd = `node "${LOG_BIN}" ${type} "${description}" "${result}" 2>/dev/null &`;
    execSync(cmd, { stdio: 'ignore', timeout: 100 });
  } catch (e) {
    // Silently fail - don't break agent
  }
}

// Quick logging functions
const log = {
  read: (file, lines = 0) => logBg('search', `Read ${path.basename(file)}`, `${lines} lines retrieved`),
  
  write: (file, bytes = 0) => logBg('file_created', `Created ${path.basename(file)}`, `${(bytes/1024).toFixed(1)} KB`),
  
  edit: (file, change = '') => logBg('file_edited', `Updated ${path.basename(file)}`, change),
  
  exec: (cmd, code = 0, ms = 0) => {
    const short = cmd.length > 50 ? cmd.substring(0, 50) + '...' : cmd;
    const status = code === 0 ? 'Success' : 'Failed';
    logBg('task_completed', `Exec: ${short}`, `${status} (${ms}ms)`);
  },
  
  search: (query, count = 0) => logBg('search', `Searched: ${query}`, `${count} results`),
  
  task: (name, status = 'success') => logBg('task_completed', name, status.charAt(0).toUpperCase() + status.slice(1)),
  
  message: (platform, summary = '') => logBg('other', `Response on ${platform}`, summary),
};

module.exports = log;

// CLI usage
if (require.main === module) {
  const [,, action, ...args] = process.argv;
  if (log[action]) {
    log[action](...args);
    console.log(`✅ Logged ${action}`);
  } else {
    console.error('Usage: node log-helper.js <action> [args...]');
    console.error('Actions:', Object.keys(log).join(', '));
  }
}
