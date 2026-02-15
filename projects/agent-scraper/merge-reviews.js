#!/usr/bin/env node
/**
 * Merge all review data from Facebook, index.cy, home.cy and other sources
 */

const fs = require('fs');
const path = require('path');

// Load original data
const inputPath = path.join(__dirname, 'all-agents-with-reviews.json');
const outputPath = path.join(__dirname, 'all-agents-all-reviews.json');

let agents = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));

// Facebook and other review data gathered from web searches
const reviewData = {
  "N.K. SmartAssets Ltd": {
    facebook_url: "https://www.facebook.com/smartassetscyprus/",
    facebook_likes: 2026
  },
  "KAZO REAL ESTATES": {
    facebook_url: "https://www.facebook.com/KazoRealEstates/"
  },
  "MySpace Real Estate": {
    facebook_url: "https://www.facebook.com/myspace.com.cy/",
    indexcy_url: "https://index.cy/company/myspace/"
  },
  "NCH REAL ESTATE": {
    facebook_url: "https://www.facebook.com/NCHRealEstateAgency/",
    facebook_reviews: 2,
    homecyprus_url: "https://home.cy/nch-real-estate/nicosia"
  },
  "Kalogirou Real Estate": {
    facebook_url: "https://www.facebook.com/p/Kalogirou-Real-Estate-100063689655416/",
    facebook_likes: 3900
  },
  "CENTURY 21": {
    facebook_url: "https://www.facebook.com/Century21CY/",
    facebook_recommendations: "100%",
    facebook_reviews: 24
  },
  "Cyprus Sothebys International Realty": {
    facebook_url: "https://www.facebook.com/CyprusSothebysRealty/",
    facebook_likes: 15063
  },
  "MPA Property Promoters & Consultants Ltd": {
    facebook_url: "https://www.facebook.com/mpapropertycy/"
  },
  "REMAX CYPRUS": {
    facebook_url: "https://www.facebook.com/REMAXCyprus/",
    facebook_recommendations: "96%",
    facebook_reviews: 20,
    homecyprus_url: "https://home.cy/remax/dealmakers"
  },
  "Life Realty Cyprus": {
    facebook_url: "https://www.facebook.com/liferealtycy/"
  },
  "CHRIS MICHAEL PROPERTY GROUP": {
    facebook_url: "https://www.facebook.com/ChrisMichaelEstates/"
  },
  "Sioferos Real Estate": {
    facebook_url: "https://www.facebook.com/sioferosrealestate/"
  },
  "Delfi Properties": {
    facebook_url: "https://www.facebook.com/DelfiPropertiesCyprus/",
    facebook_likes: 6130
  },
  "Altia": {
    facebook_url: "https://www.facebook.com/altiaestates/",
    facebook_likes: 6240,
    indexcy_url: "https://index.cy/company/altia/",
    indexcy_rating: 5.0,
    indexcy_reviews: 1,
    homecyprus_url: "https://home.cy/altia"
  },
  "SVA Estates": {
    facebook_url: "https://www.facebook.com/svaestates/",
    facebook_likes: 10548,
    indexcy_url: "https://index.cy/company/sva-estates/"
  },
  "LEPTOS ESTATES": {
    facebook_url: "https://www.facebook.com/p/Leptos-Group-100086541693201/",
    facebook_likes: 3776
  },
  "ThePropertyHouse": {
    facebook_url: "https://www.facebook.com/thepropertyhouse/",
    facebook_reviews: 2
  },
  "PAFILIA": {
    facebook_url: "https://www.facebook.com/pafiliapropertydevelopers/",
    facebook_likes: 11811
  },
  "Galaxia Estates": {
    facebook_url: "https://www.facebook.com/galaxiaestate/"
  },
  "Fox Smart Estate Agency Network LTD": {
    facebook_url: "https://www.facebook.com/FoxRealEstateCyprus/",
    facebook_likes: 16481
  },
  "Imperio Properties": {
    facebook_url: "https://www.facebook.com/imperioproperties/"
  },
  "Aristo Developers": {
    facebook_url: "https://www.facebook.com/aristodevelopers/",
    facebook_likes: 62124
  },
  "Cyprus101": {
    facebook_url: "https://www.facebook.com/Cyprus101/",
    facebook_likes: 15900
  },
  "M.Residence Ltd": {
    facebook_url: "https://www.facebook.com/M.Residence/",
    facebook_likes: 13332
  },
  "KADIS ESTATES": {
    facebook_url: "https://www.facebook.com/KadisEstates"
  },
  "Arena Properties": {
    facebook_url: "https://www.facebook.com/arenapropertiescyprus/",
    facebook_likes: 5412,
    indexcy_url: "https://index.cy/company/arena-properties/",
    homecyprus_url: "https://home.cy/arena-properties"
  },
  "SYNERGY ESTATE AGENTS": {
    facebook_url: "https://www.facebook.com/synergy.estateagents.cy/",
    facebook_likes: 5752
  },
  "Comark Estates": {
    facebook_url: "https://www.facebook.com/ComarkEstates/",
    facebook_likes: 1131
  },
  "Arto Estates": {
    facebook_url: "https://www.facebook.com/ArtoEstates/",
    facebook_likes: 1523,
    indexcy_url: "https://index.cy/company/arto-estates/",
    indexcy_rating: 5.0,
    indexcy_reviews: 1
  },
  "Marinos Kineyirou Estate Agencies Ltd": {
    facebook_url: "https://www.facebook.com/marinoskineyirouestateagencies/"
  },
  "David Spyrou Estates LTD": {
    facebook_url: "https://www.facebook.com/davidspyrouestates/",
    facebook_reviews: 3,
    homecyprus_url: "https://home.cy/david-spyrou-estates",
    indexcy_url: "https://index.cy/company/david-spyrou-estates/"
  },
  "Zourides Real Estate": {
    facebook_url: "https://www.facebook.com/p/Zourides-Real-Estate-100038889622234/",
    facebook_likes: 1591,
    indexcy_url: "https://index.cy/company/zourides-real-estate/"
  },
  "DOME REAL ESTATE": {
    facebook_url: "https://www.facebook.com/p/DOME-Real-Estate-100063492493513/",
    facebook_reviews: 3
  },
  "ChapterOne Properties Ltd": {
    facebook_url: "https://www.facebook.com/chapteroneproperties/",
    facebook_reviews: 1
  },
  "Plus Wise Estates": {
    facebook_url: "https://www.facebook.com/pluswiseestates/",
    facebook_likes: 120
  },
  "The HERITAGE": {
    facebook_url: "https://www.facebook.com/theheritagerealestateagency/",
    facebook_recommendations: "100%",
    facebook_reviews: 7
  },
  "RealDeal Estates": {
    indexcy_url: "https://index.cy/company/realdeal-estates/"
  },
  "Sabbianco Properties": {
    facebook_url: "https://www.facebook.com/SabbiancoProperties/",
    indexcy_url: "https://index.cy/company/sabbianco-properties/"
  },
  "Landbank Property Consultants Ltd": {
    facebook_url: "https://www.facebook.com/LandbankPropertyConsultants/",
    facebook_likes: 1225
  },
  "Omega Real Estate Cyprus": {
    facebook_url: "https://www.facebook.com/omegarealestatecy/",
    facebook_likes: 2567
  },
  "NICOLAOU ESTATES": {
    facebook_url: "https://www.facebook.com/nicolaouestatesnicosia/",
    facebook_likes: 1524
  },
  "P.N.NICOLAOU ESTATES LTD": {
    facebook_url: "https://www.facebook.com/nicolaouestatesnicosia/",
    facebook_likes: 1524
  },
  "GoGordian Real Estate": {
    facebook_url: "https://www.facebook.com/gogordian/",
    facebook_likes: 11766
  },
  "Sweet Home Estates": {
    facebook_url: "https://www.facebook.com/SweetHomeEstates/",
    facebook_likes: 16145
  },
  "E.G. GALLERY ESTATE": {
    facebook_url: "https://www.facebook.com/GalleryEstateA.N/",
    facebook_likes: 2894
  },
  "La Mer Estates": {
    facebook_url: "https://www.facebook.com/p/LA-Mer-Estates-100063518651903/",
    facebook_likes: 844
  },
  "Majesty Real Estate": {
    facebook_url: "https://www.facebook.com/majestycyprus/",
    facebook_likes: 674
  },
  "Cyprus Domus": {
    facebook_url: "https://www.facebook.com/cyprusdomus/",
    facebook_likes: 1864,
    indexcy_url: "https://index.cy/company/cyprus-domus/"
  },
  "DOM Real Estate": {
    facebook_url: "https://www.facebook.com/DOMCyprus/",
    facebook_likes: 11768,
    facebook_reviews: 1,
    indexcy_url: "https://index.cy/company/dom-real-estate/"
  },
  "West Coast Properties": {
    homecyprus_url: "https://home.cy/west-coast"
  },
  "G&P Lazarou Estate Agents LTD": {
    // From Google reviews data
  },
  "REInvest Real Estate": {
    // From Google reviews data
  }
};

// Enrich agents with review data
agents = agents.map(agent => {
  const extraData = reviewData[agent.name] || {};
  
  // Calculate total review count
  let totalReviews = 0;
  let ratingSum = 0;
  let ratingCount = 0;
  
  // Google reviews
  if (agent.google_review_count) {
    totalReviews += agent.google_review_count;
    if (agent.google_rating) {
      ratingSum += agent.google_rating * agent.google_review_count;
      ratingCount += agent.google_review_count;
    }
  }
  
  // Facebook reviews
  if (extraData.facebook_reviews) {
    totalReviews += extraData.facebook_reviews;
  }
  
  // Index.cy reviews
  if (extraData.indexcy_reviews) {
    totalReviews += extraData.indexcy_reviews;
    if (extraData.indexcy_rating) {
      ratingSum += extraData.indexcy_rating * extraData.indexcy_reviews;
      ratingCount += extraData.indexcy_reviews;
    }
  }
  
  // Calculate weighted average rating
  const averageRating = ratingCount > 0 ? Math.round((ratingSum / ratingCount) * 10) / 10 : null;
  
  return {
    ...agent,
    facebook_url: extraData.facebook_url || null,
    facebook_likes: extraData.facebook_likes || null,
    facebook_rating: extraData.facebook_rating || null,
    facebook_reviews: extraData.facebook_reviews || null,
    facebook_recommendations: extraData.facebook_recommendations || null,
    homecyprus_url: extraData.homecyprus_url || null,
    homecyprus_rating: extraData.homecyprus_rating || null,
    homecyprus_reviews: extraData.homecyprus_reviews || null,
    indexcy_url: extraData.indexcy_url || null,
    indexcy_rating: extraData.indexcy_rating || null,
    indexcy_reviews: extraData.indexcy_reviews || null,
    trustpilot_url: extraData.trustpilot_url || null,
    trustpilot_rating: extraData.trustpilot_rating || null,
    trustpilot_reviews: extraData.trustpilot_reviews || null,
    other_reviews: extraData.other_reviews || [],
    total_review_count: totalReviews,
    average_rating: averageRating,
    review_sources_checked: ['Google', 'Facebook', 'index.cy', 'home.cy', 'Trustpilot'],
    last_scraped: new Date().toISOString()
  };
});

// Save enriched data
fs.writeFileSync(outputPath, JSON.stringify(agents, null, 2));

// Generate statistics
const withAnyReviews = agents.filter(a => a.total_review_count > 0 || a.facebook_url);
const withFacebook = agents.filter(a => a.facebook_url);
const withGoogle = agents.filter(a => a.google_review_count > 0);
const withIndexcy = agents.filter(a => a.indexcy_url);
const withHomecyprus = agents.filter(a => a.homecyprus_url);

// Top 10 most reviewed
const topReviewed = [...agents]
  .sort((a, b) => (b.total_review_count || 0) - (a.total_review_count || 0))
  .slice(0, 10);

// Top 10 best rated (with at least 10 reviews)
const topRated = [...agents]
  .filter(a => a.total_review_count >= 10)
  .sort((a, b) => (b.average_rating || 0) - (a.average_rating || 0))
  .slice(0, 10);

// Top 10 by Facebook likes
const topFacebookLikes = [...agents]
  .filter(a => a.facebook_likes)
  .sort((a, b) => (b.facebook_likes || 0) - (a.facebook_likes || 0))
  .slice(0, 10);

console.log('=== REVIEW SCRAPING SUMMARY ===\n');
console.log(`Total agents: ${agents.length}`);
console.log(`Agents with ANY reviews/social presence: ${withAnyReviews.length}`);
console.log(`\n--- BREAKDOWN BY SOURCE ---`);
console.log(`Google Reviews: ${withGoogle.length} agents`);
console.log(`Facebook pages found: ${withFacebook.length} agents`);
console.log(`index.cy listings: ${withIndexcy.length} agents`);
console.log(`home.cy listings: ${withHomecyprus.length} agents`);

console.log(`\n--- TOP 10 MOST REVIEWED (ALL SOURCES) ---`);
topReviewed.forEach((a, i) => {
  console.log(`${i+1}. ${a.name} - ${a.total_review_count} reviews (Google: ${a.google_review_count || 0})`);
});

console.log(`\n--- TOP 10 BEST RATED (min 10 reviews) ---`);
topRated.forEach((a, i) => {
  console.log(`${i+1}. ${a.name} - ${a.average_rating}/5 (${a.total_review_count} reviews)`);
});

console.log(`\n--- TOP 10 FACEBOOK PRESENCE (BY LIKES) ---`);
topFacebookLikes.forEach((a, i) => {
  console.log(`${i+1}. ${a.name} - ${a.facebook_likes.toLocaleString()} likes`);
});

console.log(`\nOutput saved to: ${outputPath}`);
