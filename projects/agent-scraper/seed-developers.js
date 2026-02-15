const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');

const supabaseUrl = 'https://sqjvwnuqbvnfvftvgzdz.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNxanZ3bnVxYnZuZnZmdHZnemR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgwNzYwOTYsImV4cCI6MjA1MzY1MjA5Nn0.LxH-UyL1WE8Y8BOthTQkaA_IOfpdMZ7';

const supabase = createClient(supabaseUrl, supabaseKey);

async function seedDevelopers() {
  // Read developers data
  const data = JSON.parse(fs.readFileSync('cyprus-developers.json', 'utf8'));
  
  console.log(`Importing ${data.developers.length} developers...`);
  
  for (const dev of data.developers) {
    const developer = {
      name: dev.name,
      slug: dev.slug,
      established_year: dev.established_year,
      headquarters: dev.headquarters,
      regions_active: dev.regions_active,
      website: dev.website,
      google_rating: dev.google_rating,
      google_reviews_count: dev.google_reviews_count,
      total_projects: dev.total_projects,
      description: dev.description,
      linkedin_url: dev.linkedin,
      // Store notable projects as JSON in description for now
    };
    
    const { data: result, error } = await supabase
      .from('developers')
      .upsert(developer, { onConflict: 'slug' })
      .select();
    
    if (error) {
      console.error(`Error inserting ${dev.name}:`, error.message);
    } else {
      console.log(`✓ Inserted: ${dev.name}`);
    }
  }
  
  console.log('Done!');
}

seedDevelopers().catch(console.error);
