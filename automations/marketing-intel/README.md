# Performance Marketing Intelligence Dashboard

**Purpose:** Track what competitors are running in Meta Ads Library, Google Ads trends. Weekly "what's working in ads now" report.

## Data Sources

1. **Meta Ads Library** - Competitor ad creatives
2. **Google Ads Transparency Center** - Competitor Google campaigns
3. **Reddit/Twitter** - Community discussions on what's working
4. **Industry Blogs** - Marketing news

## Workflow

**Weekly Run (Monday 9am):**
1. Scrape/query Meta Ads Library for target competitors
2. Check Google Ads Transparency Center
3. Scan r/PPC, r/marketing, Twitter for "what's working" posts
4. Analyze patterns:
   - Common ad formats
   - Messaging angles
   - Creative trends
5. Generate report:
   - Top 5 competitor ads this week
   - Emerging trends
   - Recommendations

**Output:** 
- PDF report
- Slack #sops post
- Optional: Email delivery

## Implementation

- `scrapers/` - Data collection
  - `meta-ads.js` - Meta Ads Library scraper
  - `google-ads.js` - Google Ads scraper
  - `community.js` - Reddit/Twitter scanner
- `analyze.js` - Trend detection
- `report-generator.js` - PDF creation
- `competitors.json` - Target competitor list

## Configuration Needed

```json
{
  "competitors": [
    "Competitor A",
    "Competitor B"
  ],
  "industries": ["SaaS", "E-commerce"],
  "platforms": ["Meta", "Google"],
  "keywords": ["performance marketing", "conversion optimization"]
}
```

## Status

✅ Framework created
❓ **NEED FROM YOU:**
  - Competitor list (who to track?)
  - Meta/Google account access (if available)
  - Report format preferences
⏳ Building scrapers
