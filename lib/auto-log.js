#!/usr/bin/env node
/**
 * Auto-logging wrapper for OpenClaw agent operations
 * 
 * This script wraps common operations and automatically logs them to Mission Control
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const DASHBOARD_URL = process.env.MISSION_CONTROL_URL || 'https://mission-control-eight-nu.vercel.app';

async function logActivity(event) {
  const data = JSON.stringify({
    timestamp: Date.now(),
    type: event.type,
    description: event.description,
    result: event.result,
    metadata: event.metadata || {}
  });

  const url = new URL(`${DASHBOARD_URL}/api/log-activity`);
  
  const options = {
    hostname: url.hostname,
    port: url.port || 443,
    path: url.pathname,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length,
      'X-Activity-Source': 'openclaw-agent'
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(body);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', (error) => reject(error));
    req.write(data);
    req.end();
  });
}

// Track operation start times
const operationTimers = new Map();

/**
 * Start tracking an operation
 */
function startOperation(id) {
  operationTimers.set(id, Date.now());
}

/**
 * End and log an operation
 */
function endOperation(id, type, description, result) {
  const startTime = operationTimers.get(id);
  const duration = startTime ? Date.now() - startTime : 0;
  operationTimers.delete(id);
  
  const finalResult = duration > 0 ? `${result} (${duration}ms)` : result;
  return logActivity({ type, description, result: finalResult });
}

/**
 * Wrap file write with logging
 */
async function writeFileLogged(filePath, content) {
  const opId = `write-${Date.now()}`;
  startOperation(opId);
  
  try {
    fs.writeFileSync(filePath, content, 'utf8');
    const stats = fs.statSync(filePath);
    const sizeKB = (stats.size / 1024).toFixed(1);
    
    await endOperation(
      opId,
      'file_created',
      `Created ${path.basename(filePath)}`,
      `${sizeKB} KB written`
    );
    
    return true;
  } catch (error) {
    await endOperation(opId, 'other', `Failed to write ${filePath}`, error.message);
    throw error;
  }
}

/**
 * Wrap file edit with logging
 */
async function editFileLogged(filePath, description) {
  const opId = `edit-${Date.now()}`;
  startOperation(opId);
  
  try {
    const stats = fs.statSync(filePath);
    const sizeKB = (stats.size / 1024).toFixed(1);
    
    await endOperation(
      opId,
      'file_edited',
      `Updated ${path.basename(filePath)}`,
      `${description} (${sizeKB} KB)`
    );
    
    return true;
  } catch (error) {
    await endOperation(opId, 'other', `Failed to edit ${filePath}`, error.message);
    return false;
  }
}

/**
 * Log a search operation
 */
async function logSearch(query, resultCount, source = 'unknown') {
  return logActivity({
    type: 'search',
    description: `Searched: ${query}`,
    result: `Found ${resultCount} results from ${source}`
  });
}

/**
 * Log a task completion
 */
async function logTask(taskName, status = 'success', details = '') {
  const statusText = status === 'success' ? 'Success' : 'Failed';
  return logActivity({
    type: 'task_completed',
    description: taskName,
    result: details ? `${statusText}: ${details}` : statusText
  });
}

/**
 * Log an exec command
 */
async function logExec(command, exitCode, duration = 0) {
  const success = exitCode === 0;
  const statusText = success ? 'Success' : 'Failed';
  return logActivity({
    type: 'task_completed',
    description: `Executed: ${command.substring(0, 60)}${command.length > 60 ? '...' : ''}`,
    result: `${statusText} - Exit code ${exitCode} (${duration}ms)`
  });
}

/**
 * Log a web fetch
 */
async function logWebFetch(url, status, sizeKB) {
  return logActivity({
    type: 'search',
    description: `Fetched ${url}`,
    result: `Status ${status}, ${sizeKB} KB retrieved`
  });
}

/**
 * Log agent message/response
 */
async function logMessage(channel, summary, wordCount) {
  return logActivity({
    type: 'other',
    description: `Responded on ${channel}`,
    result: `${wordCount} words - ${summary}`
  });
}

module.exports = {
  writeFileLogged,
  editFileLogged,
  logSearch,
  logTask,
  logExec,
  logWebFetch,
  logMessage,
  startOperation,
  endOperation
};
