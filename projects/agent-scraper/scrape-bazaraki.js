/**
 * Cyprus Real Estate Agent Scraper - Bazaraki.com
 * Collects agent/agency data from Bazaraki stores directory
 */

const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.bazaraki.com/stores/19/';
const TOTAL_PAGES = 23;
const OUTPUT_FILE = path.join(__dirname, 'data', 'bazaraki-agents.json');
const CSV_FILE = path.join(__dirname, 'data', 'bazaraki-agents.csv');

// Ensure data directory exists
if (!fs.existsSync(path.join(__dirname, 'data'))) {
  fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });
}

async function fetchPage(pageNum) {
  const url = pageNum === 1 ? BASE_URL : `${BASE_URL}?page=${pageNum}`;
  console.log(`Fetching page ${pageNum}...`);
  
  const response = await fetch(url);
  const html = await response.text();
  return html;
}

function parseAgents(html) {
  const agents = [];
  
  // Match store listings - each listitem contains an agent
  // Pattern: store name, description, location, ad count, profile URL
  
  // Extract store links and info using regex (simple approach)
  const storePattern = /<a[^>]*href="(\/c\/[^"]+\/|\/items\/author\/[^"]+\/)"[^>]*>([^<]+)<\/a>/gi;
  const locationPattern = /<div[^>]*class="[^"]*store-location[^"]*"[^>]*>([^<]+)<\/div>/gi;
  
  // More robust: parse the structured data
  // Looking for patterns like: link to /c/STORENAME/ with store name text
  
  const storeBlocks = html.match(/<li[^>]*>[\s\S]*?<\/li>/gi) || [];
  
  for (const block of storeBlocks) {
    // Skip if not a real estate store block
    if (!block.includes('/c/') && !block.includes('/items/author/')) continue;
    
    // Extract profile URL
    const urlMatch = block.match(/href="(\/c\/[^"]+\/|\/items\/author\/[^"]+\/)"/);
    if (!urlMatch) continue;
    
    // Extract name (text inside the main link)
    const nameMatch = block.match(/>([^<]+)<span[^>]*>Verified account<\/span>/i) ||
                      block.match(/class="[^"]*store-name[^"]*"[^>]*>([^<]+)</i);
    
    // Extract location
    const locationMatch = block.match(/(Limassol|Nicosia|Paphos|Larnaca|Famagusta)/i);
    
    // Extract ad count
    const adsMatch = block.match(/(\d+)\s*ads/i);
    
    // Extract description
    const descMatch = block.match(/<div[^>]*>([^<]{50,500})<\/div>/);
    
    if (urlMatch) {
      agents.push({
        name: nameMatch ? nameMatch[1].trim() : 'Unknown',
        profileUrl: 'https://www.bazaraki.com' + urlMatch[1],
        location: locationMatch ? locationMatch[1] : 'Cyprus',
        adCount: adsMatch ? parseInt(adsMatch[1]) : 0,
        description: descMatch ? descMatch[1].trim().substring(0, 200) : '',
        verified: block.includes('Verified account'),
        source: 'bazaraki',
        scrapedAt: new Date().toISOString()
      });
    }
  }
  
  return agents;
}

async function scrapeAllPages() {
  const allAgents = [];
  
  for (let page = 1; page <= TOTAL_PAGES; page++) {
    try {
      const html = await fetchPage(page);
      const agents = parseAgents(html);
      allAgents.push(...agents);
      console.log(`  Found ${agents.length} agents on page ${page}`);
      
      // Be nice to the server
      await new Promise(r => setTimeout(r, 1000));
    } catch (err) {
      console.error(`Error on page ${page}:`, err.message);
    }
  }
  
  return allAgents;
}

function saveToJson(agents) {
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(agents, null, 2));
  console.log(`Saved ${agents.length} agents to ${OUTPUT_FILE}`);
}

function saveToCsv(agents) {
  const headers = ['name', 'location', 'adCount', 'verified', 'profileUrl', 'description'];
  const rows = agents.map(a => 
    headers.map(h => `"${String(a[h] || '').replace(/"/g, '""')}"`).join(',')
  );
  const csv = [headers.join(','), ...rows].join('\n');
  fs.writeFileSync(CSV_FILE, csv);
  console.log(`Saved CSV to ${CSV_FILE}`);
}

async function main() {
  console.log('Starting Bazaraki scrape...');
  console.log(`Target: ${TOTAL_PAGES} pages of real estate agencies\n`);
  
  const agents = await scrapeAllPages();
  
  // Deduplicate by URL
  const unique = [...new Map(agents.map(a => [a.profileUrl, a])).values()];
  
  console.log(`\nTotal unique agents: ${unique.length}`);
  
  // Stats by location
  const byLocation = {};
  unique.forEach(a => {
    byLocation[a.location] = (byLocation[a.location] || 0) + 1;
  });
  console.log('By location:', byLocation);
  
  saveToJson(unique);
  saveToCsv(unique);
  
  console.log('\nDone!');
}

main().catch(console.error);
