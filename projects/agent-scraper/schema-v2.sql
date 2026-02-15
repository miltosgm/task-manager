-- =====================================================
-- AgentScore v2 Schema - Unified Platform
-- Supports: Agents, Developers, Agencies
-- =====================================================

-- Entity Types Enum
CREATE TYPE entity_type AS ENUM ('agent', 'developer', 'agency');

-- Rating Categories Enum (for developers)
CREATE TYPE rating_category AS ENUM (
  'build_quality',
  'communication', 
  'value_for_money',
  'timeliness',
  'after_sales',
  'overall'
);

-- =====================================================
-- AGENTS TABLE (existing, enhanced)
-- =====================================================
CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE,
  
  -- Contact Info
  email VARCHAR(255),
  phone VARCHAR(50),
  website VARCHAR(500),
  
  -- Location
  location VARCHAR(100), -- City: Limassol, Paphos, etc.
  address TEXT,
  
  -- External Links
  bazaraki_url VARCHAR(500),
  google_maps_url VARCHAR(500),
  linkedin_url VARCHAR(500),
  facebook_url VARCHAR(500),
  
  -- Stats
  listing_count INTEGER DEFAULT 0,
  years_experience INTEGER,
  
  -- Ratings (aggregated)
  google_rating DECIMAL(2,1),
  google_reviews_count INTEGER DEFAULT 0,
  platform_rating DECIMAL(2,1),
  platform_reviews_count INTEGER DEFAULT 0,
  
  -- Profile
  photo_url VARCHAR(500),
  bio TEXT,
  specializations TEXT[], -- e.g., ['luxury', 'commercial', 'rentals']
  languages TEXT[], -- e.g., ['English', 'Greek', 'Russian']
  
  -- Agency relationship
  agency_id UUID REFERENCES agencies(id),
  
  -- Meta
  is_verified BOOLEAN DEFAULT FALSE,
  is_claimed BOOLEAN DEFAULT FALSE,
  claimed_by UUID, -- user who claimed
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- DEVELOPERS TABLE (new)
-- =====================================================
CREATE TABLE IF NOT EXISTS developers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE,
  
  -- Company Info
  legal_name VARCHAR(255),
  registration_number VARCHAR(100),
  established_year INTEGER,
  
  -- Contact Info
  email VARCHAR(255),
  phone VARCHAR(50),
  website VARCHAR(500),
  
  -- Location
  headquarters VARCHAR(100), -- City
  address TEXT,
  regions_active TEXT[], -- e.g., ['Limassol', 'Paphos', 'Larnaca']
  
  -- External Links
  google_maps_url VARCHAR(500),
  linkedin_url VARCHAR(500),
  facebook_url VARCHAR(500),
  
  -- Stats
  total_projects INTEGER DEFAULT 0,
  completed_projects INTEGER DEFAULT 0,
  ongoing_projects INTEGER DEFAULT 0,
  total_units_delivered INTEGER DEFAULT 0,
  
  -- Ratings (aggregated)
  google_rating DECIMAL(2,1),
  google_reviews_count INTEGER DEFAULT 0,
  platform_rating DECIMAL(2,1),
  platform_reviews_count INTEGER DEFAULT 0,
  
  -- Category Ratings (averaged from reviews)
  rating_build_quality DECIMAL(2,1),
  rating_communication DECIMAL(2,1),
  rating_value DECIMAL(2,1),
  rating_timeliness DECIMAL(2,1),
  rating_after_sales DECIMAL(2,1),
  
  -- Profile
  logo_url VARCHAR(500),
  cover_image_url VARCHAR(500),
  description TEXT,
  certifications TEXT[], -- e.g., ['ISO 9001', 'Green Building']
  
  -- Meta
  is_verified BOOLEAN DEFAULT FALSE,
  is_claimed BOOLEAN DEFAULT FALSE,
  claimed_by UUID,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- PROJECTS TABLE (developer projects/buildings)
-- =====================================================
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  developer_id UUID REFERENCES developers(id) ON DELETE CASCADE,
  
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255),
  
  -- Location
  location VARCHAR(100), -- City
  address TEXT,
  coordinates POINT, -- lat/lng
  
  -- Project Details
  project_type VARCHAR(50), -- 'residential', 'commercial', 'mixed', 'resort'
  status VARCHAR(50), -- 'completed', 'under_construction', 'planned'
  
  -- Timeline
  start_date DATE,
  completion_date DATE,
  expected_completion DATE,
  
  -- Units
  total_units INTEGER,
  units_sold INTEGER,
  units_available INTEGER,
  
  -- Pricing
  price_from DECIMAL(12,2),
  price_to DECIMAL(12,2),
  currency VARCHAR(3) DEFAULT 'EUR',
  
  -- Media
  thumbnail_url VARCHAR(500),
  images TEXT[], -- array of image URLs
  brochure_url VARCHAR(500),
  
  -- Description
  description TEXT,
  amenities TEXT[], -- e.g., ['pool', 'gym', 'parking', 'garden']
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- AGENCIES TABLE (real estate agencies)
-- =====================================================
CREATE TABLE IF NOT EXISTS agencies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE,
  
  -- Contact
  email VARCHAR(255),
  phone VARCHAR(50),
  website VARCHAR(500),
  
  -- Location
  headquarters VARCHAR(100),
  address TEXT,
  branches TEXT[], -- e.g., ['Limassol', 'Paphos']
  
  -- Stats
  agent_count INTEGER DEFAULT 0,
  listing_count INTEGER DEFAULT 0,
  
  -- Ratings
  google_rating DECIMAL(2,1),
  google_reviews_count INTEGER DEFAULT 0,
  platform_rating DECIMAL(2,1),
  platform_reviews_count INTEGER DEFAULT 0,
  
  -- Profile
  logo_url VARCHAR(500),
  description TEXT,
  
  -- Meta
  is_verified BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- REVIEWS TABLE (unified for all entity types)
-- =====================================================
CREATE TABLE IF NOT EXISTS reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- What is being reviewed
  entity_type entity_type NOT NULL,
  agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  developer_id UUID REFERENCES developers(id) ON DELETE CASCADE,
  agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id), -- optional: review specific project
  
  -- Reviewer
  reviewer_name VARCHAR(255),
  reviewer_email VARCHAR(255),
  reviewer_verified BOOLEAN DEFAULT FALSE,
  
  -- Ratings
  rating_overall INTEGER CHECK (rating_overall >= 1 AND rating_overall <= 5),
  
  -- Developer-specific ratings
  rating_build_quality INTEGER CHECK (rating_build_quality >= 1 AND rating_build_quality <= 5),
  rating_communication INTEGER CHECK (rating_communication >= 1 AND rating_communication <= 5),
  rating_value INTEGER CHECK (rating_value >= 1 AND rating_value <= 5),
  rating_timeliness INTEGER CHECK (rating_timeliness >= 1 AND rating_timeliness <= 5),
  rating_after_sales INTEGER CHECK (rating_after_sales >= 1 AND rating_after_sales <= 5),
  
  -- Content
  title VARCHAR(255),
  content TEXT,
  
  -- Transaction details (optional)
  transaction_type VARCHAR(50), -- 'purchase', 'sale', 'rental'
  transaction_year INTEGER,
  property_type VARCHAR(50), -- 'apartment', 'villa', 'house', 'commercial'
  
  -- Source
  source VARCHAR(50) DEFAULT 'platform', -- 'platform', 'google', 'facebook', 'imported'
  source_url VARCHAR(500),
  source_review_id VARCHAR(255),
  
  -- Moderation
  status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
  moderated_at TIMESTAMPTZ,
  moderated_by UUID,
  
  -- Response from entity
  response TEXT,
  response_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Ensure review is linked to exactly one entity
  CONSTRAINT review_entity_check CHECK (
    (agent_id IS NOT NULL)::int + 
    (developer_id IS NOT NULL)::int + 
    (agency_id IS NOT NULL)::int = 1
  )
);

-- =====================================================
-- INDEXES
-- =====================================================

-- Agents
CREATE INDEX idx_agents_location ON agents(location);
CREATE INDEX idx_agents_slug ON agents(slug);
CREATE INDEX idx_agents_agency ON agents(agency_id);
CREATE INDEX idx_agents_rating ON agents(platform_rating DESC NULLS LAST);

-- Developers
CREATE INDEX idx_developers_headquarters ON developers(headquarters);
CREATE INDEX idx_developers_slug ON developers(slug);
CREATE INDEX idx_developers_rating ON developers(platform_rating DESC NULLS LAST);

-- Projects
CREATE INDEX idx_projects_developer ON projects(developer_id);
CREATE INDEX idx_projects_location ON projects(location);
CREATE INDEX idx_projects_status ON projects(status);

-- Reviews
CREATE INDEX idx_reviews_agent ON reviews(agent_id) WHERE agent_id IS NOT NULL;
CREATE INDEX idx_reviews_developer ON reviews(developer_id) WHERE developer_id IS NOT NULL;
CREATE INDEX idx_reviews_agency ON reviews(agency_id) WHERE agency_id IS NOT NULL;
CREATE INDEX idx_reviews_status ON reviews(status);
CREATE INDEX idx_reviews_created ON reviews(created_at DESC);

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Function to update agent rating when reviews change
CREATE OR REPLACE FUNCTION update_agent_rating()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE agents SET
    platform_rating = (
      SELECT ROUND(AVG(rating_overall)::numeric, 1)
      FROM reviews
      WHERE agent_id = COALESCE(NEW.agent_id, OLD.agent_id)
      AND status = 'approved'
    ),
    platform_reviews_count = (
      SELECT COUNT(*)
      FROM reviews
      WHERE agent_id = COALESCE(NEW.agent_id, OLD.agent_id)
      AND status = 'approved'
    ),
    updated_at = NOW()
  WHERE id = COALESCE(NEW.agent_id, OLD.agent_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to update developer ratings when reviews change
CREATE OR REPLACE FUNCTION update_developer_rating()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE developers SET
    platform_rating = (
      SELECT ROUND(AVG(rating_overall)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    platform_reviews_count = (
      SELECT COUNT(*)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    rating_build_quality = (
      SELECT ROUND(AVG(rating_build_quality)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    rating_communication = (
      SELECT ROUND(AVG(rating_communication)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    rating_value = (
      SELECT ROUND(AVG(rating_value)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    rating_timeliness = (
      SELECT ROUND(AVG(rating_timeliness)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    rating_after_sales = (
      SELECT ROUND(AVG(rating_after_sales)::numeric, 1)
      FROM reviews
      WHERE developer_id = COALESCE(NEW.developer_id, OLD.developer_id)
      AND status = 'approved'
    ),
    updated_at = NOW()
  WHERE id = COALESCE(NEW.developer_id, OLD.developer_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER trigger_update_agent_rating
  AFTER INSERT OR UPDATE OR DELETE ON reviews
  FOR EACH ROW
  WHEN (COALESCE(NEW.agent_id, OLD.agent_id) IS NOT NULL)
  EXECUTE FUNCTION update_agent_rating();

CREATE TRIGGER trigger_update_developer_rating
  AFTER INSERT OR UPDATE OR DELETE ON reviews
  FOR EACH ROW
  WHEN (COALESCE(NEW.developer_id, OLD.developer_id) IS NOT NULL)
  EXECUTE FUNCTION update_developer_rating();

-- =====================================================
-- ROW LEVEL SECURITY
-- =====================================================

ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE developers ENABLE ROW LEVEL SECURITY;
ALTER TABLE agencies ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Public read access
CREATE POLICY "Public read agents" ON agents FOR SELECT USING (true);
CREATE POLICY "Public read developers" ON developers FOR SELECT USING (true);
CREATE POLICY "Public read agencies" ON agencies FOR SELECT USING (true);
CREATE POLICY "Public read projects" ON projects FOR SELECT USING (true);
CREATE POLICY "Public read approved reviews" ON reviews FOR SELECT USING (status = 'approved');
