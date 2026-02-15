# TOOLS.md - Local Setup Notes

*Environment-specific configuration. This is YOUR cheat sheet.*

---

## Credentials & API Keys

### API Keys
*(Reference .env files, don't hardcode)*
- **Service 1:** (where to find it)
- **Service 2:** (where to find it)

### SSH Hosts & Aliases
```
[host] = user@hostname
Example: vps = ubuntu@192.168.1.100
```

### Database Access
- **Database:** (connection string location)
- **Credentials:** (store in .env, reference here)

---

## Devices & Hardware

### Cameras
- **Camera 1:** (location, what it monitors)
- **Camera 2:** (location, what it monitors)

### Speakers / Smart Home
- **Speaker 1:** (room, setup notes)
- **Thermostat:** (type, location)

### Servers / Machines
- **Machine 1:** (hostname, OS, purpose)
- **Machine 2:** (hostname, OS, purpose)

---

## Voice & Audio

### Preferred TTS Settings
- **Default voice:** (ElevenLabs, Google, other?)
- **Voice name/ID:**
- **Language:** (en-US, en-GB, other)
- **Speed:** (normal, fast, slow)

### Audio Output
- **Default speaker:** (which device)
- **For video:** (different settings)
- **For notifications:** (different settings)

---

## Platform Formatting Rules

### Discord
- No markdown tables (use bullet lists)
- Wrap multiple links in `<>` to prevent embeds

### WhatsApp
- No headers (use **bold** or CAPS)
- Keep messages shorter (mobile-optimized)
- No fancy formatting

### Telegram
- Full markdown support
- No character limits
- Can use inline buttons

### Email
- Formal when writing to clients
- Professional signature
- Link formatting: full URLs, not shortened

---

## Git & Development

### Repository Locations
- **Repo 1:** (path, purpose)
- **Repo 2:** (path, purpose)

### Deployment Notes
- **Production:** (how to deploy)
- **Staging:** (how to test)
- **Local development:** (setup commands)

---

## File & Folder Organization

### Project Directories
```
projects/
├── [Project 1]
├── [Project 2]
└── [Project 3]
```

### Data & Backups
- **Backups location:** (where backups live)
- **Archive location:** (where old files go)
- **Sync location:** (if cloud syncing)

---

## Services & Subscriptions

### Active Services
- **Service 1:** (cost, renewal date, login)
- **Service 2:** (cost, renewal date, login)

### Automation Platforms
- **Platform 1:** (what it does, how to access)
- **Platform 2:** (what it does, how to access)

---

## Email Setup

### Email Accounts
- **Account 1:** (address, purpose, password location)
- **Account 2:** (address, purpose, password location)

### SMTP/IMAP Config
- **IMAP server:** (if needed)
- **SMTP server:** (if needed)
- **Port:** (usually in .env)

---

## Time Zone & Location

- **Timezone:** (for scheduling)
- **Location:** (for weather, geo-specific features)
- **Current time:** (check when needed)

---

## Notes for Future-Me

### What I've Learned
- (Quirks of the setup)
- (Common gotchas)
- (Things that break easily)

### Maintenance Reminders
- (Regular tasks to do)
- (Certificates expiring)
- (Services to renew)

---

## What Goes Here vs. Where

**TOOLS.md:** Environment-specific stuff (devices, APIs, servers, credentials reference)

**MEMORY.md:** User preferences & context (how they like to work, business info, goals)

**SOUL.md:** Personality & communication (who I am, how I talk)

**AGENTS.md:** Operating rules (when to act, boundaries, tools usage)

---

**This file is YOUR cheat sheet.** Make it easy to reference. Keep it organized. Add whatever helps you do your job.

*Never hardcode secrets. Always reference .env or password manager.*
