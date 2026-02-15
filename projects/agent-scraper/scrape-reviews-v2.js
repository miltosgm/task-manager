const { chromium } = require('playwright');
const fs = require('fs');

const agents = JSON.parse(fs.readFileSync('all-agents-all-reviews.json', 'utf8'));
const agentsWithGoogleReviews = agents.filter(a => a.google_review_count > 0);

console.log(`Scraping full reviews for ${agentsWithGoogleReviews.length} agents...`);

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapeGoogleReviews(page, agentName, location) {
  const searchQuery = `${agentName} ${location} Cyprus`;
  
  console.log(`\n  Searching for: ${searchQuery}`);
  
  try {
    // Go to Google Maps
    await page.goto('https://www.google.com/maps', { waitUntil: 'domcontentloaded' });
    await delay(2000);
    
    // Accept cookies if shown
    try {
      const acceptButton = await page.$('button:has-text("Accept all")');
      if (acceptButton) {
        await acceptButton.click();
        await delay(1000);
      }
    } catch (e) {}
    
    // Search
    const searchBox = await page.$('#searchboxinput');
    if (!searchBox) {
      console.log('  Could not find search box');
      return [];
    }
    
    await searchBox.fill(searchQuery);
    await delay(500);
    await page.keyboard.press('Enter');
    await delay(4000);
    
    // Check if we landed on a place or a list
    const url = page.url();
    console.log(`  URL: ${url.substring(0, 80)}...`);
    
    // Click on reviews count/button
    const reviewsLink = await page.$('button[jsaction*="review"]');
    if (reviewsLink) {
      await reviewsLink.click();
      await delay(2000);
    }
    
    // Try to find and click the reviews tab
    const tabs = await page.$$('button[role="tab"]');
    for (const tab of tabs) {
      const text = await tab.textContent();
      if (text && text.toLowerCase().includes('review')) {
        await tab.click();
        await delay(2000);
        break;
      }
    }
    
    // Scroll the reviews panel to load more
    const scrollContainer = await page.$('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde');
    if (scrollContainer) {
      console.log('  Scrolling to load reviews...');
      for (let i = 0; i < 15; i++) {
        await scrollContainer.evaluate(el => el.scrollTop = el.scrollHeight);
        await delay(800);
      }
    } else {
      // Try alternative scroll container
      const altContainer = await page.$('div.m6QErb.DxyBCb.kA9KIf.dS8AEf');
      if (altContainer) {
        console.log('  Scrolling (alt container)...');
        for (let i = 0; i < 15; i++) {
          await altContainer.evaluate(el => el.scrollTop = el.scrollHeight);
          await delay(800);
        }
      }
    }
    
    // Click all "More" buttons to expand review text
    const moreButtons = await page.$$('button.w8nwRe.kyuRq');
    console.log(`  Expanding ${moreButtons.length} reviews...`);
    for (const btn of moreButtons) {
      try {
        await btn.click();
        await delay(100);
      } catch (e) {}
    }
    
    // Extract all reviews
    const reviews = await page.evaluate(() => {
      const results = [];
      
      // Try multiple selectors for review containers
      const reviewSelectors = [
        'div[data-review-id]',
        'div.jftiEf',
        'div[jscontroller][jsaction*="review"]'
      ];
      
      let reviewEls = [];
      for (const sel of reviewSelectors) {
        reviewEls = document.querySelectorAll(sel);
        if (reviewEls.length > 0) break;
      }
      
      reviewEls.forEach(el => {
        const nameEl = el.querySelector('.d4r55') || el.querySelector('.WNxzHc');
        const ratingEl = el.querySelector('.kvMYJc');
        const dateEl = el.querySelector('.rsqaWe');
        const textEl = el.querySelector('.wiI7pd') || el.querySelector('.MyEned');
        
        const review = {
          reviewer: nameEl?.textContent?.trim() || 'Anonymous',
          rating: null,
          date: dateEl?.textContent?.trim() || null,
          text: textEl?.textContent?.trim() || ''
        };
        
        // Extract rating from aria-label
        if (ratingEl) {
          const ariaLabel = ratingEl.getAttribute('aria-label');
          if (ariaLabel) {
            const match = ariaLabel.match(/(\d)/);
            if (match) review.rating = parseInt(match[1]);
          }
        }
        
        if (review.text && review.text.length > 0) {
          results.push(review);
        }
      });
      
      return results;
    });
    
    console.log(`  Found ${reviews.length} reviews`);
    return reviews;
    
  } catch (error) {
    console.log(`  Error: ${error.message}`);
    return [];
  }
}

async function main() {
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'en-GB',
    geolocation: { latitude: 34.707130, longitude: 33.022617 }, // Cyprus
    permissions: ['geolocation']
  });
  
  const page = await context.newPage();
  
  const allReviews = [];
  let processed = 0;
  let totalReviewsFound = 0;
  
  for (const agent of agentsWithGoogleReviews) {
    processed++;
    console.log(`\n[${processed}/${agentsWithGoogleReviews.length}] ${agent.name} (${agent.google_review_count} Google reviews)`);
    
    const reviews = await scrapeGoogleReviews(page, agent.name, agent.location);
    
    totalReviewsFound += reviews.length;
    
    allReviews.push({
      agent_name: agent.name,
      location: agent.location,
      bazaraki_url: agent.url,
      google_rating: agent.google_rating,
      expected_reviews: agent.google_review_count,
      scraped_reviews: reviews.length,
      reviews: reviews
    });
    
    // Save progress every 5 agents
    if (processed % 5 === 0) {
      fs.writeFileSync('full-reviews-progress.json', JSON.stringify(allReviews, null, 2));
      console.log(`  Progress saved. Total reviews so far: ${totalReviewsFound}`);
    }
    
    // Random delay between agents
    await delay(3000 + Math.random() * 2000);
  }
  
  // Final save
  fs.writeFileSync('full-reviews.json', JSON.stringify(allReviews, null, 2));
  console.log(`\n\n========================================`);
  console.log(`Done! Scraped ${allReviews.length} agents`);
  console.log(`Total reviews collected: ${totalReviewsFound}`);
  console.log(`Saved to full-reviews.json`);
  
  await browser.close();
}

main().catch(console.error);
