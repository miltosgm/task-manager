# AgentScore - Product Documentation

> **Version:** 1.0 | **Last Updated:** January 2026

---

## 1. Project Overview

### What the product does

AgentScore is a **review platform for real estate agencies**. Think of it as "Trustpilot for property agents" — a place where people can:
- Find trusted real estate agents in their area
- Read verified reviews from real customers
- Compare agencies by ratings, reviews, and services

### The problem it solves

**For property buyers/renters:**
- "How do I know if this agent is trustworthy?"
- "Are there any reviews about this agency?"
- "Who are the best agents in Limassol?"

Currently, reviews are scattered across Google, Facebook, and random forums. AgentScore aggregates them into one searchable directory.

**For agencies:**
- No central platform to showcase their reputation
- Positive reviews get lost across multiple sites
- Hard to stand out from competitors

### Who it's for

| User Type | What They Want |
|-----------|----------------|
| **Property Seekers** | Find trusted agents, read reviews before committing |
| **Expats** | English-language reviews, expat-friendly agencies |
| **Investors** | Identify reliable agencies for property investment |
| **Agencies** | Showcase reputation, respond to reviews, get discovered |

---

## 2. Core Concept (High-Level)

### The "Trust Layer" for Real Estate

Think of AgentScore as the **trust layer** between property seekers and agencies.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Property Seeker                                   │
│        │                                            │
│        ▼                                            │
│   ┌─────────────────┐                               │
│   │   AgentScore    │  ◄── Trust Layer              │
│   │   - Reviews     │                               │
│   │   - Ratings     │                               │
│   │   - Verified    │                               │
│   └────────┬────────┘                               │
│            │                                        │
│            ▼                                        │
│   Real Estate Agency                                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Why it works:**
- Aggregates reviews from multiple sources (Google, Facebook, etc.)
- Adds user-submitted reviews with verification
- Creates a single "trust score" for each agency

---

## 3. User Journey

### Journey 1: Property Seeker Finding an Agent

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Land on │───►│  Search  │───►│  Browse  │───►│  Read    │
│  Homepage│    │  by City │    │  Results │    │  Reviews │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                     │
                                                     ▼
                                               ┌──────────┐
                                               │  Contact │
                                               │  Agency  │
                                               └──────────┘
```

**Step-by-step:**

1. **Land on Homepage**
   - See search bar, stats (50+ agencies, 800+ reviews)
   - Quick-filter buttons for cities

2. **Search by City or Name**
   - Type location or agency name
   - Or click city tag (Limassol, Nicosia, etc.)

3. **Browse Results**
   - See ranked list of agencies
   - Filter by rating, services, specialization
   - Sort by most reviews or highest rated

4. **Read Reviews**
   - Click agency to see full profile
   - Read all reviews with dates and sources
   - See rating breakdown (5-star, 4-star, etc.)

5. **Contact Agency**
   - Click "Contact Agency" button
   - See phone, email, address, website

---

### Journey 2: User Submitting a Review

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Click   │───►│  Select  │───►│  Write   │───►│  Verify  │
│  "Write  │    │  Agency  │    │  Review  │    │  Email   │
│  Review" │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                     │
                                                     ▼
                                               ┌──────────┐
                                               │  Review  │
                                               │  Published│
                                               └──────────┘
```

**Step-by-step:**

1. **Click "Write Review"**
   - From homepage or agency profile

2. **Select Agency**
   - Search and select the agency you worked with

3. **Write Review**
   - Give star rating (1-5)
   - Write review title and text
   - Select transaction type (bought, sold, rented, etc.)
   - Optionally name the specific agent

4. **Verify Email**
   - Receive confirmation email
   - Click link to verify

5. **Review Published**
   - Review goes live after moderation
   - Agency can respond to review

---

## 4. System Architecture (Simplified)

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Homepage   │  │  City Page  │  │  Profile    │          │
│  │             │  │             │  │  Page       │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │  Write      │  │  Search     │                           │
│  │  Review     │  │  Results    │                           │
│  └─────────────┘  └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                      API                             │    │
│  │  • GET /agencies         • GET /agencies/:id         │    │
│  │  • GET /cities/:city     • POST /reviews             │    │
│  │  • GET /search           • GET /reviews/:agencyId    │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    DATABASE                          │    │
│  │  • Agencies (50+)                                    │    │
│  │  • Reviews (800+)                                    │    │
│  │  • Users                                             │    │
│  │  • Cities                                            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Components Explained

| Component | What It Does |
|-----------|--------------|
| **Frontend** | The website users see and interact with |
| **API** | Handles requests (get agencies, submit reviews, etc.) |
| **Database** | Stores all agencies, reviews, and user data |

**Tech Stack (Recommended):**
- Frontend: Next.js (React)
- Backend: Next.js API routes
- Database: PostgreSQL or JSON files (MVP)
- Hosting: Vercel (free tier)

---

## 5. Data Model

### Agency

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| name | string | Agency name |
| location | string | Primary city |
| rating | number | Average rating (1-5) |
| reviewCount | number | Total reviews |
| services | array | Sales, Rentals, Commercial, etc. |
| tags | array | Expat Friendly, Luxury, etc. |
| contact | object | Phone, email, website, address |
| sources | object | Google, Facebook, etc. ratings |

### Review

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| agencyId | string | Agency this review belongs to |
| reviewer | string | Reviewer name |
| rating | number | Star rating (1-5) |
| date | string | When review was written |
| text | string | Review content |
| source | string | Google, Facebook, or User |
| transactionType | string | Bought, Sold, Rented, etc. |
| agentName | string | Specific agent (optional) |
| verified | boolean | Email verified |

---

## 6. Key Features

### 6.1 Search & Discovery

```
┌────────────────────────────────────────┐
│  🔍 Search by agency name or location  │
└────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  📍 Filter by city                     │
│  ⭐ Filter by minimum rating           │
│  🏠 Filter by services                 │
│  🏷️ Filter by specialization           │
└────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  📊 Sort by most reviews               │
│  📊 Sort by highest rated              │
│  📊 Sort alphabetically                │
└────────────────────────────────────────┘
```

### 6.2 Agency Profiles

What users see on an agency profile:

- **Header:** Logo, name, location, rating, review count
- **Tags:** Services and specializations
- **Actions:** Contact Agency, Write Review
- **Reviews:** Full list with filters
- **Sidebar:** Contact info, rating breakdown

### 6.3 Review System

**Aggregated Reviews:**
- Imported from Google, Facebook, etc.
- Marked with source

**User-Submitted Reviews:**
- Email verification required
- Moderated before publishing
- Agency can respond

### 6.4 Agency Claims (Future)

Agencies can:
- Claim their profile
- Add logo and details
- Respond to reviews
- Get verified badge

---

## 7. Page Structure

### Homepage

```
┌─────────────────────────────────────────────────────────┐
│                         HERO                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  🏠 Find Trusted Real Estate Agents               │  │
│  │  [_______Search by agency or location_______] 🔍  │  │
│  │  📍Limassol  📍Nicosia  📍Paphos  📍Larnaca       │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                      STATS BAR                          │
│     50+ Agencies    │    800+ Reviews    │    4.7 Avg   │
├─────────────────────────────────────────────────────────┤
│                    AGENCY LIST                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ 1 │ [K] │ Kalogirou Real Estate │ ⭐4.8 (389) │    │
│  ├────────────────────────────────────────────────┤    │
│  │ 2 │ [M] │ M.Residence           │ ⭐4.9 (133) │    │
│  ├────────────────────────────────────────────────┤    │
│  │ 3 │ [G] │ G&P Lazarou           │ ⭐4.8 (124) │    │
│  └────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                       CTA                               │
│  "Are you an agency? Claim your profile →"              │
└─────────────────────────────────────────────────────────┘
```

### City Page (e.g., /limassol)

```
┌─────────────────────────────────────────────────────────┐
│                      CITY HERO                          │
│  📍 Real Estate Agents in Limassol                      │
│     18 Agencies  │  320+ Reviews  │  4.6 Avg            │
├─────────────────────────────────────────────────────────┤
│  FILTERS           │           RESULTS                  │
│  ┌───────────┐     │  ┌─────────────────────────────┐  │
│  │ Rating    │     │  │ 1. Doorway Real Estate      │  │
│  │ [3+][4+]  │     │  │    ⭐5.0 (105 reviews)      │  │
│  ├───────────┤     │  ├─────────────────────────────┤  │
│  │ Services  │     │  │ 2. 4BUY&SELL                │  │
│  │ ☑ Sales   │     │  │    ⭐5.0 (64 reviews)       │  │
│  │ ☑ Rentals │     │  ├─────────────────────────────┤  │
│  │ ☐ Commerc │     │  │ 3. CENTURY 21               │  │
│  └───────────┘     │  │    ⭐4.6 (61 reviews)       │  │
│                    │  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Agency Profile Page

```
┌─────────────────────────────────────────────────────────┐
│  Home → Larnaca → Kalogirou Real Estate                 │
├─────────────────────────────────────────────────────────┤
│  ┌────┐                                                 │
│  │ K  │  Kalogirou Real Estate                          │
│  └────┘  📍 Larnaca • Est. 2008 • kalogirourealestate.com│
│          ┌─────┐ ⭐⭐⭐⭐⭐                               │
│          │ 4.8 │ Based on 389 reviews                   │
│          └─────┘                                        │
│          🏠Sales  🔑Rentals  🌍Expat Friendly           │
│                                         [Contact] [Review]│
├─────────────────────────────────────────────────────────┤
│  REVIEWS (389)              │  CONTACT INFO             │
│  ┌─────────────────────┐   │  📍 Ermou 196, Larnaca    │
│  │ ⬤ Yuri M.  ⭐⭐⭐⭐⭐  │   │  📞 +357 24 003723       │
│  │ 2 months ago         │   │  🌐 kalogirourealestate   │
│  │ "Very professional,  │   │                           │
│  │ young, energetic..." │   │  RATING BREAKDOWN         │
│  └─────────────────────┘   │  5⭐ ████████████░ 360    │
│  ┌─────────────────────┐   │  4⭐ █░░░░░░░░░░░░ 4      │
│  │ ⬤ Aziz A.  ⭐⭐⭐⭐⭐  │   │  3⭐ ░░░░░░░░░░░░░ 2      │
│  │ 1 month ago          │   │  2⭐ ░░░░░░░░░░░░░ 3      │
│  │ "I had the pleasure  │   │  1⭐ █░░░░░░░░░░░░ 20     │
│  │ of working with..."  │   │                           │
│  └─────────────────────┘   │                           │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Example Use Case

### Scenario: Expat Moving to Limassol

**User:** Sarah, a British expat relocating to Limassol for work.

**Goal:** Find a trustworthy agency to help rent an apartment.

**Journey:**

1. **Google Search:** "best real estate agents limassol"
   → Finds AgentScore

2. **Homepage:** Clicks "📍 Limassol" quick filter

3. **City Page:** 
   - Sees 18 agencies listed
   - Filters by "Expat Friendly" tag
   - Sorts by "Highest Rated"

4. **Results:** 
   - Doorway Real Estate appears #1 (5.0 rating, 105 reviews)
   - Notes "Expat Friendly" tag

5. **Profile Page:**
   - Reads reviews from other expats
   - Sees reviewer "Rosa Bachmann" (1 week ago): *"Vasilis has been professional, friendly, and always helpful..."*
   - Sees contact info

6. **Action:** 
   - Clicks "Contact Agency"
   - Calls +357 number
   - Books viewing appointment

**Outcome:** Sarah found a trusted agent based on real reviews from people like her.

---

## 9. Metrics & Success

### Key Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| **Monthly Visitors** | Unique visitors per month | 1,000+ |
| **Search-to-Profile** | % who click an agency | >30% |
| **Profile-to-Contact** | % who contact agency | >10% |
| **Reviews Submitted** | New user reviews per month | 20+ |
| **Agency Claims** | Agencies claiming profiles | 10+ |

### Success Indicators

✅ Ranking in Google for "real estate agents [city] cyprus"
✅ Agencies asking to claim their profiles
✅ Users submitting organic reviews
✅ Repeat visitors

---

## 10. Roadmap

### Phase 1: MVP Launch ✅
- [x] Data collection (50 agencies)
- [x] Homepage design
- [x] City pages
- [x] Agency profiles
- [x] Basic search

### Phase 2: Core Features
- [ ] User review submission
- [ ] Email verification
- [ ] Agency claim flow
- [ ] Mobile optimization

### Phase 3: Growth
- [ ] SEO optimization
- [ ] More cities/countries
- [ ] Agency dashboard
- [ ] Review responses
- [ ] Verified badges

### Phase 4: Monetization
- [ ] Featured listings
- [ ] Premium agency profiles
- [ ] Lead generation
- [ ] Advertising

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **Agency** | A real estate company/business |
| **Agent** | Individual person working at an agency |
| **Review** | User feedback about an agency (rating + text) |
| **Rating** | Score from 1-5 stars |
| **Trust Score** | Aggregated rating from all sources |
| **Verified Review** | Review confirmed via email verification |
| **Claimed Profile** | Agency has taken ownership of their listing |
| **Sources** | Where reviews come from (Google, Facebook, User) |

---

## 12. FAQ

**Q: Where do the reviews come from?**
A: We aggregate reviews from Google, Facebook, and other platforms. Users can also submit their own reviews.

**Q: Are the reviews verified?**
A: Imported reviews are from trusted sources. User-submitted reviews require email verification.

**Q: Can agencies remove bad reviews?**
A: No. Agencies can respond to reviews but cannot remove legitimate feedback.

**Q: How do agencies get listed?**
A: We proactively list agencies from public data. Agencies can then claim and enhance their profile.

**Q: Is it free to use?**
A: Yes, for property seekers. Agency premium features may be paid in the future.

---

## 13. Contact & Resources

**Project Repository:** `/projects/agent-scraper/`

**Key Files:**
- `mockups/` - HTML mockups of all pages
- `all-agents-all-reviews.json` - Full agency data
- `sample-reviews.json` - Sample review data
- `docs/PRODUCT_DOCUMENTATION.md` - This file

**Google Sheet:** [Cyprus Agents with Reviews](https://docs.google.com/spreadsheets/d/19WAYy8QL1etPvPTmsnsY-wwFqe_C5_hEA_wmhazR0W8/edit)

---

*Documentation created: January 2026*
*Last updated: January 29, 2026*
