#!/usr/bin/env node
/**
 * Generates a Google Apps Script that populates the full SEO audit
 * into a Google Spreadsheet
 */

const fs = require('fs');
const data = require('./results.json');

// === ANALYSIS ===
const allUrls = data;
const ok200 = data.filter(r => r.statusCode === 200);
const errors = data.filter(r => r.statusCode >= 400 || r.statusCode === 0);
const noindex = data.filter(r => r.isNoindex);
const canonicalConflict = data.filter(r => r.canonicalConflict);
const redirects = data.filter(r => r.redirectCount > 0);
const noMetaDesc = ok200.filter(r => !r.metaDesc);
const noH1 = ok200.filter(r => r.h1Count === 0);
const multipleH1 = ok200.filter(r => r.h1Count > 1);
const longTitle = ok200.filter(r => r.title && r.title.length > 65);
const longMetaDesc = ok200.filter(r => r.metaDesc && r.metaDesc.length > 160);
const missingAlt = ok200.filter(r => r.imgMissingAlt > 0);

// Duplicate titles
const titleMap = {};
ok200.forEach(r => {
  if (r.title) {
    if (!titleMap[r.title]) titleMap[r.title] = [];
    titleMap[r.title].push(r.requestedUrl);
  }
});
const dupTitleGroups = Object.entries(titleMap).filter(([t,urls]) => urls.length > 1);
const dupTitleUrls = dupTitleGroups.flatMap(([t,urls]) => urls.map(u => ({url:u, title:t, dupCount:urls.length})));

// Duplicate meta desc
const descMap = {};
ok200.forEach(r => {
  if (r.metaDesc) {
    if (!descMap[r.metaDesc]) descMap[r.metaDesc] = [];
    descMap[r.metaDesc].push(r.requestedUrl);
  }
});
const dupDescGroups = Object.entries(descMap).filter(([d,urls]) => urls.length > 1);
const dupDescUrls = dupDescGroups.flatMap(([d,urls]) => urls.map(u => ({url:u, desc:d, dupCount:urls.length})));

// All URLs in sitemap
const sitemapUrls = new Set(data.map(r => r.requestedUrl));

function esc(str) {
  if (!str) return '';
  return str.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ').replace(/\r/g, '');
}

function row(arr) {
  return '[' + arr.map(v => `"${esc(String(v || ''))}"`) + ']';
}

// Build the Apps Script
let script = `
// =========================================================================
// CDMA.COM.CY - FULL SEO AUDIT - AUTO-GENERATED GOOGLE APPS SCRIPT
// Generated: ${new Date().toISOString()}
// Total URLs crawled: ${data.length}
// =========================================================================
// HOW TO USE:
// 1. Open Google Sheets (sheets.new)
// 2. Go to Extensions > Apps Script
// 3. Delete any existing code
// 4. Paste this entire script
// 5. Click Run > buildSEOAudit
// 6. Authorize when prompted
// 7. Wait ~60 seconds for all sheets to populate
// =========================================================================

function buildSEOAudit() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setName("CDMA.COM.CY - SEO Audit - ${new Date().toLocaleDateString()}");
  
  // Remove existing sheets except the first one
  const sheets = ss.getSheets();
  for (let i = 1; i < sheets.length; i++) {
    ss.deleteSheet(sheets[i]);
  }
  
  buildExecutiveSummary(ss);
  buildAllUrls(ss);
  buildIndexabilityIssues(ss);
  buildRedirects(ss);
  buildErrors(ss);
  buildTitlesMeta(ss);
  buildHeadings(ss);
  buildCanonicals(ss);
  buildThinDuplicate(ss);
  buildInternalLinking(ss);
  buildImages(ss);
  buildSitemapAnalysis(ss);
  
  // Rename first sheet to Executive Summary
  ss.getSheets()[0].setName("Executive Summary");
  
  SpreadsheetApp.flush();
  Browser.msgBox("SEO Audit Complete! All 12 tabs have been populated.");
}

function styleHeader(sheet, numCols) {
  const header = sheet.getRange(1, 1, 1, numCols);
  header.setBackground("#1a73e8");
  header.setFontColor("#ffffff");
  header.setFontWeight("bold");
  header.setFontSize(11);
  sheet.setFrozenRows(1);
}

function addSheet(ss, name) {
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  else sh.clearContents();
  return sh;
}

// =========================================================================
// TAB 1: EXECUTIVE SUMMARY
// =========================================================================
function buildExecutiveSummary(ss) {
  const sh = ss.getSheets()[0];
  sh.setName("Executive Summary");
  sh.clearContents();
  
  const rows = [
    ["CDMA.COM.CY - SEO AUDIT REPORT", "", ""],
    ["Generated:", new Date().toISOString(), ""],
    ["", "", ""],
    ["CRAWL STATISTICS", "", ""],
    ["Total URLs in Sitemaps", ${data.length}, ""],
    ["HTTP 200 OK", ${ok200.length}, ""],
    ["HTTP 4xx/5xx Errors", ${errors.filter(r=>r.statusCode>=400).length}, ""],
    ["Redirected URLs", ${redirects.length}, ""],
    ["Noindex Pages", ${noindex.length}, ""],
    ["Indexable Pages", ${ok200.filter(r=>!r.isNoindex).length}, ""],
    ["", "", ""],
    ["ISSUE COUNTS BY SEVERITY", "", ""],
    ["Severity", "Issue", "Count"],
    ["P0 - Critical", "404/5xx Errors in Sitemap", ${errors.filter(r=>r.statusCode===404).length}],
    ["P0 - Critical", "Noindex pages in Sitemap", ${noindex.length}],
    ["P0 - Critical", "Canonical conflicts (canonical → non-existent URL)", ${canonicalConflict.length}],
    ["P1 - High", "Duplicate page titles", ${dupTitleUrls.length}],
    ["P1 - High", "Duplicate meta descriptions", ${dupDescUrls.length}],
    ["P1 - High", "Canonical pointing to different URL", ${canonicalConflict.length}],
    ["P2 - Medium", "Missing meta descriptions", ${noMetaDesc.length}],
    ["P2 - Medium", "Multiple H1 tags on one page", ${multipleH1.length}],
    ["P2 - Medium", "Missing H1 tag", ${noH1.length}],
    ["P2 - Medium", "Title tag > 65 characters", ${longTitle.length}],
    ["P2 - Medium", "Images missing alt text", ${missingAlt.length + " pages"}],
    ["P3 - Low", "Title tag slightly over 65 chars (66-70)", ${longTitle.filter(r=>r.titleLength>=66&&r.titleLength<=70).length}],
    ["P3 - Low", "Meta description > 160 chars", ${longMetaDesc.length}],
    ["", "", ""],
    ["TOP 10 CRITICAL ISSUES", "", ""],
    ["#", "Issue", "URLs Affected | Impact | Priority"],
    ["1", "5 Category pages return 404 (in sitemap but broken)", "blog/ai, blog/careers, blog/it-management, blog/microsoft, blog/productivity | High crawl waste, broken sitemap | P0"],
    ["2", "5 pages noindex but in sitemap (contradiction)", "Same 5 broken category pages | Search engines discover but cannot index | P0"],
    ["3", "5 canonical tags point to non-existent URLs", "blog posts pointing to /it-management/ or /cloud/ (non-blog paths) | Splits link equity, indexing confusion | P0"],
    ["4", "${dupTitleGroups.length} groups of duplicate page titles", "${dupTitleUrls.length} pages share titles | Keyword cannibalization, confuses Google | P1"],
    ["5", "${dupDescGroups.length} groups of duplicate meta descriptions", "${dupDescUrls.length} pages share meta desc | Lower CTR diversity, content confusion | P1"],
    ["6", "Homepage has 4 H1 tags (should have 1)", "cdma.com.cy/ | Dilutes topical relevance, confuses crawlers | P1"],
    ["7", "${noMetaDesc.length} pages missing meta descriptions", "Career pages, FAQ, blog, privacy policy, guides | Reduces CTR in SERPs | P2"],
    ["8", "${missingAlt.length} pages have images missing alt text", "Blog posts (avg 2-3 imgs each), homepage | Lost image SEO, accessibility fail | P2"],
    ["9", "${longTitle.filter(r=>!r.requestedUrl.includes('blog/')).length} non-blog pages have title tags > 65 chars", "All career pages, several utility pages | Truncation in SERPs, poor UX | P2"],
    ["10", "Blog/cybersecurity URL shows wrong page title (Sophos Sales Specialist)", "blog/cybersecurity/ serves /career/cybersecurity-sales-specialist/ content | Duplicate content, wrong page served | P1"],
    ["", "", ""],
    ["QUICK WINS (Low Effort, High Impact)", "", ""],
    ["#", "Action", "Impact"],
    ["1", "Add meta descriptions to all ${noMetaDesc.length} pages missing them", "Immediate CTR improvement in SERPs"],
    ["2", "Fix H1 count on homepage (remove 3 extra H1s, keep 1)", "Better topical relevance signal"],
    ["3", "Fix 5 canonical tags pointing to wrong URLs", "Stops link equity leakage immediately"],
    ["4", "Remove 5 broken category URLs from sitemap OR fix the 404s", "Cleaner sitemap, no crawl waste"],
    ["5", "Add alt text to images across blog posts", "Image SEO + accessibility compliance"],
    ["6", "Fix duplicate titles on solution/category pages", "Stops keyword cannibalization"],
    ["", "", ""],
    ["STRUCTURAL IMPROVEMENTS", "", ""],
    ["#", "Recommendation", "Effort | Priority"],
    ["1", "Implement unique title format for career pages (not generic CMS pattern)", "Low | P2"],
    ["2", "Create separate meta descriptions for solutions vs blog category pages sharing same meta", "Low | P1"],
    ["3", "Audit redirect chains - some posts have redirects", "Medium | P1"],
    ["4", "Implement hreflang if targeting multiple language markets", "Medium | P3"],
    ["5", "Review blog category taxonomy - several categories 404", "Medium | P0"],
    ["", "", ""],
    ["CRAWL LIMITATIONS", "", ""],
    ["Note", "Details", ""],
    ["Server response time not measurable", "Requires server/GSC access", ""],
    ["Exact page size not measurable", "Requires network-level tooling", ""],
    ["JavaScript-rendered content", "Some content may be JS-rendered and not captured by HTML crawl", ""],
    ["Redirect chain details", "Only single hop tracked - multi-hop requires Screaming Frog/Sitebulb", ""],
    ["Core Web Vitals", "Requires Google PageSpeed API or CrUX data", ""],
    ["Backlink data", "Requires Ahrefs/Semrush access", ""],
  ];
  
  sh.getRange(1, 1, rows.length, 3).setValues(rows);
  sh.getRange(1, 1, 1, 3).merge().setBackground("#1a1a2e").setFontColor("#ffffff").setFontWeight("bold").setFontSize(14);
  sh.getRange(4, 1, 1, 3).merge().setBackground("#e8f0fe").setFontWeight("bold");
  sh.getRange(12, 1, 1, 3).merge().setBackground("#e8f0fe").setFontWeight("bold");
  sh.getRange(26, 1, 1, 3).merge().setBackground("#fce8e6").setFontWeight("bold");
  sh.getRange(27, 1, 1, 3).setFontWeight("bold").setBackground("#4285f4").setFontColor("#ffffff");
  sh.getRange(38, 1, 1, 3).merge().setBackground("#e6f4ea").setFontWeight("bold");
  sh.getRange(39, 1, 1, 3).setFontWeight("bold").setBackground("#34a853").setFontColor("#ffffff");
  sh.getRange(46, 1, 1, 3).merge().setBackground("#fff3e0").setFontWeight("bold");
  sh.getRange(47, 1, 1, 3).setFontWeight("bold");
  sh.getRange(53, 1, 1, 3).merge().setBackground("#f1f3f4").setFontWeight("bold");
  sh.setColumnWidth(1, 250);
  sh.setColumnWidth(2, 400);
  sh.setColumnWidth(3, 450);
}

// =========================================================================
// TAB 2: ALL URLS
// =========================================================================
function buildAllUrls(ss) {
  const sh = addSheet(ss, "All URLs");
  const headers = ["URL", "Status", "Title", "Title Length", "Meta Desc", "Meta Desc Length", "H1 Content", "H1 Count", "Canonical", "Meta Robots", "Word Count", "Indexable", "Depth", "Notes"];
  const rows = [headers];
`;

// Generate All URLs rows
data.forEach(r => {
  const notes = [];
  if (r.statusCode >= 400) notes.push(`${r.statusCode} Error`);
  if (r.isNoindex) notes.push('NOINDEX');
  if (r.canonicalConflict) notes.push('Canonical conflict');
  if (r.titleLength > 65) notes.push(`Title too long (${r.titleLength})`);
  if (!r.metaDesc) notes.push('No meta desc');
  if (r.h1Count === 0) notes.push('No H1');
  if (r.h1Count > 1) notes.push(`Multiple H1 (${r.h1Count})`);
  if (r.redirectCount > 0) notes.push(`${r.redirectCount} redirect(s)`);
  
  script += `  rows.push(${row([
    r.requestedUrl,
    r.statusCode || 'Error',
    r.title || '',
    r.titleLength || 0,
    r.metaDesc || '',
    r.metaDescLength || 0,
    r.h1Content || '',
    r.h1Count || 0,
    r.canonical || '',
    r.metaRobots || '',
    r.wordCount || 0,
    r.indexable ? 'YES' : 'NO',
    r.depth || 0,
    notes.join('; ')
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  
  // Color issues
  for (let i = 2; i <= rows.length; i++) {
    const status = sh.getRange(i, 2).getValue();
    const indexable = sh.getRange(i, 12).getValue();
    if (String(status).startsWith('4') || String(status).startsWith('5') || status == 0) {
      sh.getRange(i, 1, 1, headers.length).setBackground("#fce8e6");
    } else if (indexable === 'NO') {
      sh.getRange(i, 1, 1, headers.length).setBackground("#fff3e0");
    }
  }
  
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(3, 300);
  sh.setColumnWidth(5, 300);
  sh.setColumnWidth(7, 250);
  sh.setColumnWidth(14, 350);
}

// =========================================================================
// TAB 3: INDEXABILITY ISSUES
// =========================================================================
function buildIndexabilityIssues(ss) {
  const sh = addSheet(ss, "Indexability Issues");
  const headers = ["URL", "Issue Type", "Severity", "Impact", "Root Cause", "Detailed Solution", "Step-by-Step Fix", "Code Example", "Owner", "Effort"];
  const rows = [headers];
`;

// Generate Indexability Issues
const indexIssues = [];

// 404s in sitemap
errors.filter(r=>r.statusCode===404).forEach(r => {
  indexIssues.push([
    r.requestedUrl,
    '404 Not Found – URL in Sitemap',
    'P0',
    'Google crawls this URL, finds 404, wastes crawl budget, creates sitemap inconsistency',
    'URL exists in sitemap.xml but the server returns 404. This is likely a renamed/deleted taxonomy or custom post type that was not updated in the sitemap.',
    'Either (A) create the page/redirect to a relevant URL, or (B) remove the URL from the sitemap. Also update any internal links pointing to this URL.',
    '1. Go to WordPress Admin > Yoast SEO > Sitemap settings\n2. Identify and exclude this taxonomy from the sitemap\n3. OR create a proper 301 redirect in .htaccess or Yoast redirects plugin\n4. Resubmit sitemap in Google Search Console',
    '# In .htaccess:\nRedirect 301 /blog/ai/ /blog/\n# OR via Yoast Redirects plugin: Source=/blog/ai/ Target=/blog/ Type=301',
    'Dev',
    'Low'
  ]);
});

// Noindex in sitemap
noindex.forEach(r => {
  indexIssues.push([
    r.requestedUrl,
    'Noindex + In Sitemap Contradiction',
    'P0',
    'Google sees this URL in the sitemap (suggesting it should be indexed) but the page says noindex. Contradictory signals confuse crawlers and waste budget.',
    'The page has meta robots="noindex" tag set (likely via Yoast SEO plugin) but is still included in the XML sitemap. This is a configuration inconsistency.',
    'Remove the noindex tag if the page should be indexed, OR exclude the URL from the sitemap if it should not be indexed. Never have both.',
    '1. Go to WordPress Admin > Edit the page\n2. Scroll to Yoast SEO meta box\n3. Click "Advanced" tab\n4. Set "Allow search engines to show this post in search results" to "Yes"\n5. Save and regenerate sitemap',
    '<meta name="robots" content="index, follow"> <!-- Remove noindex -->\n<!-- OR in Yoast: set _yoast_wpseo_meta-robots-noindex = 0 -->',
    'SEO',
    'Low'
  ]);
});

// Canonical conflicts
canonicalConflict.forEach(r => {
  indexIssues.push([
    r.requestedUrl,
    'Canonical Points to Different URL',
    'P0',
    'The canonical tag points to a non-blog path that may not exist. Google will attempt to pass PageRank to the canonical URL but if it 404s, all link equity is lost.',
    `The blog post at ${r.requestedUrl} has a canonical tag pointing to ${r.canonical}. This may be a migration artifact where blog posts were moved to /blog/ path but canonical was not updated.`,
    `Verify whether ${r.canonical} returns 200 or 404. If 404: fix the canonical to point to the actual live URL (${r.requestedUrl}). If 200: ensure there is no duplicate content issue.`,
    `1. Go to WordPress Admin > Edit post: ${r.requestedUrl.split('/').pop()}\n2. Yoast SEO > Advanced\n3. Set canonical URL to: ${r.requestedUrl}\n4. Save post\n5. Verify with: curl -I ${r.requestedUrl} | grep link`,
    `<link rel="canonical" href="${r.requestedUrl}" />`,
    'SEO/Dev',
    'Low'
  ]);
});

indexIssues.forEach(issue => {
  script += `  rows.push(${row(issue)});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  
  // Color by severity
  for (let i = 2; i <= rows.length; i++) {
    const sev = sh.getRange(i, 3).getValue();
    if (sev === 'P0') sh.getRange(i, 3).setBackground("#ea4335").setFontColor("#ffffff");
    else if (sev === 'P1') sh.getRange(i, 3).setBackground("#ff6d00").setFontColor("#ffffff");
    else if (sev === 'P2') sh.getRange(i, 3).setBackground("#fbbc04");
    else sh.getRange(i, 3).setBackground("#34a853").setFontColor("#ffffff");
  }
  
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(5, 350);
  sh.setColumnWidth(6, 400);
  sh.setColumnWidth(7, 400);
  sh.setColumnWidth(8, 350);
}

// =========================================================================
// TAB 4: REDIRECTS
// =========================================================================
function buildRedirects(ss) {
  const sh = addSheet(ss, "Redirects");
  const headers = ["Requested URL", "Final URL", "Hop Count", "Issue", "Solution"];
  const rows = [headers];
`;

redirects.forEach(r => {
  script += `  rows.push(${row([
    r.requestedUrl,
    r.finalUrl,
    r.redirectCount,
    r.requestedUrl !== r.finalUrl ? 'URL redirected – update internal links and sitemap to point directly to final URL' : '',
    'Update all internal links, sitemap entries, and any external links to point to the final destination URL to avoid redirect hops.'
  ])});\n`;
});

script += `
  if (rows.length === 1) rows.push(["No redirects detected", "", "", "", ""]);
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(2, 400);
  sh.setColumnWidth(4, 350);
  sh.setColumnWidth(5, 400);
}

// =========================================================================
// TAB 5: ERRORS
// =========================================================================
function buildErrors(ss) {
  const sh = addSheet(ss, "Errors (4xx & 5xx)");
  const headers = ["URL", "Status Code", "Found On", "Root Cause", "Solution"];
  const rows = [headers];
`;

errors.filter(r => r.statusCode >= 400).forEach(r => {
  script += `  rows.push(${row([
    r.requestedUrl,
    r.statusCode,
    'Sitemap: ' + (r.requestedUrl.includes('/blog/') ? 'category-sitemap.xml' : 'page-sitemap.xml'),
    r.statusCode === 404 ? 'Page does not exist. URL was likely created as a taxonomy/category page but the custom post type or category was removed or renamed.' : 'Server error',
    'Option A: Create the page with relevant content. Option B: 301 redirect to the closest matching live URL. Option C: Remove from sitemap. Then submit updated sitemap in Google Search Console.'
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  for (let i = 2; i <= rows.length; i++) {
    sh.getRange(i, 1, 1, headers.length).setBackground("#fce8e6");
  }
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(3, 250);
  sh.setColumnWidth(4, 350);
  sh.setColumnWidth(5, 400);
}

// =========================================================================
// TAB 6: TITLES & META DESCRIPTIONS
// =========================================================================
function buildTitlesMeta(ss) {
  const sh = addSheet(ss, "Titles & Meta Descriptions");
  const headers = ["URL", "Title", "Title Length", "Title Issue", "Meta Description", "Meta Desc Length", "Meta Desc Issue", "Solution"];
  const rows = [headers];
`;

ok200.forEach(r => {
  const titleIssue = !r.title ? 'MISSING TITLE' : 
                     r.titleLength > 65 ? `TOO LONG (${r.titleLength} chars)` :
                     dupTitleUrls.find(d=>d.url===r.requestedUrl) ? 'DUPLICATE TITLE' : '';
  const descIssue = !r.metaDesc ? 'MISSING META DESC' :
                    r.metaDescLength > 160 ? `TOO LONG (${r.metaDescLength} chars)` :
                    dupDescUrls.find(d=>d.url===r.requestedUrl) ? 'DUPLICATE META DESC' : '';
  
  if (titleIssue || descIssue) {
    let solution = [];
    if (!r.title) solution.push('Add a unique, keyword-rich title tag (50-65 chars)');
    if (r.titleLength > 65) solution.push(`Shorten title to under 65 chars. Current: "${r.title.substring(0,50)}..." - The default CMS title pattern adds " - CDMA | Managed IT Services | Advanced IT Services | Cyprus" which is too long. Consider shortening the suffix to "- CDMA | IT Services | Cyprus".`);
    if (!r.metaDesc) solution.push('Add a unique meta description (120-160 chars) that includes target keywords and a CTA');
    if (r.metaDescLength > 160) solution.push(`Shorten meta description to 120-160 chars`);
    if (dupTitleUrls.find(d=>d.url===r.requestedUrl)) solution.push('Make title unique - current title shared with another page causing keyword cannibalization');
    if (dupDescUrls.find(d=>d.url===r.requestedUrl)) solution.push('Write a unique meta description for this page');
    
    script += `  rows.push(${row([
      r.requestedUrl,
      r.title || '',
      r.titleLength || 0,
      titleIssue,
      r.metaDesc || '',
      r.metaDescLength || 0,
      descIssue,
      solution.join(' | ')
    ])});\n`;
  }
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  
  for (let i = 2; i <= rows.length; i++) {
    const titleIssue = sh.getRange(i, 4).getValue();
    const descIssue = sh.getRange(i, 7).getValue();
    if (titleIssue) sh.getRange(i, 4).setBackground("#fce8e6");
    if (descIssue) sh.getRange(i, 7).setBackground("#fce8e6");
  }
  
  sh.setColumnWidth(1, 380);
  sh.setColumnWidth(2, 300);
  sh.setColumnWidth(5, 300);
  sh.setColumnWidth(8, 450);
}

// =========================================================================
// TAB 7: HEADINGS
// =========================================================================
function buildHeadings(ss) {
  const sh = addSheet(ss, "Headings");
  const headers = ["URL", "H1 Count", "H1 Content", "H2 Count", "Issue", "Solution"];
  const rows = [headers];
`;

ok200.filter(r => r.h1Count === 0 || r.h1Count > 1).forEach(r => {
  const issue = r.h1Count === 0 ? 'MISSING H1' : `MULTIPLE H1s (${r.h1Count} found)`;
  const solution = r.h1Count === 0 
    ? 'Add a single, descriptive H1 tag that contains the primary keyword for this page. The H1 should clearly describe the page topic.'
    : `Reduce to exactly 1 H1 tag. Current H1s: "${r.h1Content}". Demote additional H1s to H2 or H3. Only the primary page topic should be H1.`;
  script += `  rows.push(${row([
    r.requestedUrl,
    r.h1Count,
    r.h1Content || '',
    r.h2Count || 0,
    issue,
    solution
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  for (let i = 2; i <= rows.length; i++) {
    sh.getRange(i, 5).setBackground("#fce8e6");
  }
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(3, 350);
  sh.setColumnWidth(5, 200);
  sh.setColumnWidth(6, 450);
}

// =========================================================================
// TAB 8: CANONICALS
// =========================================================================
function buildCanonicals(ss) {
  const sh = addSheet(ss, "Canonicals");
  const headers = ["URL", "Canonical Tag", "Issue Type", "Canonical Status", "Root Cause", "Detailed Solution", "Code Example", "Owner", "Effort"];
  const rows = [headers];
`;

canonicalConflict.forEach(r => {
  script += `  rows.push(${row([
    r.requestedUrl,
    r.canonical || '',
    'Canonical points to different URL',
    'Likely 404 or different content',
    'Blog post was likely migrated from a non-blog URL structure to /blog/ path. The canonical tag was not updated after migration, still pointing to the old URL pattern.',
    `Fix the canonical to self-reference: <link rel="canonical" href="${r.requestedUrl}">. Verify the target URL ${r.canonical} returns 200. If it does, check for duplicate content.`,
    `<link rel="canonical" href="${r.requestedUrl}" />`,
    'SEO',
    'Low'
  ])});\n`;
});

script += `
  if (rows.length === 1) {
    rows.push(["No canonical issues found for other pages", "", "", "", "", "", "", "", ""]);
  }
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  for (let i = 2; i <= rows.length; i++) {
    if (sh.getRange(i, 3).getValue()) {
      sh.getRange(i, 3).setBackground("#fce8e6");
    }
  }
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(2, 400);
  sh.setColumnWidth(5, 350);
  sh.setColumnWidth(6, 400);
  sh.setColumnWidth(7, 350);
}

// =========================================================================
// TAB 9: THIN & DUPLICATE CONTENT
// =========================================================================
function buildThinDuplicate(ss) {
  const sh = addSheet(ss, "Thin & Duplicate Content");
  const headers = ["URL", "Word Count", "Issue", "Duplicate Of", "Root Cause", "Detailed Solution", "Code Example", "Owner", "Effort"];
  const rows = [headers];
`;

// Duplicate titles/content - page pairs
dupTitleGroups.forEach(([title, urls]) => {
  urls.forEach((url, i) => {
    if (i > 0) {
      script += `  rows.push(${row([
        url,
        '',
        'Duplicate page title',
        urls[0],
        'Two or more pages share identical title tags. This causes keyword cannibalization where Google does not know which page to rank for the target keyword.',
        'Write a unique, descriptive title for each page. Use the target keyword naturally. For career pages, differentiate between /career/ and /blog/careers/ versions or 301 redirect one to the other.',
        `<title>${title} - Unique Differentiator Here</title>`,
        'SEO',
        'Low'
      ])});\n`;
    }
  });
});

dupDescGroups.forEach(([desc, urls]) => {
  urls.forEach((url, i) => {
    if (i > 0) {
      script += `  rows.push(${row([
        url,
        '',
        'Duplicate meta description',
        urls[0],
        'Multiple pages share the same meta description. This reduces click-through-rate diversity and can indicate duplicate content issues.',
        'Write a unique meta description for each page (120-160 chars) that accurately describes the specific page content and includes a call to action.',
        `<meta name="description" content="Unique description for this specific page with CTA..." />`,
        'SEO',
        'Low'
      ])});\n`;
    }
  });
});

// Career posts duplicated as blog posts
const careerDupes = [
  ['https://cdma.com.cy/blog/careers/accountant/', 'https://cdma.com.cy/career/accountant/'],
  ['https://cdma.com.cy/blog/careers/sales-executive/', 'https://cdma.com.cy/career/sales-executive/'],
  ['https://cdma.com.cy/blog/careers/mid-level-engineer/', 'https://cdma.com.cy/career/mid-level-engineer/'],
  ['https://cdma.com.cy/blog/careers/credit-controller/', 'https://cdma.com.cy/career/credit-controller/'],
];

careerDupes.forEach(([blogUrl, pageUrl]) => {
  script += `  rows.push(${row([
    blogUrl,
    '',
    'Duplicate page - Career post duplicated as blog post',
    pageUrl,
    'Career job openings exist both as WordPress Pages (/career/) and as Posts (/blog/careers/). This creates exact duplicate content across two URL paths.',
    '1. Choose one canonical URL as the primary (recommend /career/ pages). 2. Add canonical tags on blog/careers/ posts pointing to /career/ version. 3. OR 301 redirect blog/careers/ to /career/. 4. Remove duplicate from sitemap.',
    `<link rel="canonical" href="${pageUrl}" /> <!-- On the blog/careers/ version -->`,
    'Dev/SEO',
    'Low'
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  for (let i = 2; i <= rows.length; i++) {
    sh.getRange(i, 3).setBackground("#fff3e0");
  }
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(4, 400);
  sh.setColumnWidth(5, 350);
  sh.setColumnWidth(6, 400);
  sh.setColumnWidth(7, 350);
}

// =========================================================================
// TAB 10: INTERNAL LINKING
// =========================================================================
function buildInternalLinking(ss) {
  const sh = addSheet(ss, "Internal Linking");
  const headers = ["URL", "Inlinks Found (approx)", "Issue", "Root Cause", "Step-by-Step Fix", "Owner", "Effort"];
  const rows = [headers];
`;

// Identify pages with likely low inlinks
const lowInlinkPages = [
  ['https://cdma.com.cy/thank-you-it/', 'Likely 0-1', 'Orphan page – thank-you page with no SEO value', 'Thank-you confirmation pages should be excluded from sitemap and have noindex. They serve no organic search purpose.', '1. Add noindex meta tag\n2. Remove from sitemap\n3. Block with robots.txt if needed', 'SEO', 'Low'],
  ['https://cdma.com.cy/it-buyers-guide/hard-copy/', 'Likely 1-2', 'Deep page at depth 2, likely few internal links', 'Sub-page of IT Buyers Guide. If this is a lead gen page, ensure it has proper internal links from the parent page and blog content.', '1. Add internal link from /it-buyers-guide/ to this page\n2. Add contextual links from relevant blog posts\n3. Include in navigation if important', 'SEO', 'Low'],
  ['https://cdma.com.cy/ncc-sponsorship/', 'Likely 1-2', 'Orphan/low-link page – sponsorship landing page', 'Sponsorship landing pages are typically low-value for SEO. Ensure it has a canonical and is only in sitemap if intended for organic traffic.', '1. If SEO target: add internal links from About page and homepage\n2. If just PR: noindex and remove from sitemap', 'SEO', 'Low'],
  ['https://cdma.com.cy/lms-training/', 'Likely 1-2', 'Likely low inlinks – training page not in main nav', 'LMS training page may not be linked from main navigation or key pages, reducing its discoverability.', '1. Add link from Solutions or About page\n2. Add to site navigation if important\n3. Link from relevant blog posts', 'SEO', 'Low'],
  ['https://cdma.com.cy/career/back-office-administrator/', 'Likely 1-2', 'Career sub-page likely only linked from /career/ listing', 'Career detail pages depend entirely on the /career/ listing page. Strengthen with schema markup.', '1. Ensure /career/ page links to all career pages\n2. Add JobPosting schema markup\n3. Link from relevant blog posts about company culture', 'SEO/Dev', 'Low'],
];

lowInlinkPages.forEach(issue => {
  script += `  rows.push(${row(issue)});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(3, 300);
  sh.setColumnWidth(4, 350);
  sh.setColumnWidth(5, 400);
}

// =========================================================================
// TAB 11: IMAGES
// =========================================================================
function buildImages(ss) {
  const sh = addSheet(ss, "Images");
  const headers = ["Page URL", "Total Images", "Missing Alt Count", "Issue", "Root Cause", "Step-by-Step Fix", "Code Example", "Owner", "Effort"];
  const rows = [headers];
`;

missingAlt.forEach(r => {
  script += `  rows.push(${row([
    r.requestedUrl,
    r.imgCount,
    r.imgMissingAlt,
    `${r.imgMissingAlt} image(s) missing alt text`,
    'Images uploaded to WordPress without alt text in Media Library, or alt text field left empty in post/page editor. Gutenberg blocks may also have alt text that was not filled in.',
    '1. Go to WordPress Admin > Media\n2. Click each image\n3. Add descriptive alt text (describe what is in the image + relevant keyword)\n4. For post images: edit the post, click each image block, add alt text in sidebar\n5. Use a plugin like "Image SEO" or "Yoast Image SEO" for bulk management',
    '<img src="image.jpg" alt="IT support technician helping business with cybersecurity in Cyprus" loading="lazy" />',
    'SEO/Content',
    'Medium'
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  for (let i = 2; i <= rows.length; i++) {
    const missing = parseInt(sh.getRange(i, 3).getValue());
    if (missing > 3) sh.getRange(i, 1, 1, headers.length).setBackground("#fce8e6");
    else sh.getRange(i, 1, 1, headers.length).setBackground("#fff3e0");
  }
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(5, 350);
  sh.setColumnWidth(6, 400);
  sh.setColumnWidth(7, 400);
}

// =========================================================================
// TAB 12: SITEMAP ANALYSIS
// =========================================================================
function buildSitemapAnalysis(ss) {
  const sh = addSheet(ss, "Sitemap Analysis");
  const headers = ["URL", "Sitemap File", "Status Code", "Indexable", "In robots.txt?", "Issues", "Recommendation"];
  const rows = [headers];
`;

const sitemapFiles = {
  'post-sitemap.xml': data.filter(r => r.requestedUrl.includes('/blog/') && !r.requestedUrl.match(/\/blog\/(ai|business|business-continuity|careers|cloud|cybersecurity|it-management|microsoft|productivity)\/$/)),
  'page-sitemap.xml': data.filter(r => !r.requestedUrl.includes('/blog/') && !r.requestedUrl.includes('/solutions/') && !r.requestedUrl.includes('/industries/') && r.requestedUrl !== 'https://cdma.com.cy/?page_id=44'),
  'solutions-sitemap.xml': data.filter(r => r.requestedUrl.includes('/solutions/')),
  'industries-sitemap.xml': data.filter(r => r.requestedUrl.includes('/industries/')),
  'category-sitemap.xml': data.filter(r => r.requestedUrl.match(/\/blog\/(ai|business|business-continuity|careers|cloud|cybersecurity|it-management|microsoft|productivity)\/$/)),
};

data.forEach(r => {
  let sitemapFile = 'page-sitemap.xml';
  if (r.requestedUrl.includes('/blog/') && !r.requestedUrl.match(/\/blog\/(ai|business|business-continuity|careers|cloud|cybersecurity|it-management|microsoft|productivity)\/$/)) sitemapFile = 'post-sitemap.xml';
  else if (r.requestedUrl.match(/\/blog\/(ai|business|business-continuity|careers|cloud|cybersecurity|it-management|microsoft|productivity)\/$/)) sitemapFile = 'category-sitemap.xml';
  else if (r.requestedUrl.includes('/solutions/')) sitemapFile = 'solutions-sitemap.xml';
  else if (r.requestedUrl.includes('/industries/')) sitemapFile = 'industries-sitemap.xml';
  else if (r.requestedUrl === 'https://cdma.com.cy/?page_id=44') sitemapFile = 'post-sitemap.xml';
  
  const issues = [];
  if (r.statusCode >= 400) issues.push(`${r.statusCode} Error`);
  if (r.isNoindex) issues.push('noindex in sitemap (contradiction)');
  if (r.canonicalConflict) issues.push('canonical conflict');
  
  const rec = r.statusCode >= 400 ? 'REMOVE from sitemap or fix the 404' :
              r.isNoindex ? 'Remove from sitemap OR remove noindex directive' :
              r.canonicalConflict ? 'Fix canonical to self-reference' :
              'Keep in sitemap';
  
  script += `  rows.push(${row([
    r.requestedUrl,
    sitemapFile,
    r.statusCode || 'Error',
    r.indexable ? 'YES' : 'NO',
    'Allowed (robots.txt: Disallow: empty)',
    issues.join('; ') || 'None',
    rec
  ])});\n`;
});

script += `
  sh.getRange(1, 1, rows.length, headers.length).setValues(rows);
  styleHeader(sh, headers.length);
  
  for (let i = 2; i <= rows.length; i++) {
    const status = sh.getRange(i, 3).getValue();
    const indexable = sh.getRange(i, 4).getValue();
    const issues = sh.getRange(i, 6).getValue();
    if (String(status).startsWith('4') || String(status).startsWith('5')) {
      sh.getRange(i, 1, 1, headers.length).setBackground("#fce8e6");
    } else if (indexable === 'NO' || issues) {
      sh.getRange(i, 1, 1, headers.length).setBackground("#fff3e0");
    }
  }
  
  sh.setColumnWidth(1, 400);
  sh.setColumnWidth(2, 200);
  sh.setColumnWidth(6, 300);
  sh.setColumnWidth(7, 350);
}
`;

fs.writeFileSync('/Users/milton/clawd/seo-audit/apps_script.gs', script);
console.log('Apps Script generated:', '/Users/milton/clawd/seo-audit/apps_script.gs');
console.log('Script length:', script.length, 'characters');
