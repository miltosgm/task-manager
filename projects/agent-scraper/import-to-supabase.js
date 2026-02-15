#!/usr/bin/env node
/**
 * Import agents from JSON to Supabase
 * Run: node import-to-supabase.js
 */

const fs = require('fs');
const path = require('path');

const SUPABASE_URL = 'https://sqjvwnuqbvnfvftvgzdz.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_LxH-UyL1WE8Y8BOthTQkaA_IOfpdMZ7';

async function importAgents() {
    console.log('📥 Starting agent import to Supabase...\n');
    
    // Load agent data
    const dataPath = path.join(__dirname, 'all-agents-with-reviews.json');
    const rawData = fs.readFileSync(dataPath, 'utf8');
    const rawAgents = JSON.parse(rawData);
    console.log(`📋 Loaded ${rawAgents.length} agents from JSON\n`);
    
    // Transform to Supabase format
    const agents = rawAgents.map(agent => ({
        name: agent.name,
        location: agent.location,
        bazaraki_url: agent.url,
        listing_count: agent.ads || 0,
        google_rating: agent.google_rating || null,
        google_reviews_count: agent.google_review_count || 0
    }));
    
    console.log('🔄 Inserting agents into Supabase...\n');
    
    // Insert in batches of 50
    const batchSize = 50;
    let inserted = 0;
    let errors = [];
    
    for (let i = 0; i < agents.length; i += batchSize) {
        const batch = agents.slice(i, i + batchSize);
        
        try {
            const response = await fetch(`${SUPABASE_URL}/rest/v1/agents`, {
                method: 'POST',
                headers: {
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                },
                body: JSON.stringify(batch)
            });
            
            if (response.ok) {
                inserted += batch.length;
                console.log(`✅ Inserted ${inserted}/${agents.length} agents`);
            } else {
                const errorText = await response.text();
                errors.push({ batch: i, error: errorText });
                console.error(`❌ Error at batch ${i}:`, errorText.substring(0, 200));
            }
        } catch (err) {
            errors.push({ batch: i, error: err.message });
            console.error(`❌ Network error at batch ${i}:`, err.message);
        }
    }
    
    console.log('\n📊 Import Summary:');
    console.log(`   ✅ Inserted: ${inserted} agents`);
    console.log(`   ❌ Errors: ${errors.length} batches`);
    
    if (errors.length > 0) {
        console.log('\n❌ Error details:');
        errors.forEach(e => console.log(`   Batch ${e.batch}: ${e.error.substring(0, 100)}`));
    }
    
    return { inserted, errors };
}

// Run
importAgents()
    .then(result => {
        console.log('\n✨ Done!');
        process.exit(result.errors.length > 0 ? 1 : 0);
    })
    .catch(err => {
        console.error('\n💥 Fatal error:', err);
        process.exit(1);
    });
