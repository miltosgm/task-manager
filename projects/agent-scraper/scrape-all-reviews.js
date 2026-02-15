#!/usr/bin/env node
/**
 * Multi-source review scraper for Cyprus real estate agents
 * Searches: Facebook, home.cy, index.cy, Trustpilot, and other sources
 */

const fs = require('fs');
const path = require('path');

// Load agents
const inputPath = path.join(__dirname, 'all-agents-with-reviews.json');
const outputPath = path.join(__dirname, 'all-agents-all-reviews.json');
const progressPath = path.join(__dirname, 'scrape-progress.json');

let agents = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));

// Sort by ads count (descending) to prioritize bigger agencies
agents.sort((a, b) => (b.ads || 0) - (a.ads || 0));

// Initialize new fields for each agent
agents = agents.map(agent => ({
  ...agent,
  facebook_url: agent.facebook_url || null,
  facebook_likes: agent.facebook_likes || null,
  facebook_rating: agent.facebook_rating || null,
  facebook_reviews: agent.facebook_reviews || null,
  facebook_recommendations: agent.facebook_recommendations || null,
  homecyprus_url: agent.homecyprus_url || null,
  homecyprus_rating: agent.homecyprus_rating || null,
  homecyprus_reviews: agent.homecyprus_reviews || null,
  indexcy_url: agent.indexcy_url || null,
  indexcy_rating: agent.indexcy_rating || null,
  indexcy_reviews: agent.indexcy_reviews || null,
  trustpilot_url: agent.trustpilot_url || null,
  trustpilot_rating: agent.trustpilot_rating || null,
  trustpilot_reviews: agent.trustpilot_reviews || null,
  other_reviews: agent.other_reviews || [],
  total_review_count: agent.total_review_count || 0,
  average_rating: agent.average_rating || null,
  review_sources_checked: agent.review_sources_checked || [],
  last_scraped: agent.last_scraped || null
}));

// Save initial structure
fs.writeFileSync(outputPath, JSON.stringify(agents, null, 2));

console.log(`Initialized ${agents.length} agents`);
console.log(`Top 20 by ad count:`);
agents.slice(0, 20).forEach((a, i) => {
  console.log(`${i+1}. ${a.name} - ${a.ads || 'N/A'} ads (${a.location})`);
});

// Count agents with 50+ ads
const bigAgents = agents.filter(a => (a.ads || 0) >= 50);
console.log(`\nAgents with 50+ ads: ${bigAgents.length}`);
console.log(`Total agents: ${agents.length}`);
