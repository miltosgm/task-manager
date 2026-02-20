# MEMORY.md - Long-Term Memory

*This is your curated memory. Read at the start of main sessions.*

---

## 🚨 NEVER FORGET

### Critical Rules
- **FULL AUTONOMY**: Never ask for permission, confirmation, or user to perform manual steps. Always attempt to complete tasks yourself using available tools.
- **Never delegate back to user**: If you encounter obstacles, try to solve independently. Only report results + blockers.
- **Credentials/Access Missing?** State what's blocking you and move on. Do NOT list manual steps for user to follow.
- **Report style**: Results only. Brief. If blocked by external constraint, state that. No questions, no asking what to do.

### Non-negotiables
- Never ask "should I?" — just do it
- Never ask "can you?" — attempt it yourself first
- Attempt to complete tasks yourself using available tools
- Try to solve obstacles independently before reporting

---

## Client Context Library (AISquad — SEO / AEO / Paid Ads)

| Client | Website | Vertical | Notes |
|---|---|---|---|
| **Karma Developers** | karmadevelopers.com | Real Estate (Cyprus) | Part of Karma Group, 40yrs, 5,000+ homes. Villas/apartments in Ayia Napa & Protaras. Greek + international buyers. |
| **CDMA** | cdma.com.cy | B2B Managed IT (Cyprus) | Cloud, infrastructure, bespoke app dev. Expanding locally + internationally. |
| **Hola Prime** | holaprime.com | Fintech / Prop Trading / Forex | Regulated prop firm + forex broker. Fast payouts (1hr), brand ambassador Karl-Anthony Towns. |
| **ThePayStubs** | thepaystubs.com | SaaS / HR Tools (US) | Online paystub generator. B2C SaaS, US-focused, high-volume keyword opportunity. |

---

## User Profile

### Who They Are
- **Timezone:** Europe/Athens | **Telegram:** 350271065
- **Business:** AISquad (SEO, AEO, Paid Ads for clients above)
- **Style:** Fast-paced, high autonomy, visual-first, mobile-first mindset

### What They're Great At
- Building autonomous agents (OpenClaw infrastructure)
- Rapid iteration and decision-making
- Clear product vision, flexible on implementation

### Operating Style
- **Pace:** Fast. Solve it quickly, don't deliberate.
- **Feedback:** Visual and direct — shows preferences through complaints
- **Decisions:** Present 3 options with actual visual renders, let them choose
- **Risk tolerance:** High — provides tokens, iterates quickly

---

## Active Projects

### Mission Control Activity Dashboard
- **Goal:** Real-time activity tracking dashboard for OpenClaw agent with live webhook logging
- **Status:** 🟢 **LIVE** — deployed, mobile-responsive
- **GitHub:** https://github.com/miltosgm/mission-control
- **Live URL:** https://mission-control-eight-nu.vercel.app
- **Vercel Project ID:** `prj_q6teL3CFacuRwTzcz3QviZohpAq2` | Org: `exide1` (exide1@hotmail.com)

**What it does (user's words):** "Automatic notebook that records everything the agent does" — tracks file creation, tasks, searches, proposals. Audit trail of agent work.

**Tech Stack:**
- Frontend: Next.js + Tailwind CSS (Vercel)
- API: POST/GET `/api/log-activity`
- Webhook Library: `/Users/milton/clawd/lib/openclaw-webhook.ts`
- Env var: `MISSION_CONTROL_URL` → live Vercel URL
- ⚠️ Data stored in-memory only — needs DB for production persistence

**Webhook Functions:**
- `logFileCreated(path, sizeBytes)` · `logFileEdited(path, description)`
- `logSearch(query, resultCount, sources[])` · `logTaskCompleted(taskName, durationMs, status)`
- `logProposal(name, pageCount, description)` · `logCustom(description, result)`

**Pending:** User to pick final design (C / C1-orange / C2-cyan / C3-violet) → build production Next.js site for grow-fintech.io.

### grow-fintech.io Homepage
- **Goal:** Full marketing website for Miltos's fintech agency brand
- **Status:** 🟡 Design selection stage — 4 HTML prototypes live on GitHub Pages
- **GitHub Pages:** https://miltosgm.github.io/grow-fintech-designs/
- **GitHub Repo:** https://github.com/miltosgm/grow-fintech-designs
- **Next.js draft:** `/Users/milton/clawd/grow-fintech/site/` (14 sections, builds clean)
- **Copy doc:** https://docs.google.com/document/d/1Q1QzxnArotXYs5WmPEtKL5g0ueEzb7W7ha4H14QIREg
- **Designs:** C (green gradient), C1 (orange), C2 (cyan/authority), C3 (violet/future)
- **Key copy lines:** H1 = "We Grow Fintechs. Profitably." | CTA = "Even if the answer isn't 'spend more.'"
- **GEO** (Generative Engine Optimization) = major differentiator — highlight in every design
- **Services:** Paid Acquisition · GEO · Growth Strategy & GTM · B2B Demand Gen · Fractional CMO

---

## Preferences & Rules

### Communication
- Direct, visual-first (rendered mockups, not text descriptions)
- Prefers options to choose from, never single imposed solution
- Escalation triggers: aesthetic issues, lack of visual clarity
- **No dashes** in written copy or reviews (no em dashes, no hyphens as punctuation)

### Lessons Learned
- ✅ Provide actual rendered HTML files — "These are not visuals!!!" = needs real renders
- ✅ Offer 3 design options, let user pick
- ✅ Mobile-first always — user primary device is mobile
- ✅ Full autonomy — just execute, only report results & blockers
- ✅ Browser relay more reliable than automation for auth flows
- ❌ Never describe designs in text — always render them
- ❌ Never ask permission or delegate steps back to user
- ❌ Never desktop-first design

---

## Slack DM — Confirmed Working Method

- **✅ Working:** `message(action=send, channel=slack, target=D0ACZSASYGY)` — use the DM channel ID directly
- **❌ Broken:** `target=miltosgm` — returns `missing_scope`
- Confirmed working: Feb 20, 2026 at 8:59 AM Athens

## Slack Key IDs

| Who/What | ID |
|---|---|
| Miltos (owner) | `U06MWAMT456` |
| Muhammad Talha / Stelios (team) | `U07MXR84XT3` |
| Team member 2 | `U06RKR47ELW` |
| General / team channel | `C09CKQ6D5K6` |
| Group DM (Miltos + Muhammad Talha + Clawdbot) | `C0AGS8C3NMN` |
| Miltos DM channel | `D0ACZSASYGY` |

---

## WhatsApp / Twilio Status

- **Account SID:** ACaf7fec5f636363682926edf1ecbf5017 | **Phone:** +19894954114
- **Status:** ⚠️ NOT ACTIVE — WhatsApp sandbox not provisioned on Twilio side
- **Blocker:** Requires manual Twilio console activation (external action)
- **OpenClaw config:** ✅ Ready once Twilio WhatsApp is provisioned

---

## Notes for Future-Me

- **Mission-Driven:** Deploys quickly, cares about things that actually work
- **Quality-Focused:** Notices and calls out UI/UX issues immediately (especially mobile)
- **Trust-Based:** Provides credentials once you prove you need them
- **Iterative:** Wants options → picks → implements. Not a plan-then-execute person.

---

**Review Frequency:** Weekly | **Last Updated:** 2026-02-19
