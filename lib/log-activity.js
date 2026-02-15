#!/usr/bin/env node
/**
 * Mission Control Activity Logger CLI
 * 
 * Usage:
 *   node log-activity.js file_created "Created README.md" "2.5 KB"
 *   node log-activity.js task_completed "Fixed bug #123" "✅ Success"
 */

const https = require('https');

const DASHBOARD_URL = process.env.MISSION_CONTROL_URL || 'https://mission-control-eight-nu.vercel.app';

async function logActivity(type, description, result, metadata = {}) {
  const data = JSON.stringify({
    timestamp: Date.now(),
    type,
    description,
    result,
    metadata
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
          console.log(`✅ Logged: ${description}`);
          resolve(body);
        } else {
          console.error(`❌ Failed to log activity: ${res.statusCode}`);
          reject(new Error(`HTTP ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', (error) => {
      console.error('❌ Connection error:', error.message);
      reject(error);
    });

    req.write(data);
    req.end();
  });
}

// CLI usage
if (require.main === module) {
  const [,, type, description, result, ...metadataPairs] = process.argv;
  
  if (!type || !description || !result) {
    console.error('Usage: node log-activity.js <type> <description> <result> [key=value...]');
    console.error('\nTypes: file_created, file_edited, search, task_completed, proposal, other');
    console.error('\nExample:');
    console.error('  node log-activity.js task_completed "Deploy dashboard" "✅ Success" env=production');
    process.exit(1);
  }

  // Parse metadata from key=value pairs
  const metadata = {};
  metadataPairs.forEach(pair => {
    const [key, value] = pair.split('=');
    if (key && value) metadata[key] = value;
  });

  logActivity(type, description, result, metadata)
    .then(() => process.exit(0))
    .catch((error) => {
      console.error('Failed:', error.message);
      process.exit(1);
    });
}

module.exports = { logActivity };
