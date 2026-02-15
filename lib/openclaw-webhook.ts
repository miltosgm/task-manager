/**
 * OpenClaw Webhook Integration Library
 * 
 * Use this in your OpenClaw agent to automatically log activities
 * to the Mission Control dashboard.
 * 
 * Example:
 * import { logActivity } from '@/lib/openclaw-webhook'
 * 
 * logActivity({
 *   type: 'file_created',
 *   description: 'Created portfolio-plan.md',
 *   result: '12.6 KB file generated'
 * })
 */

export type ActivityType = 
  | 'file_created'
  | 'file_edited'
  | 'search'
  | 'task_completed'
  | 'proposal'
  | 'other'

export interface ActivityEvent {
  type: ActivityType
  description: string
  result: string
  metadata?: Record<string, any>
}

/**
 * Get the dashboard URL (uses env var or defaults to localhost)
 */
function getDashboardUrl(): string {
  if (typeof window !== 'undefined') {
    // Client-side
    return process.env.NEXT_PUBLIC_MISSION_CONTROL_URL || 'http://localhost:3000'
  }
  // Server-side
  return process.env.MISSION_CONTROL_URL || 'http://localhost:3000'
}

/**
 * Log an activity to Mission Control dashboard
 * 
 * @param event Activity event to log
 * @returns Promise that resolves when activity is logged
 */
export async function logActivity(event: ActivityEvent): Promise<void> {
  try {
    const dashboardUrl = getDashboardUrl()
    const url = `${dashboardUrl}/api/log-activity`

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Activity-Source': 'openclaw-agent',
      },
      body: JSON.stringify({
        timestamp: Date.now(),
        type: event.type,
        description: event.description,
        result: event.result,
        metadata: event.metadata || {}
      })
    })

    if (!response.ok) {
      const error = await response.text()
      console.error(`[Mission Control] Failed to log activity: ${response.status}`, error)
    } else {
      console.log(`[Mission Control] ✅ Logged: ${event.description}`)
    }
  } catch (error) {
    // Silently fail - don't break agent if dashboard is down
    console.error('[Mission Control] Connection error (dashboard may be offline):', error)
  }
}

/**
 * Log file creation
 */
export async function logFileCreated(path: string, sizeBytes: number): Promise<void> {
  return logActivity({
    type: 'file_created',
    description: `Created ${path}`,
    result: `${(sizeBytes / 1024).toFixed(1)} KB file`
  })
}

/**
 * Log file edit
 */
export async function logFileEdited(path: string, changes: string): Promise<void> {
  return logActivity({
    type: 'file_edited',
    description: `Updated ${path}`,
    result: changes
  })
}

/**
 * Log search operation
 */
export async function logSearch(query: string, resultCount: number, sources: string[]): Promise<void> {
  return logActivity({
    type: 'search',
    description: `Searched for "${query}"`,
    result: `Found ${resultCount} results from ${sources.join(', ')}`
  })
}

/**
 * Log task completion
 */
export async function logTaskCompleted(taskName: string, durationMs: number, status: 'success' | 'failed' = 'success'): Promise<void> {
  return logActivity({
    type: 'task_completed',
    description: taskName,
    result: `${status === 'success' ? '✅' : '❌'} Completed in ${durationMs}ms`
  })
}

/**
 * Log proposal/document generation
 */
export async function logProposal(name: string, pageCount: number, description: string): Promise<void> {
  return logActivity({
    type: 'proposal',
    description: `Generated ${name}`,
    result: `${pageCount} pages - ${description}`
  })
}

/**
 * Log custom activity
 */
export async function logCustom(description: string, result: string): Promise<void> {
  return logActivity({
    type: 'other',
    description,
    result
  })
}

/**
 * Batch log multiple activities
 */
export async function logActivities(events: ActivityEvent[]): Promise<void> {
  await Promise.all(events.map(logActivity))
}
