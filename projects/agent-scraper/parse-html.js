const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const allAgents = [];

// Parse each HTML file
for (let i = 1; i <= 23; i++) {
  const filePath = path.join(dataDir, `html_page_${i}.html`);
  if (!fs.existsSync(filePath)) {
    console.log(`Skipping page ${i} - file not found`);
    continue;
  }
  
  const html = fs.readFileSync(filePath, 'utf8');
  
  // Extract agent links using regex
  // Pattern: /c/STORENAME/ with name nearby
  const pattern = /href="(\/c\/[^"]+\/)"[^>]*>([^<]+?)(?:<[^>]*>Verified account)?<\/a>/gi;
  let match;
  
  while ((match = pattern.exec(html)) !== null) {
    const url = 'https://www.bazaraki.com' + match[1];
    let name = match[2].trim();
    
    // Skip navigation links
    if (name.length < 3 || name.match(/^\d+$/) || name === 'Next' || name === 'Previous') continue;
    
    // Find location near this match (look in surrounding context)
    const contextStart = Math.max(0, match.index - 500);
    const contextEnd = Math.min(html.length, match.index + 1000);
    const context = html.substring(contextStart, contextEnd);
    
    const locationMatch = context.match(/(Limassol|Nicosia|Paphos|Larnaca|Famagusta)(?:<\/div>|<\/span>|\s)/);
    const adsMatch = context.match(/(\d+)\s*ads/);
    
    allAgents.push({
      name,
      url,
      location: locationMatch ? locationMatch[1] : 'Cyprus',
      ads: adsMatch ? parseInt(adsMatch[1]) : 0,
      page: i
    });
  }
  
  console.log(`Page ${i}: Found ${allAgents.filter(a => a.page === i).length} agents`);
}

// Dedupe by URL
const unique = [...new Map(allAgents.map(a => [a.url, a])).values()];

// Add metadata
unique.forEach(a => {
  a.source = 'bazaraki';
  a.verified = true;
  a.scrapedAt = new Date().toISOString();
  delete a.page;
});

// Save JSON
const jsonPath = path.join(dataDir, 'cyprus-agents-bazaraki.json');
fs.writeFileSync(jsonPath, JSON.stringify(unique, null, 2));
console.log(`\nSaved ${unique.length} unique agents to ${jsonPath}`);

// Save CSV
const headers = ['name', 'location', 'ads', 'verified', 'url'];
const csv = [
  headers.join(','),
  ...unique.map(a => headers.map(h => `"${String(a[h] || '').replace(/"/g, '""')}"`).join(','))
].join('\n');
const csvPath = path.join(dataDir, 'cyprus-agents-bazaraki.csv');
fs.writeFileSync(csvPath, csv);
console.log(`Saved CSV to ${csvPath}`);

// Stats
const byLocation = {};
unique.forEach(a => byLocation[a.location] = (byLocation[a.location] || 0) + 1);
console.log('\nBy location:', byLocation);
console.log('Total ads:', unique.reduce((sum, a) => sum + a.ads, 0));
