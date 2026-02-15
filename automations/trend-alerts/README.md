# Trend Alert System

**Purpose:** Daily scan for breaking news in performance marketing, AI search, AEO/GEO. Alert Miltos to "post-worthy" topics while they're fresh.

## How It Works

1. **Scheduled Run** (via cron): Every morning at 8am GMT+2
2. **Search Topics:**
   - Performance marketing news
   - AI search updates (ChatGPT Search, Perplexity, Google SGE)
   - AEO/GEO developments
   - Meta Ads / Google Ads updates
3. **Filter for "Hot Takes":**
   - Published in last 24 hours
   - High engagement (upvotes, shares)
   - Controversial or trend-setting
4. **Generate Alert:**
   - Summary of the trend
   - Why it matters
   - Draft LinkedIn post angle
5. **Deliver:** Telegram message to Miltos

## Implementation

- `scan.js` - Main scanning logic
- `topics.json` - Search topics configuration
- `filters.js` - Relevance scoring
- `draft-post.js` - LinkedIn post generator using voice profile

## Cron Schedule

```json
{
  "schedule": "0 8 * * *",
  "timezone": "Europe/Athens",
  "action": "Run trend scan and alert if worthy topics found"
}
```

## Status

✅ Framework created
⏳ Building scan logic
