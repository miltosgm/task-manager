# Mission Control Integration Guide

## Quick Start

Every agent operation should log automatically. Use the quick helper:

```javascript
const log = require('./lib/log-helper.js');

// After reading a file
const content = await read('file.txt');
log.read('file.txt', content.split('\n').length);

// After writing a file
const bytes = await write('output.txt', data);
log.write('output.txt', bytes);

// After editing
await edit('config.json', oldText, newText);
log.edit('config.json', 'Updated API endpoint');

// After executing command
const result = await exec('npm build');
log.exec('npm build', result.code, result.duration);

// After searching
const results = await webSearch('query');
log.search('query', results.length);

// Task completion
await deployApp();
log.task('Deploy app', 'success');

// Message sent
await sendMessage(channel, text);
log.message(channel, 'Deployment complete notification');
```

## Integration Pattern

### For OpenClaw Tool Calls

After every tool invocation, log it:

```javascript
// Read operation
const fileContent = tool('read', { path: 'README.md' });
require('./lib/log-helper').read('README.md', 150); // 150 lines

// Write operation  
tool('write', { path: 'output.json', content: json });
require('./lib/log-helper').write('output.json', json.length);

// Exec operation
const start = Date.now();
const result = tool('exec', { command: 'npm test' });
require('./lib/log-helper').exec('npm test', result.code, Date.now() - start);
```

## Current Implementation Status

**✅ Working:**
- Dashboard live: https://mission-control-eight-nu.vercel.app
- API endpoint: POST /api/log-activity
- Logging tools: log-activity.js, auto-log.js, log-helper.js
- Real-time updates (5 second polling)

**🔄 In Progress:**
- Automatic logging for all operations
- Agent using log-helper after every tool call

**📊 Activity Types:**
- `file_created` - New files
- `file_edited` - File updates
- `search` - Searches (web, memory, files)
- `task_completed` - Task/operation completions
- `proposal` - Generated proposals/reports
- `other` - General activities

## Live Dashboard

View all activities: https://mission-control-eight-nu.vercel.app

Features:
- Real-time activity feed (auto-refresh 5s)
- Filter by activity type
- Search activities
- Click to expand details
- Works across all platforms (WhatsApp, Telegram, Slack, etc.)

## Files

- `/lib/log-activity.js` - Core logging (2.5 KB)
- `/lib/auto-log.js` - Operation wrappers (3.5 KB)
- `/lib/log-helper.js` - Quick helper (1.8 KB)
- `/lib/mission-control-helpers.sh` - Shell helpers (1.4 KB)

## Testing

Test logging:
```bash
node lib/log-helper.js task "Test task" success
node lib/log-helper.js search "test query" 5
```

View activities:
```bash
curl https://mission-control-eight-nu.vercel.app/api/log-activity | jq
```

## Agent Integration

From now on, every operation I perform will be logged automatically using this pattern.
