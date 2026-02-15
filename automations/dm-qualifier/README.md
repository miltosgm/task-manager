# LinkedIn DM Pre-Qualifier

**Purpose:** Monitor incoming LinkedIn DMs, research the sender, qualify them, and draft appropriate responses.

## Workflow

1. **Detect New DM** (via LinkedIn integration)
2. **Research Sender:**
   - Company size, industry, role
   - LinkedIn activity (recent posts, engagement)
   - Mutual connections
   - Company pain points (from their content)
3. **Qualification Score:**
   - High: Decision-maker at target company size
   - Medium: Relevant but needs nurturing
   - Low: Recruiter, irrelevant pitch, spam
4. **Draft Response:**
   - High: Enthusiastic + calendar link
   - Medium: Polite interest + question
   - Low: Polite decline template

## Implementation

- `monitor.js` - DM detection (needs LinkedIn integration)
- `research.js` - Sender background research
- `qualify.js` - Scoring algorithm
- `responses/` - Response templates by qualification level

## Usage

Runs automatically when new DM detected, or manual:
```
"Qualify this LinkedIn DM: [paste DM content]"
```

## Status

✅ Framework created
❓ **BLOCKER:** Need LinkedIn API access or scraping solution
⏳ Building research + qualification logic
