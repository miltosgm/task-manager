/**
 * Browser-based scraper using Puppeteer
 * For Bazaraki.com real estate agents
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.bazaraki.com/stores/19/';
const OUTPUT_DIR = path.join(__dirname, 'data');

async function scrapeAgents() {
  // Ensure output dir exists
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
  
  const allAgents = [];
  let pageNum = 1;
  let hasNextPage = true;
  
  while (hasNextPage && pageNum <= 25) {
    const url = pageNum === 1 ? BASE_URL : `${BASE_URL}?page=${pageNum}`;
    console.log(`Scraping page ${pageNum}: ${url}`);
    
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // Extract agents from the page
    const agents = await page.evaluate(() => {
      const items = [];
      const cards = document.querySelectorAll('ul > li');
      
      cards.forEach(card => {
        const linkEl = card.querySelector('a[href*="/c/"], a[href*="/items/author/"]');
        if (!linkEl) return;
        
        const nameEl = card.querySelector('a[href*="/c/"], a[href*="/items/author/"]');
        const locationEl = card.querySelectorAll('div');
        const verified = card.innerHTML.includes('Verified account');
        
        // Find location (usually contains city name)
        let location = 'Cyprus';
        let adCount = 0;
        let description = '';
        
        card.querySelectorAll('div').forEach(div => {
          const text = div.textContent.trim();
          if (['Limassol', 'Nicosia', 'Paphos', 'Larnaca', 'Famagusta'].includes(text)) {
            location = text;
          }
          if (text.match(/^\d+ ads$/)) {
            adCount = parseInt(text);
          }
          if (text.length > 50 && text.length < 600 && !text.includes('ads')) {
            description = text.substring(0, 300);
          }
        });
        
        const href = linkEl.getAttribute('href');
        const name = nameEl ? nameEl.textContent.replace('Verified account', '').trim() : 'Unknown';
        
        if (href && name !== 'Unknown') {
          items.push({
            name,
            profileUrl: 'https://www.bazaraki.com' + href,
            location,
            adCount,
            description,
            verified,
            source: 'bazaraki'
          });
        }
      });
      
      return items;
    });
    
    console.log(`  Found ${agents.length} agents`);
    allAgents.push(...agents);
    
    // Check for next page
    const nextLink = await page.$('a:has-text("Next")');
    hasNextPage = !!nextLink && agents.length > 0;
    pageNum++;
    
    // Be nice
    await new Promise(r => setTimeout(r, 1500));
  }
  
  await browser.close();
  
  // Dedupe
  const unique = [...new Map(allAgents.map(a => [a.profileUrl, a])).values()];
  
  // Add timestamp
  unique.forEach(a => a.scrapedAt = new Date().toISOString());
  
  // Save
  const jsonPath = path.join(OUTPUT_DIR, 'bazaraki-agents.json');
  fs.writeFileSync(jsonPath, JSON.stringify(unique, null, 2));
  console.log(`\nSaved ${unique.length} agents to ${jsonPath}`);
  
  // CSV
  const headers = ['name', 'location', 'adCount', 'verified', 'profileUrl', 'description'];
  const csv = [
    headers.join(','),
    ...unique.map(a => headers.map(h => `"${String(a[h] || '').replace(/"/g, '""')}"`).join(','))
  ].join('\n');
  const csvPath = path.join(OUTPUT_DIR, 'bazaraki-agents.csv');
  fs.writeFileSync(csvPath, csv);
  console.log(`Saved CSV to ${csvPath}`);
  
  // Stats
  const byLocation = {};
  unique.forEach(a => byLocation[a.location] = (byLocation[a.location] || 0) + 1);
  console.log('\nBy location:', byLocation);
  
  return unique;
}

scrapeAgents().catch(console.error);
