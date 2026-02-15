# Content Repurposing

Transforms LinkedIn posts into other formats while maintaining Miltos's voice.

## Usage

User provides LinkedIn post (URL or paste text), then request format:
- "Repurpose as Twitter thread"
- "Turn this into an email newsletter section"  
- "Expand this into a blog post"

## Process

1. **Extract core message** from LinkedIn post
2. **Load voice profile** from `/Users/milton/clawd/miltos-linkedin-voice.md`
3. **Transform** based on target format:

### Twitter Thread Format
- Hook (first tweet): Attention-grabbing question or bold statement
- 3-5 tweets max (Miltos's style is punchy)
- Each tweet standalone readable
- End with CTA or discussion prompt
- Maintain conversational but expert tone

### Email Newsletter Section
- Subject line suggestion
- Opening hook
- 2-3 paragraphs expanding on the LinkedIn post
- Bullet points for key takeaways
- CTA at end

### Blog Post Expansion
- SEO-friendly title (H1)
- Introduction (problem/hook)
- 3-4 main sections with H2 headers
- Examples and data points
- Conclusion with next steps
- Meta description suggestion

## Voice Consistency Checklist

From `miltos-linkedin-voice.md`:
- Conversational but authoritative
- Short paragraphs (2-3 lines max)
- Strategic use of emojis (not overdone)
- Direct address to reader
- Data-backed claims
- Practical, actionable advice

## Output Format

Present each repurposed version with:
```
### [Platform] Version

[Content]

---
**Why this works:** [Brief explanation of format choices]
```
