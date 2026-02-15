const { chromium } = require('playwright');
const fs = require('fs');

const agents = JSON.parse(fs.readFileSync('all-agents-all-reviews.json', 'utf8'));
const agentsWithGoogleReviews = agents.filter(a => a.google_review_count > 0);

console.log(`Scraping full reviews for ${agentsWithGoogleReviews.length} agents...`);

async function scrapeGoogleReviews(page, agentName, location) {
  const searchQuery = encodeURIComponent(`${agentName} real estate ${location} Cyprus`);
  const url = `https://www.google.com/maps/search/${searchQuery}`;
  
  console.log(`\nSearching: ${agentName}`);
  
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // Click on first result if it's a list
    const firstResult = await page.$('div[role="feed"] > div:first-child');
    if (firstResult) {
      await firstResult.click();
      await page.waitForTimeout(2000);
    }
    
    // Look for reviews tab/button
    const reviewsButton = await page.$('button[aria-label*="Reviews"]');
    if (reviewsButton) {
      await reviewsButton.click();
      await page.waitForTimeout(2000);
    }
    
    // Scroll to load all reviews
    const reviewsPanel = await page.$('div[role="main"]');
    if (reviewsPanel) {
      for (let i = 0; i < 10; i++) {
        await page.evaluate(() => {
          const scrollable = document.querySelector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf');
          if (scrollable) scrollable.scrollTop = scrollable.scrollHeight;
        });
        await page.waitForTimeout(1000);
      }
    }
    
    // Expand all "More" buttons in reviews
    const moreButtons = await page.$$('button.w8nwRe.kyuRq');
    for (const btn of moreButtons) {
      try {
        await btn.click();
        await page.waitForTimeout(200);
      } catch (e) {}
    }
    
    // Extract reviews
    const reviews = await page.evaluate(() => {
      const reviewElements = document.querySelectorAll('div[data-review-id]');
      return Array.from(reviewElements).map(el => {
        const nameEl = el.querySelector('.d4r55');
        const ratingEl = el.querySelector('.kvMYJc');
        const dateEl = el.querySelector('.rsqaWe');
        const textEl = el.querySelector('.wiI7pd');
        
        return {
          reviewer: nameEl?.textContent?.trim() || 'Unknown',
          rating: ratingEl?.getAttribute('aria-label')?.match(/(\d)/)?.[1] || null,
          date: dateEl?.textContent?.trim() || null,
          text: textEl?.textContent?.trim() || ''
        };
      }).filter(r => r.text.length > 0);
    });
    
    console.log(`  Found ${reviews.length} reviews`);
    return reviews;
    
  } catch (error) {
    console.log(`  Error: ${error.message}`);
    return [];
  }
}

async function main() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();
  
  const allReviews = [];
  let processed = 0;
  
  for (const agent of agentsWithGoogleReviews) {
    processed++;
    console.log(`\n[${processed}/${agentsWithGoogleReviews.length}] ${agent.name}`);
    
    const reviews = await scrapeGoogleReviews(page, agent.name, agent.location);
    
    if (reviews.length > 0) {
      allReviews.push({
        agent_name: agent.name,
        location: agent.location,
        google_rating: agent.google_rating,
        total_review_count: agent.google_review_count,
        scraped_reviews: reviews.length,
        reviews: reviews
      });
    }
    
    // Save progress every 5 agents
    if (processed % 5 === 0) {
      fs.writeFileSync('full-reviews-progress.json', JSON.stringify(allReviews, null, 2));
      console.log('  Progress saved...');
    }
    
    // Random delay to avoid rate limiting
    await page.waitForTimeout(2000 + Math.random() * 2000);
  }
  
  // Final save
  fs.writeFileSync('full-reviews.json', JSON.stringify(allReviews, null, 2));
  console.log(`\n\nDone! Saved ${allReviews.length} agents with reviews to full-reviews.json`);
  
  // Count total reviews
  const totalReviews = allReviews.reduce((sum, a) => sum + a.reviews.length, 0);
  console.log(`Total reviews scraped: ${totalReviews}`);
  
  await browser.close();
}

main().catch(console.error);
