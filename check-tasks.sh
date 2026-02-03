#!/bin/bash

# Check project-tasks for "In Progress" tasks
# Run this during heartbeats

TASKS_URL="https://raw.githubusercontent.com/miltosgm/project-tasks/main/tasks.json"

echo "Checking for In Progress tasks..."
curl -s "$TASKS_URL" | jq -r '
  to_entries[] | 
  .key as $project | 
  .value[] | 
  select(.status == "in-progress") | 
  "[\($project)] \(.name) (Priority: \(.priority), Due: \(.date // "none"))"
'
