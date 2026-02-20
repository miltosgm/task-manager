# HEARTBEAT.md - Recurring Task Checklist

*Periodic things to check and do. Customize based on your human's needs.*

---

## Critical Daily Tasks

Check these at least once per day:

- [ ] **Emails:** Any urgent unread messages?
- [ ] **Calendar:** Events coming up in next 24-48h?
- [ ] **Mentions:** Any @mentions in Slack/Discord/Telegram?
- [ ] **Status:** Are background jobs running? Any failures?

## Slack Channels to Monitor Every Heartbeat

Always scan these for new messages / @mentions:
- `D0ACZSASYGY` — Miltos DM (primary)
- `C09CKQ6D5K6` — General team channel
- `C0AGS8C3NMN` — Group DM (Miltos + Muhammad Talha + Clawdbot)
- `D0ABZ65075Z` — Muhammad Talha DM (direct)

---

## Weekly Tasks (Every 3-4 Days)

Pick 2-3 of these per check:

- [ ] **Project Status:** Where are active projects? Any blockers?
- [ ] **Memory Review:** Read recent daily logs, distill into MEMORY.md
- [ ] **Automation Check:** Are cron jobs working? Running on schedule?
- [ ] **Team Communication:** Any important updates from key people?
- [ ] **Weather:** Relevant for upcoming plans?

---

## Weekly Memory Maintenance (Once Per Week)

- [ ] Read last 7 days of `memory/YYYY-MM-DD.md`
- [ ] Identify significant events/decisions/lessons
- [ ] Update `MEMORY.md` with curated insights
- [ ] Remove outdated entries from MEMORY.md
- [ ] Archive old daily files (keep rolling 30-day window)

---

## Health Checks (Every 2 Weeks)

- [ ] **Cron jobs:** All scheduled tasks running?
- [ ] **Services:** Any critical services down?
- [ ] **Credentials:** Do API keys/passwords need rotation?
- [ ] **Storage:** Disk space okay? Backups working?
- [ ] **Security:** Any suspicious activity?

---

## Quiet Hours (Never Disturb)

Define when NOT to send messages:
- **Sleeping:** (time range)
- **Work focus time:** (if applicable)
- **Family time:** (if applicable)
- **On vacation:** (don't message unless urgent)

---

## Proactive Work to Do

When you have downtime, do this (in order of priority):

1. **Read and organize daily logs**
   - Scan memory/YYYY-MM-DD.md files
   - Flag important items
   - Link to projects if relevant

2. **Update MEMORY.md**
   - Add significant learnings
   - Refine user preferences
   - Remove outdated entries

3. **Check project status**
   - Pull latest from git
   - Any abandoned branches?
   - Test scripts still working?

4. **Improve documentation**
   - Update TOOLS.md
   - Clean up messy notes
   - Create new guides if needed

5. **Security audit**
   - Review file permissions
   - Check for exposed secrets
   - Tighten access controls

---

## When to Reach Out

Message your human if:
- Important email needs response (check first, but flag if urgent)
- Calendar event coming up in <2 hours
- You found something interesting they'd care about
- Been >8 hours since last contact and something needs attention
- Blocker requires their input
- Automation failed

---

## When to Stay Silent

Reply `HEARTBEAT_OK` if:
- Late night/sleeping hours
- Human is clearly busy
- Nothing new since last check
- Just checked <30 min ago
- No actionable items

---

## Heartbeat Frequency

Default: **Check every 30-60 minutes during active hours**

Adjust based on:
- Human's work schedule (more often when busy)
- Project deadlines (more frequent near launches)
- Automation complexity (more checks if many cron jobs)
- Personal preference (some like constant updates, others prefer daily)

---

**Remember:** Don't just check boxes. Be proactive. If you notice patterns, bring them up. Heartbeats are your chance to add value without waiting to be asked.
