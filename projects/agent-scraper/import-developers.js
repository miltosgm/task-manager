// Import Cyprus Developers to Supabase
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const SUPABASE_URL = 'https://sqjvwnuqbvnfvftvgzdz.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;

if (!SUPABASE_SERVICE_KEY) {
  console.error('Please set SUPABASE_SERVICE_KEY environment variable');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

// Parse CSV
function parseCSV(content) {
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.replace(/"/g, '').trim());
  const rows = [];
  
  for (let i = 1; i < lines.length; i++) {
    const values = [];
    let current = '';
    let inQuotes = false;
    
    for (const char of lines[i]) {
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.trim());
    
    const row = {};
    headers.forEach((header, idx) => {
      row[header] = values[idx] || '';
    });
    rows.push(row);
  }
  
  return rows;
}

async function main() {
  try {
    // Step 1: Add 'type' column if not exists and update existing agents
    console.log('Step 1: Checking and updating schema...');
    
    // First, let's try to update existing agents to have type='agent'
    const { error: updateError } = await supabase
      .from('agents')
      .update({ type: 'agent' })
      .is('type', null);
    
    if (updateError && !updateError.message.includes('column "type" does not exist')) {
      console.log('Note:', updateError.message);
    }
    
    // Step 2: Read developers CSV
    console.log('Step 2: Reading developers CSV...');
    const csvPath = path.join(__dirname, 'cyprus-developers.csv');
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const developers = parseCSV(csvContent);
    
    console.log(`Found ${developers.length} developers to import`);
    
    // Step 3: Transform and import developers
    console.log('Step 3: Importing developers...');
    
    const developersToInsert = developers.map(dev => ({
      name: dev.name,
      type: dev.type || 'developer',
      location: dev.location,
      google_rating: dev.google_rating ? parseFloat(dev.google_rating) : null,
      google_reviews_count: dev.google_reviews_count ? parseInt(dev.google_reviews_count) : null,
      website: dev.website || null,
      listing_count: dev.projects_count ? parseInt(dev.projects_count.replace('+', '')) : null,
      bazaraki_url: dev.linkedin || null, // Reusing this field for linkedin temporarily
    }));
    
    // Insert in batches
    const batchSize = 10;
    let inserted = 0;
    
    for (let i = 0; i < developersToInsert.length; i += batchSize) {
      const batch = developersToInsert.slice(i, i + batchSize);
      
      const { data, error } = await supabase
        .from('agents')
        .upsert(batch, { onConflict: 'name' })
        .select();
      
      if (error) {
        console.error(`Error inserting batch ${i / batchSize + 1}:`, error.message);
      } else {
        inserted += data.length;
        console.log(`Inserted batch ${i / batchSize + 1}: ${data.length} records`);
      }
    }
    
    console.log(`\nDone! Imported ${inserted} developers.`);
    
    // Step 4: Verify
    const { data: allRecords, error: countError } = await supabase
      .from('agents')
      .select('type')
      .limit(1000);
    
    if (!countError) {
      const agents = allRecords.filter(r => r.type === 'agent' || !r.type).length;
      const devs = allRecords.filter(r => r.type === 'developer').length;
      console.log(`\nDatabase now has:`);
      console.log(`- ${agents} agents`);
      console.log(`- ${devs} developers`);
      console.log(`- ${allRecords.length} total`);
    }
    
  } catch (err) {
    console.error('Error:', err);
  }
}

main();
