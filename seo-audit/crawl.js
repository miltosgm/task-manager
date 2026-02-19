#!/usr/bin/env node
/**
 * SEO Crawler for cdma.com.cy
 * Extracts all SEO signals from each URL
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// All URLs from sitemaps
const URLS = [
  // Pages
  'https://cdma.com.cy/',
  'https://cdma.com.cy/about/',
  'https://cdma.com.cy/contact-us/',
  'https://cdma.com.cy/why-us/',
  'https://cdma.com.cy/faqs/',
  'https://cdma.com.cy/blog/',
  'https://cdma.com.cy/solutions/',
  'https://cdma.com.cy/industries/',
  'https://cdma.com.cy/pricing-calculator/',
  'https://cdma.com.cy/downtime-calculator/',
  'https://cdma.com.cy/password-generator/',
  'https://cdma.com.cy/privacy-policy/',
  'https://cdma.com.cy/channel-partner-program/',
  'https://cdma.com.cy/free-strategy-session/',
  'https://cdma.com.cy/breached-email/',
  'https://cdma.com.cy/thank-you-it/',
  'https://cdma.com.cy/it-buyers-guide/',
  'https://cdma.com.cy/it-buyers-guide/hard-copy/',
  'https://cdma.com.cy/ncc-sponsorship/',
  'https://cdma.com.cy/cdma-cybersecurity-services/',
  'https://cdma.com.cy/lms-training/',
  // Careers
  'https://cdma.com.cy/career/',
  'https://cdma.com.cy/career/sales-executive/',
  'https://cdma.com.cy/career/credit-controller/',
  'https://cdma.com.cy/career/accountant/',
  'https://cdma.com.cy/career/mid-level-engineer/',
  'https://cdma.com.cy/career/account-manager/',
  'https://cdma.com.cy/career/cybersecurity-sales-specialist/',
  'https://cdma.com.cy/career/back-office-administrator/',
  // Solutions
  'https://cdma.com.cy/solutions/vcio/',
  'https://cdma.com.cy/solutions/vciso/',
  'https://cdma.com.cy/solutions/it-compliance/',
  'https://cdma.com.cy/solutions/cloud-services/',
  'https://cdma.com.cy/solutions/disaster-recovery/',
  'https://cdma.com.cy/solutions/vit-director/',
  'https://cdma.com.cy/solutions/strategic-planning/',
  'https://cdma.com.cy/solutions/business-continuity/',
  'https://cdma.com.cy/solutions/network-engineering/',
  'https://cdma.com.cy/solutions/security-approach/',
  'https://cdma.com.cy/solutions/it-support/',
  'https://cdma.com.cy/solutions/cloud-migration/',
  'https://cdma.com.cy/solutions/voice-engineering/',
  'https://cdma.com.cy/solutions/24x7x365-helpdesk/',
  'https://cdma.com.cy/solutions/unified-communications/',
  'https://cdma.com.cy/solutions/security-and-compliance/',
  'https://cdma.com.cy/solutions/network-operations-centre-noc-services/',
  'https://cdma.com.cy/solutions/human-risk-management/',
  'https://cdma.com.cy/solutions/managed-security-services/',
  // Industries
  'https://cdma.com.cy/industries/smbs/',
  'https://cdma.com.cy/industries/insurance/',
  'https://cdma.com.cy/industries/architecture-engineering-construction/',
  'https://cdma.com.cy/industries/fintech/',
  'https://cdma.com.cy/industries/professional-services/',
  'https://cdma.com.cy/industries/retail/',
  'https://cdma.com.cy/industries/accounting-law/',
  'https://cdma.com.cy/industries/hospitality/',
  // Blog categories
  'https://cdma.com.cy/blog/ai/',
  'https://cdma.com.cy/blog/business/',
  'https://cdma.com.cy/blog/business-continuity/',
  'https://cdma.com.cy/blog/careers/',
  'https://cdma.com.cy/blog/cloud/',
  'https://cdma.com.cy/blog/cybersecurity/',
  'https://cdma.com.cy/blog/it-management/',
  'https://cdma.com.cy/blog/microsoft/',
  'https://cdma.com.cy/blog/productivity/',
  // Blog posts
  'https://cdma.com.cy/?page_id=44',
  'https://cdma.com.cy/blog/cybersecurity/sophos-mdr-stops-ransomware-in-its-tracks-real-world-cases/',
  'https://cdma.com.cy/blog/business-continuity/noc-vs-soc-the-essential-guide-to-operations-centers/',
  'https://cdma.com.cy/blog/business/how-msps-help-it-consultants-thrive-in-2025/',
  'https://cdma.com.cy/blog/careers/accountant/',
  'https://cdma.com.cy/blog/careers/sales-executive/',
  'https://cdma.com.cy/blog/careers/mid-level-engineer/',
  'https://cdma.com.cy/blog/business/cdma-named-sophos-partner-of-the-year/',
  'https://cdma.com.cy/blog/business-continuity/why-disaster-recovery-planning-is-essential-for-your-business/',
  'https://cdma.com.cy/blog/business/benefits-of-cloud-migration-for-businesses-in-2025/',
  'https://cdma.com.cy/blog/business/why-businesses-need-proactive-it-support-maintenance/',
  'https://cdma.com.cy/blog/careers/credit-controller/',
  'https://cdma.com.cy/blog/microsoft/prepare-your-business-for-windows-10-end-of-life/',
  'https://cdma.com.cy/blog/cybersecurity/keep-confidential-exchanges-truly-private-with-microsoft-teams-new-prevent-screen-capture/',
  'https://cdma.com.cy/blog/cybersecurity/5-essential-cybersecurity-measures-for-smbs-in-2025/',
  'https://cdma.com.cy/blog/cybersecurity/how-to-use-a-password-manager-and-virtual-cards-for-zero-risk-holiday-shopping/',
  'https://cdma.com.cy/blog/ai/6-ways-to-prevent-leaking-private-data-through-public-ai-tools/',
  'https://cdma.com.cy/blog/it-management/managed-it-improves-customer-experience/',
  'https://cdma.com.cy/blog/it-management/it-asset-refresh-strategy/',
  'https://cdma.com.cy/blog/business-continuity/top-cybersecurity-threats-and-how-managed-cybersecurity-services-can-help/',
  'https://cdma.com.cy/blog/cloud/on-premise-vs-cloud-storage-making-the-right-choice/',
  'https://cdma.com.cy/blog/business-continuity/unified-communications-integration-best-practices/',
  'https://cdma.com.cy/blog/business-continuity/top-7-disaster-recovery-best-practices-for-enterprises/',
  'https://cdma.com.cy/blog/it-management/it-compliance-risk-management-best-practices/',
  'https://cdma.com.cy/blog/it-management/vciso-services-guide/',
  'https://cdma.com.cy/blog/it-management/incident-response-disaster-recovery/',
  'https://cdma.com.cy/blog/cloud/cloud-migration-plan-to-reduce-costs/',
  'https://cdma.com.cy/blog/cloud/cloud-performance-checklist-cost-efficient/',
  'https://cdma.com.cy/blog/it-management/user-experience-monitoring-improves-it-operations/',
];

function fetchPage(url) {
  return new Promise((resolve) => {
    const parsedUrl = new URL(url);
    const lib = parsedUrl.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; SEO-Auditor/1.0)',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9',
      },
      timeout: 15000,
    };
    
    let redirectCount = 0;
    
    function makeRequest(reqUrl, opts) {
      const lib2 = reqUrl.startsWith('https:') ? https : http;
      const p2 = new URL(reqUrl);
      opts.hostname = p2.hostname;
      opts.path = p2.pathname + p2.search;
      
      const req = lib2.request(opts, (res) => {
        // Handle redirects
        if ((res.statusCode === 301 || res.statusCode === 302 || res.statusCode === 307 || res.statusCode === 308) && res.headers.location && redirectCount < 5) {
          redirectCount++;
          const redirectTo = res.headers.location.startsWith('http') ? res.headers.location : new URL(res.headers.location, reqUrl).href;
          res.resume();
          makeRequest(redirectTo, opts);
          return;
        }
        
        let body = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => { body += chunk; });
        res.on('end', () => {
          resolve({
            requestedUrl: url,
            finalUrl: reqUrl,
            statusCode: res.statusCode,
            redirectCount,
            html: body,
          });
        });
      });
      
      req.on('error', (err) => {
        resolve({ requestedUrl: url, finalUrl: reqUrl, statusCode: 0, error: err.message, html: '' });
      });
      req.on('timeout', () => {
        req.destroy();
        resolve({ requestedUrl: url, finalUrl: url, statusCode: 0, error: 'timeout', html: '' });
      });
      req.end();
    }
    
    makeRequest(url, options);
  });
}

function extractSEO(data) {
  const { requestedUrl, finalUrl, statusCode, redirectCount, html, error } = data;
  
  const result = {
    requestedUrl,
    finalUrl,
    statusCode: statusCode || 0,
    redirectCount: redirectCount || 0,
    error: error || '',
  };
  
  if (!html) return result;
  
  // Title
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  result.title = titleMatch ? titleMatch[1].replace(/\s+/g, ' ').trim() : '';
  result.titleLength = result.title.length;
  
  // Meta description
  const metaDescMatch = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) ||
                        html.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i);
  result.metaDesc = metaDescMatch ? metaDescMatch[1].trim() : '';
  result.metaDescLength = result.metaDesc.length;
  
  // Meta robots
  const metaRobotsMatch = html.match(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']*)["']/i) ||
                          html.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']robots["']/i);
  result.metaRobots = metaRobotsMatch ? metaRobotsMatch[1].trim() : '';
  
  // Canonical
  const canonicalMatch = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)["']/i) ||
                         html.match(/<link[^>]+href=["']([^"']*)["'][^>]+rel=["']canonical["']/i);
  result.canonical = canonicalMatch ? canonicalMatch[1].trim() : '';
  
  // H1 tags
  const h1Matches = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)];
  result.h1Count = h1Matches.length;
  result.h1Content = h1Matches.map(m => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim()).join(' | ');
  
  // H2 tags
  const h2Matches = [...html.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)];
  result.h2Count = h2Matches.length;
  
  // OG tags
  result.ogTitle = html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']*)["']/i)?.[1] || '';
  result.ogDesc = html.match(/<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']*)["']/i)?.[1] || '';
  result.ogImage = html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']*)["']/i)?.[1] || '';
  result.hasOG = !!(result.ogTitle || result.ogDesc || result.ogImage);
  
  // Schema
  result.hasSchema = html.includes('application/ld+json') || html.includes('itemscope');
  
  // Viewport
  result.hasViewport = html.toLowerCase().includes('name="viewport"') || html.toLowerCase().includes("name='viewport'");
  
  // Hreflang
  result.hasHreflang = html.toLowerCase().includes('hreflang');
  
  // Word count (approx from body text)
  const bodyText = html.replace(/<script[\s\S]*?<\/script>/gi, '')
                       .replace(/<style[\s\S]*?<\/style>/gi, '')
                       .replace(/<[^>]+>/g, ' ')
                       .replace(/\s+/g, ' ')
                       .trim();
  result.wordCount = bodyText.split(' ').filter(w => w.length > 1).length;
  
  // Images
  const imgMatches = [...html.matchAll(/<img[^>]+>/gi)];
  result.imgCount = imgMatches.length;
  result.imgMissingAlt = imgMatches.filter(m => !m[0].match(/alt=["'][^"']+["']/i) || m[0].match(/alt=["']\s*["']/i)).length;
  
  // Internal links
  const domain = 'cdma.com.cy';
  const linkMatches = [...html.matchAll(/href=["']([^"'#?]+)["']/gi)];
  const internalLinks = linkMatches
    .map(m => m[1])
    .filter(l => l.includes(domain) || l.startsWith('/'))
    .filter(l => !l.match(/\.(css|js|png|jpg|jpeg|gif|svg|ico|pdf|webp|avif|woff|ttf)$/i))
    .map(l => l.startsWith('/') ? `https://${domain}${l}` : l);
  result.internalLinkCount = [...new Set(internalLinks)].length;
  result.internalLinks = [...new Set(internalLinks)].slice(0, 20).join('; ');
  
  // Noindex check
  result.isNoindex = !!(result.metaRobots && result.metaRobots.toLowerCase().includes('noindex'));
  
  // Canonical conflict
  result.canonicalConflict = !!(result.canonical && result.canonical !== finalUrl && result.canonical !== requestedUrl);
  
  // Indexable
  result.indexable = !result.isNoindex && statusCode === 200;
  
  // Depth (count slashes after domain)
  try {
    const u = new URL(requestedUrl);
    const parts = u.pathname.split('/').filter(p => p.length > 0);
    result.depth = parts.length;
  } catch(e) {
    result.depth = 0;
  }
  
  return result;
}

async function crawl() {
  const results = [];
  
  // Process in batches of 5
  for (let i = 0; i < URLS.length; i += 5) {
    const batch = URLS.slice(i, i + 5);
    const batchResults = await Promise.all(batch.map(url => fetchPage(url)));
    const analyzed = batchResults.map(r => extractSEO(r));
    results.push(...analyzed);
    process.stdout.write(`Crawled ${Math.min(i + 5, URLS.length)}/${URLS.length}\n`);
    // Small delay between batches
    await new Promise(r => setTimeout(r, 500));
  }
  
  // Output as JSON
  const fs = require('fs');
  fs.writeFileSync('/Users/milton/clawd/seo-audit/results.json', JSON.stringify(results, null, 2));
  console.log('Done! Results written to results.json');
  
  // Print summary
  console.log('\n=== CRAWL SUMMARY ===');
  console.log(`Total URLs: ${results.length}`);
  console.log(`200 OK: ${results.filter(r => r.statusCode === 200).length}`);
  console.log(`4xx/5xx: ${results.filter(r => r.statusCode >= 400).length}`);
  console.log(`Redirects: ${results.filter(r => r.redirectCount > 0).length}`);
  console.log(`No title: ${results.filter(r => !r.title).length}`);
  console.log(`No meta desc: ${results.filter(r => !r.metaDesc).length}`);
  console.log(`No H1: ${results.filter(r => r.h1Count === 0).length}`);
  console.log(`Noindex: ${results.filter(r => r.isNoindex).length}`);
  console.log(`Canonical conflict: ${results.filter(r => r.canonicalConflict).length}`);
  console.log(`Missing alt imgs: ${results.filter(r => r.imgMissingAlt > 0).length} pages`);
}

crawl().catch(console.error);
