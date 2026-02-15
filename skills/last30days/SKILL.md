---
name: last30days
description: Research any topic across Reddit and X/Twitter from the last 30 days, synthesize what's trending/working, and generate ready-to-use prompts. Use when user says "last30days:" followed by a topic, or asks for recent community insights, trending prompts, or what's working now for any tool/topic.
---

# Last 30 Days Research

Research any topic by scanning Reddit and X discussions from the last 30 days.

## Trigger

User message contains "last30days:" followed by a topic.

Examples:
- "last30days: best ChatGPT prompts for coding"
- "last30days: Midjourney v6 tips"
- "last30days: what are people saying about DeepSeek"

## Workflow

### 1. Parse the Query

Extract:
- **Topic**: The main subject to research
- **Target tool** (optional): If user wants prompts FOR a specific tool (ChatGPT, Midjourney, Suno, etc.)

### 2. Search Reddit (via Brave)

```
web_search:
  query: "site:reddit.com {topic}"
  freshness: "pm"  # past month
  count: 10
```

Look for:
- r/ChatGPT, r/LocalLLaMA, r/midjourney, r/StableDiffusion, r/ClaudeAI
- Upvote counts in snippets
- Specific techniques, tips, prompts mentioned

### 3. Search X/Twitter (via Brave)

```
web_search:
  query: "site:twitter.com OR site:x.com {topic}"
  freshness: "pm"
  count: 10
```

Look for:
- Viral posts (likes/reposts mentioned)
- Practitioners sharing what works
- Threads with examples

### 4. Fetch Top Results (optional)

If search snippets lack detail, use `web_fetch` on 2-3 top URLs to get full content.

### 5. Synthesize Findings

Create a summary covering:
- **Key patterns**: What techniques/approaches are people praising?
- **Common mistakes**: What to avoid?
- **Engagement signals**: Which posts got most upvotes/likes?
- **Specific examples**: Actual prompts or techniques that worked

### 6. Generate Prompt (if applicable)

If user wants prompts for a specific tool, write a **copy-paste-ready prompt** based on discovered patterns.

Structure the prompt using best practices found in the research.

## Output Format

```
## 🔍 Last 30 Days: {topic}

### What's Working
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

### Sources
- Reddit: [X] threads analyzed
- X/Twitter: [Y] posts analyzed

### Top Patterns
[Synthesized insights from community]

### Ready-to-Use Prompt (if applicable)
[Copy-paste prompt based on research]
```

## Limitations

- Brave search is less comprehensive than direct API access
- X/Twitter coverage depends on indexing
- No engagement metrics (upvotes/likes) unless in snippets
- Best for popular topics with active discussion
