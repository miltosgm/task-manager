# MEMORY.md - Long-Term Memory

*This is your curated memory. Read at the start of main sessions.*

---

## 🚨 NEVER FORGET

### Critical Rules
- **FULL AUTONOMY**: Never ask for permission, confirmation, or user to perform manual steps. Always attempt to complete tasks yourself using available tools.
- **Never delegate back to user**: If you encounter obstacles, try to solve independently. Only report results + blockers.
- **Credentials/Access Missing?** State what's blocking you and move on. Do NOT list manual steps for user to follow.
- **Report style**: Results only. Brief. If blocked by external constraint, state that. No questions, no asking what to do.

### Boundaries
- Never ask "should I?" — just do it
- Never ask "can you?" — attempt it yourself first
- Never delegate internal work back to the user
- Never make the user's problem YOUR problem to report

### Non-negotiables
- Attempt to complete tasks yourself using available tools
- Try to solve obstacles independently before reporting
- This is non-negotiable. No exceptions. No hedging. Just action.

---

## User Expertise & Strengths

### What They're Great At
- Building autonomous agents (OpenClaw agent infrastructure)
- Rapid iteration and decision-making
- Clear vision for product goals (knows exactly what Mission Control should do)
- Pragmatic problem-solving (provided token when browser automation blocked deployment)

### Past Wins
- Deployed full-stack agent application with webhook integration
- Successfully iterated from desktop-first to mobile-responsive design in single session
- Built complete agent webhook library for activity logging

### Operating Style
- **Pace:** Fast. Wants problems solved quickly, not deliberated.
- **Autonomy:** High. Wants minimal back-and-forth. Prefers "just do it" approach.
- **Feedback:** Visual and direct. Shows preferences through what they complain about.
- **Vision:** Clear goals, flexible on implementation. Cares about end user experience.
- **Collaboration:** Cooperative when needed (provided token) but independent by default.

---

## Active Projects & Businesses

### Mission Control Activity Dashboard
- **Goal:** Real-time activity tracking dashboard for OpenClaw agent with live webhook logging
- **Status:** 🟢 **LIVE** — Dashboard deployed, mobile-responsive, awaiting design selection
- **GitHub:** https://github.com/miltosgm/mission-control
- **Live Dashboard URL:** https://mission-control-eight-nu.vercel.app ✅ LIVE
- **Key People:** miltos (solo project)

**Deployment Status (2026-02-15 17:51 GMT+2):**
- ✅ Dashboard LIVE and working: https://mission-control-eight-nu.vercel.app
- ✅ Mobile responsive design deployed (hamburger menu, adaptive layouts)
- ✅ Webhook API endpoints verified working (POST/GET)
- ✅ Agent environment config updated with live URL
- ✅ Vercel project properly linked to GitHub (miltosgm/mission-control)
- ✅ Webhook library installed in agent: `/Users/milton/clawd/lib/openclaw-webhook.ts`
- ✅ Test script ready: `/Users/milton/mission-control/test-webhook.sh`

**Current Phase: Design Selection**
- User needs to choose from 3 visual design options before final implementation
- **Option 1 - Simple & Minimal**: ✅ HTML prototype created - `option1.html` (white bg, text-focused, green/blue accents, mobile-optimized)
- **Option 2 - Colorful Cards**: 🔄 In progress - Dark background, gradient cards, vibrant emojis, modern look
- **Option 3 - Dashboard Pro**: 🔄 In progress - Sidebar layout, professional gray/blue, 4-column stats grid

**Next Steps:**
1. Complete Option 2 and Option 3 HTML visual prototypes (render in browser, not text)
2. Provide user with browser-viewable HTML files for visual comparison
3. Await user design selection from actual visual renders
4. Implement selected design into live Next.js dashboard
5. Test agent integration - send real activities from OpenClaw to dashboard
6. Verify webhook logging works end-to-end

**Key Technical URLs & IDs:**
- Vercel Project ID: `prj_q6teL3CFacuRwTzcz3QviZohpAq2`
- Vercel Organization: `exide1` (exide1@hotmail.com)
- API Endpoint: POST/GET `/api/log-activity`
- Webhook Functions Available: logFileCreated, logFileEdited, logSearch, logTaskCompleted, logProposal, logCustom

### Project 2: [Name]
- **Goal:**
- **Status:**
- **Key People:**
- **Recent Progress:**
- **Next Steps:**

---

## Preferences & Rules

### Communication
- **Preferred channels:** WhatsApp for quick feedback/decisions, direct action without asking permission
- **Feedback style:** Direct, visual-first (needs actual rendered designs, not text descriptions)
- **Decision framework:** Prefers to choose from multiple options rather than single imposed design
- **Quiet hours:** (not yet established)
- **Escalation triggers:** Aesthetic issues ("looks bad on mobile"), lack of visual clarity

### Work Style
- **Decision framework:** Present 3-5 options with actual visual mockups, let them choose
- **Risk tolerance:** High (provides tokens, iterates quickly, wants autonomous action)
- **Information format:** Visual mockups > text descriptions; rendered HTML/screenshots preferred
- **Feedback style:** Direct and specific ("These are not visuals!!!" = needs actual renders, not descriptions)
- **Autonomy:** Full autonomy required - never ask permission, attempt solutions independently, only report results/blockers

### Platform-Specific Notes
- **Telegram:** (what it's used for)
- **Email:** (response time expectations)
- **Slack:** (channel norms)

---

## Lessons Learned

### What Worked Well
- **Providing actual visual renders** (HTML files) instead of text mockups - user responds much better to seeing real designs
- **Offering 3 design options** and letting user choose rather than implementing single design
- **Full autonomy directive** - user appreciates independent problem-solving; only report results & blockers
- **Browser relay for auth flows** - using user's existing authenticated browser more reliable than automation
- **Mobile-first iteration** - user complained about desktop design, immediate pivot to mobile responsive paid off
- **Quick deployment cycles** - fixing issues and redeploying in minutes keeps momentum

### Mistakes to Avoid
- Text descriptions of design mockups ("These are not visuals!!!" feedback)
- Asking for permission or confirmation before attempting autonomous solutions
- Delegating manual steps back to user ("please do X")
- Imposing single design choice instead of offering options
- Desktop-first design when user works primarily on mobile

### Blind Spots to Watch
- User feedback is often visual/aesthetic, not technical - pay attention to "looks bad" complaints as design signals
- When browser automation times out (45+ min), recognize the blocker and move to user collaboration instead of persisting
- Visual design choices are subjective - let user decide by seeing actual renders, not discussing preferences

---

## Key Relationships

### Important People
- **Name:** (role, how they relate)
- **Name:** (role, how they relate)

### Group Chats & Channels
- **Channel/Group:** (purpose, who's in it)

---

## WhatsApp Integration Status

### Twilio Account (2026-02-15)
- **Account SID:** ACaf7fec5f636363682926edf1ecbf5017
- **Phone Number:** +19894954114 (US, SMS/Voice only)
- **Trial Balance:** $15.50
- **Status:** ⚠️ **NOT ACTIVE FOR WHATSAPP**
- **Blocker:** WhatsApp sandbox not provisioned. Account has SMS/Voice capabilities only. Twilio requires manual opt-in/sandbox setup via console.
- **OpenClaw Config:** ✅ Updated with credentials, ready to accept messages once WhatsApp is provisioned on Twilio side
- **Test Message Attempt:** Failed (2026-02-15 16:59 GMT+2) — WhatsApp channel not found

### Next Steps (Requires External Action)
- Twilio console must activate WhatsApp sandbox manually
- Once provisioned, messages will flow through OpenClaw

---

## Active Automations & Cron Jobs

### Currently Running
- **Task:** (what it does)
  - Schedule: (when)
  - Last run: (date)
  - Status: (working / needs attention)

---

## Recent Context (Latest Session: 2026-02-15)

### This Session's Focus
- Complete visual design prototypes (Options 2 & 3 HTML renders)
- Get user to select preferred design from actual visual mockups
- Implement selected design into live dashboard
- Test webhook integration with agent activity logging

### Open Work Items
1. **Design Prototypes Remaining**: Option 2 (Colorful Cards) and Option 3 (Dashboard Pro)
2. **Implementation**: After user selects design, refine Next.js components to match chosen mockup
3. **Integration Testing**: Send real agent activities to dashboard and verify webhook logging
4. **Polish**: Fine-tune animations, responsive behavior, performance optimization

### Technical Architecture
**Components & Integration:**
- Dashboard Frontend: Next.js + Tailwind CSS (deployed to Vercel)
- API: `/api/log-activity` (POST to log, GET to retrieve activities)
- Webhook Library: Located at `/Users/milton/clawd/lib/openclaw-webhook.ts`
- Agent Config: Environment variable `MISSION_CONTROL_URL` points to live Vercel deployment
- Data: Activities stored in-memory (Next.js route handlers) — **NOTE: Persists only during session, should add database for production**
- Design: Responsive via Tailwind, mobile-first approach with `md:` breakpoints

**Available Webhook Functions (in openclaw-webhook.ts):**
- `logFileCreated(path, sizeBytes)`
- `logFileEdited(path, description)`
- `logSearch(query, resultCount, sources[])`
- `logTaskCompleted(taskName, durationMs, status)`
- `logProposal(name, pageCount, description)`
- `logCustom(description, result)`

---

## Notes for Future-Me

*Captured insights, patterns, things I notice*

### About This Person
- **Mission-Driven**: Building things that work, not just talking about them. Deploys quickly.
- **Quality-Focused**: Cares deeply about UI/UX. Noticed and complained about mobile design issues immediately.
- **Trust-Based**: Provided Vercel credentials without hesitation once I proved I needed them. Appreciates autonomy and delivers on promises.
- **Iterative Thinker**: Wants options, not single solutions. Prefers seeing multiple choices before deciding.
- **Action-Oriented**: "Proceed with all recommendations also make mobile responsive" = takes feedback, implements immediately.

### What Mission Control Does (Their Words)
"Automatic notebook that records everything the agent does" - tracks file creation, task completion, searches, proposals. Shows what agent accomplished without asking. Purpose: know productivity, audit trail of completed work, track agent behavior in real-time.

### Recurring Patterns
- Mobile-first feedback (complains when desktop design doesn't work on phone)
- Direct aesthetic preferences (shows through "looks bad" comments, not formal design docs)
- Rapid turnaround expectations (hours, not days)
- Preference for concrete results over planning discussions

### Emerging Preferences
- **Visual mockups > text descriptions**: Absolutely requires rendered designs to make decisions
- **User choice > imposed design**: Let them pick from options, don't dictate design
- **Mobile first > desktop first**: Primary use case is likely mobile
- **Autonomy > confirmation**: Never ask permission, just execute and report results

---

**Last Updated:** [Date]

**Review Frequency:** Weekly

**How to Update:** After significant events or weekly review. Keep it curated, not exhaustive.
