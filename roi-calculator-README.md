# ROI Calculator - Deployment Guide

## What This Is
A lead generation tool for Growth-onomics that calculates:
- **ROI (Return on Investment)** - Campaign profitability
- **CAC (Customer Acquisition Cost)** - Cost per new customer
- **Revenue Per Customer** - Average revenue per customer
- **LTV:CAC Ratio** - Customer lifetime value vs acquisition cost

## Features
✅ Clean, professional design with Growth-onomics branding
✅ Mobile-responsive layout
✅ Real-time calculations with visual feedback
✅ Color-coded results (green for good, red for warning)
✅ Built-in CTA to book consultation
✅ SEO-friendly meta tags
✅ No dependencies - pure HTML/CSS/JS

## How to Deploy

### Option 1: Add to Growth-onomics Website
1. Upload `roi-calculator.html` to your web server
2. Access at: `https://growth-onomics.com/roi-calculator`
3. Update the consultation CTA link if needed (currently: `https://growth-onomics.com/contact`)

### Option 2: Standalone Hosting (Netlify/Vercel)
1. Create new GitHub repo or use existing one
2. Push `roi-calculator.html` (rename to `index.html` for root hosting)
3. Connect to Netlify or Vercel
4. Deploy (takes ~30 seconds)
5. Get free HTTPS domain

### Option 3: Lead Magnet Landing Page
Embed this on a dedicated landing page with:
- LinkedIn/Meta ads driving traffic
- Email capture before revealing full results (add form)
- Retargeting pixel for follow-up

## Customization Options

### Branding
- Colors: Currently using purple gradient (#667eea → #764ba2)
- Change in CSS variables at top of `<style>` section
- Update footer links to your preferred URLs

### Add Email Capture
Insert before calculation results:
```html
<div class="email-gate">
    <input type="email" placeholder="Enter email to see results" required>
    <button onclick="unlockResults()">Get My Results</button>
</div>
```

### Analytics Tracking
Add before `</body>`:
```html
<script>
    // Google Analytics
    gtag('event', 'calculator_use', {
        'event_category': 'engagement',
        'event_label': 'roi_calculator'
    });
</script>
```

## Marketing Uses

### LinkedIn Posts
"Want to know if your marketing campaigns are actually profitable? Try our free ROI calculator → [link]"

### Email Signature
Add calculator link to team signatures

### Proposal Attachments
Share with prospects during sales conversations

### Content Upgrades
Mention in blog posts about performance marketing

## Metrics to Track
- Page views
- Calculator uses (completion rate)
- CTA clicks (consultation bookings)
- Time on page
- Return visitors

## Next Steps
1. Upload to Growth-onomics website
2. Test on mobile devices
3. Share on LinkedIn (Miltos's 16.7K followers)
4. Add to email campaigns
5. Consider A/B testing different CTAs

## Technical Notes
- Single-file implementation (no external dependencies)
- Works offline once loaded
- Browser compatibility: All modern browsers
- Load time: <1 second
- No backend required - pure client-side

---

**Built by Clawdy for Growth-onomics**
Questions? Ping Miltos at miltosgm@gmail.com
