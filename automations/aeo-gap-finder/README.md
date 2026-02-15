# SEO/AEO Content Gap Finder

**Purpose:** Analyze what AI search engines (ChatGPT, Perplexity, Google SGE) show for target keywords. Find gaps competitors aren't covering. Generate content briefs.

## How It Works

**Input:** Target keyword or topic
**Process:**
1. Query ChatGPT Search, Perplexity, Google for the keyword
2. Extract what content they surface
3. Analyze competitor coverage
4. Identify gaps (questions asked but not fully answered)
5. Generate content brief to fill the gap

**Output:**
- **Current Landscape:** What AI search shows now
- **Competitor Analysis:** Who's ranking, what they cover
- **Gap Opportunities:** Uncovered angles
- **Content Brief:** Outline for blog post/article to fill gap

## Implementation

- `gap-finder.js` - Main analysis logic
- `search/` - AI search query modules
  - `chatgpt.js` - ChatGPT Search query
  - `perplexity.js` - Perplexity query
  - `google.js` - Google SGE/search
- `analyze.js` - Gap detection algorithm
- `brief-generator.js` - Content brief writer

## Usage

```
"Find AEO gaps for: [keyword/topic]"
```

## Status

✅ Framework created
⏳ Building search integrations
❓ Need: API access or scraping approach for each platform
