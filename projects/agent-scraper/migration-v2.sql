-- Migration script to upgrade existing AgentScore DB to v2
-- Run this after the initial schema-v2.sql

-- Add missing columns to agents table
ALTER TABLE agents ADD COLUMN IF NOT EXISTS slug VARCHAR(255) UNIQUE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS email VARCHAR(255);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS phone VARCHAR(50);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS google_maps_url VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS linkedin_url VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS facebook_url VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS years_experience INTEGER;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS platform_rating DECIMAL(2,1);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS platform_reviews_count INTEGER DEFAULT 0;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS photo_url VARCHAR(500);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS bio TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS specializations TEXT[];
ALTER TABLE agents ADD COLUMN IF NOT EXISTS languages TEXT[];
ALTER TABLE agents ADD COLUMN IF NOT EXISTS agency_id UUID;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_claimed BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS claimed_by UUID;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Add missing columns to reviews table
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS entity_type VARCHAR(20) DEFAULT 'agent';
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS developer_id UUID;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS agency_id UUID;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS project_id UUID;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS reviewer_name VARCHAR(255);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS reviewer_email VARCHAR(255);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS reviewer_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_overall INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_build_quality INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_communication INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_value INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_timeliness INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS rating_after_sales INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS title VARCHAR(255);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS transaction_type VARCHAR(50);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS transaction_year INTEGER;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS property_type VARCHAR(50);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'platform';
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS source_url VARCHAR(500);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS source_review_id VARCHAR(255);
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'approved';
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS moderated_at TIMESTAMPTZ;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS moderated_by UUID;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS response TEXT;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS response_at TIMESTAMPTZ;

-- Create indexes if not exists (using DO block to check)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_agents_slug') THEN
        CREATE INDEX idx_agents_slug ON agents(slug);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_agents_agency') THEN
        CREATE INDEX idx_agents_agency ON agents(agency_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_agents_platform_rating') THEN
        CREATE INDEX idx_agents_platform_rating ON agents(platform_rating DESC NULLS LAST);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reviews_developer') THEN
        CREATE INDEX idx_reviews_developer ON reviews(developer_id) WHERE developer_id IS NOT NULL;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reviews_agency') THEN
        CREATE INDEX idx_reviews_agency ON reviews(agency_id) WHERE agency_id IS NOT NULL;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reviews_status') THEN
        CREATE INDEX idx_reviews_status ON reviews(status);
    END IF;
END $$;

-- Add foreign key for agency_id in agents (if agencies table exists)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'agencies') THEN
        ALTER TABLE agents 
        ADD CONSTRAINT fk_agents_agency 
        FOREIGN KEY (agency_id) REFERENCES agencies(id)
        ON DELETE SET NULL;
    END IF;
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- Add foreign keys for reviews
DO $$
BEGIN
    ALTER TABLE reviews 
    ADD CONSTRAINT fk_reviews_developer 
    FOREIGN KEY (developer_id) REFERENCES developers(id) ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE reviews 
    ADD CONSTRAINT fk_reviews_agency 
    FOREIGN KEY (agency_id) REFERENCES agencies(id) ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE reviews 
    ADD CONSTRAINT fk_reviews_project 
    FOREIGN KEY (project_id) REFERENCES projects(id);
EXCEPTION WHEN duplicate_object THEN
    NULL;
END $$;

-- Update RLS policies for reviews
DROP POLICY IF EXISTS "Public read approved reviews" ON reviews;
CREATE POLICY "Public read reviews" ON reviews FOR SELECT USING (true);
