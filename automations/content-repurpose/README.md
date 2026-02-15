# Content Repurposing Engine

**Purpose:** Take LinkedIn posts → transform into Twitter threads, email newsletter snippets, blog post drafts. Maintains Miltos's voice across platforms.

## Workflow

**Input:** LinkedIn post URL or text
**Output:** 
- Twitter thread (with hooks)
- Email newsletter section
- Blog post expansion (optional)
- Short-form quote graphics (text suggestions)

## Voice Consistency

Uses `miltos-linkedin-voice.md` to maintain:
- Conversational but expert tone
- Specific formatting patterns
- Signature phrases

## Implementation

- `repurpose.js` - Main repurposing logic
- `formats/` - Platform-specific templates
  - `twitter.js` - Thread generator
  - `email.js` - Newsletter formatter
  - `blog.js` - Long-form expander

## Usage

```bash
# Via chat
"Repurpose this LinkedIn post: [URL or paste text]"

# Or batch mode
"Repurpose my last 5 LinkedIn posts"
```

## Status

✅ Framework created
⏳ Building format templates
