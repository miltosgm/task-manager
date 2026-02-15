const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

async function convertToPdf() {
  const mdPath = '/Users/milton/clawd/projects/agent-scraper/docs/PRODUCT_DOCUMENTATION.md';
  const pdfPath = '/Users/milton/clawd/projects/agent-scraper/docs/AgentScore-Documentation.pdf';
  
  const markdown = fs.readFileSync(mdPath, 'utf8');
  const html = marked.parse(markdown);
  
  const fullHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; line-height: 1.6; }
    h1 { color: #1a1a1a; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }
    h2 { color: #333; margin-top: 30px; }
    h3 { color: #555; }
    table { border-collapse: collapse; width: 100%; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    th { background: #f5f5f5; }
    pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
    blockquote { border-left: 4px solid #0066cc; margin: 20px 0; padding-left: 20px; color: #666; }
  </style>
</head>
<body>
${html}
</body>
</html>`;

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(fullHtml);
  await page.pdf({ path: pdfPath, format: 'A4', margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' } });
  await browser.close();
  
  console.log('PDF created:', pdfPath);
}

convertToPdf().catch(console.error);
