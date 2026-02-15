#!/bin/bash
# Mission Control Activity Logging Helpers
# Source this file to get automatic activity logging functions

LOGGER="/Users/milton/clawd/lib/log-activity.js"

# Log file creation
mc_log_file_created() {
    local filepath="$1"
    local size="$2"
    node "$LOGGER" file_created "Created $filepath" "$size KB" &>/dev/null &
}

# Log file edit
mc_log_file_edited() {
    local filepath="$1"
    local changes="$2"
    node "$LOGGER" file_edited "Updated $filepath" "$changes" &>/dev/null &
}

# Log search
mc_log_search() {
    local query="$1"
    local count="$2"
    node "$LOGGER" search "Searched: $query" "Found $count results" &>/dev/null &
}

# Log task completion
mc_log_task() {
    local task="$1"
    local status="${2:-success}"
    node "$LOGGER" task_completed "$task" "Status: $status" &>/dev/null &
}

# Log custom activity
mc_log() {
    local desc="$1"
    local result="$2"
    node "$LOGGER" other "$desc" "$result" &>/dev/null &
}

# Wrap common operations
mc_write() {
    local file="$1"
    local content="$2"
    echo "$content" > "$file"
    local size=$(wc -c < "$file" | awk '{printf "%.1f", $1/1024}')
    mc_log_file_created "$file" "$size"
}

mc_edit() {
    local file="$1"
    local description="$2"
    mc_log_file_edited "$file" "$description"
}

export -f mc_log_file_created mc_log_file_edited mc_log_search mc_log_task mc_log mc_write mc_edit
