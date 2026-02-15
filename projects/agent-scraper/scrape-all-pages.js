/**
 * Scrape all Bazaraki pages using browser automation
 * Run with: node scrape-all-pages.js
 */

const fs = require('fs');
const path = require('path');

// This will be populated by the browser scraping
const allAgents = [];

// Save results
function saveResults(agents) {
  const outputDir = path.join(__dirname, 'data');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Dedupe by URL
  const unique = [...new Map(agents.map(a => [a.url, a])).values()];
  
  // Add metadata
  unique.forEach(a => {
    a.source = 'bazaraki';
    a.scrapedAt = new Date().toISOString();
    a.verified = true; // All Bazaraki stores are verified
  });
  
  // Save JSON
  const jsonPath = path.join(outputDir, 'cyprus-agents-bazaraki.json');
  fs.writeFileSync(jsonPath, JSON.stringify(unique, null, 2));
  console.log(`Saved ${unique.length} agents to ${jsonPath}`);
  
  // Save CSV
  const headers = ['name', 'location', 'ads', 'url', 'source'];
  const csv = [
    headers.join(','),
    ...unique.map(a => headers.map(h => `"${String(a[h] || '').replace(/"/g, '""')}"`).join(','))
  ].join('\n');
  const csvPath = path.join(outputDir, 'cyprus-agents-bazaraki.csv');
  fs.writeFileSync(csvPath, csv);
  console.log(`Saved CSV to ${csvPath}`);
  
  // Stats
  const byLocation = {};
  unique.forEach(a => byLocation[a.location] = (byLocation[a.location] || 0) + 1);
  console.log('By location:', byLocation);
  
  return unique;
}

// If running standalone with collected data
if (process.argv[2] === '--save') {
  const dataFile = process.argv[3];
  if (dataFile && fs.existsSync(dataFile)) {
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    saveResults(data);
  }
}

module.exports = { saveResults };
