const fs = require('fs');

// Read the input files
const allAgents = JSON.parse(fs.readFileSync('/Users/milton/clawd/projects/agent-scraper/collected-agents.json', 'utf8'));
const enrichedAgents = JSON.parse(fs.readFileSync('/Users/milton/clawd/projects/agent-scraper/agents-enriched.json', 'utf8'));

// URLs to skip (already processed)
const skipUrls = [
  'https://www.bazaraki.com/c/SmartAssets/',
  'https://www.bazaraki.com/c/domrealestate/',
  'https://www.bazaraki.com/c/kazorealestate/',
  'https://www.bazaraki.com/c/mresidence/',
  'https://www.bazaraki.com/c/myspace/',
  'https://www.bazaraki.com/c/nch/',
  'https://www.bazaraki.com/c/kalogirourealestate/',
  'https://www.bazaraki.com/c/sothebys/',
  'https://www.bazaraki.com/c/arenapropertiesagents/',
  'https://www.bazaraki.com/c/century21/',
  'https://www.bazaraki.com/c/mpaproperty/',
  'https://www.bazaraki.com/c/LifeRealty/',
  'https://www.bazaraki.com/c/remaxcyprus/',
  'https://www.bazaraki.com/c/chrismichaelpropertygroup/',
  'https://www.bazaraki.com/c/ChapterOneProperties/'
];

// Also add URLs from enriched agents file
const enrichedUrls = enrichedAgents.map(agent => agent.url);
const allSkipUrls = [...new Set([...skipUrls, ...enrichedUrls])];

console.log(`Total agents: ${allAgents.length}`);
console.log(`Already processed: ${allSkipUrls.length}`);

// Filter out already processed agents
const remainingAgents = allAgents.filter(agent => !allSkipUrls.includes(agent.url));

console.log(`Remaining to process: ${remainingAgents.length}`);

// Sort by ads descending (most important first)
const sortedAgents = remainingAgents.sort((a, b) => b.ads - a.ads);

console.log('\nTop 10 remaining agents:');
sortedAgents.slice(0, 10).forEach((agent, index) => {
  console.log(`${index + 1}. ${agent.name} - ${agent.ads} ads`);
});

// Save the filtered and sorted list
fs.writeFileSync('/Users/milton/clawd/projects/agent-scraper/remaining-agents.json', JSON.stringify(sortedAgents, null, 2));
console.log(`\nFiltered list saved to remaining-agents.json`);