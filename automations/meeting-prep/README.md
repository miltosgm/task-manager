# Meeting Prep Assistant

**Purpose:** Before client calls, auto-research their company, recent news, industry trends. Generate discussion topics and smart questions.

## Workflow

**Trigger:** "Meeting with [Company/Person] on [Date/Time] about [Topic]"

**Research Process:**
1. Company/person background
2. Recent news (last 30 days)
3. Industry trends relevant to the meeting topic
4. Competitor analysis
5. Social media presence check

**Output:**
- **Brief:** 2-paragraph company overview
- **Recent Activity:** News, product launches, funding
- **Discussion Topics:** 3-5 smart questions to ask
- **Talking Points:** How your services connect to their needs
- **Follow-up Draft:** Email template for post-meeting

## Implementation

- `prep.js` - Main research orchestrator
- `research/` - Research modules
  - `company-intel.js` - Company background
  - `news-scan.js` - Recent news aggregator
  - `social-check.js` - LinkedIn/Twitter activity
- `templates/` - Output templates

## Usage

```
"Meeting prep: [Company Name] - discussing AEO strategy tomorrow at 2pm"
```

## Status

✅ Framework created
⏳ Building research modules
