#!/usr/bin/env python3
"""
CDMA Hospitality Playbook - Premium Redesign
Brand: Navy #053a75, Cyan #00e1fc, Light #F0F3F5, Black #000000
Font: Inter (all weights)
"""

import os
import re
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ── Brand Colors ──────────────────────────────────────────────────────────────
NAVY   = HexColor('#053a75')
CYAN   = HexColor('#00e1fc')
LIGHT  = HexColor('#F0F3F5')
BLACK  = HexColor('#000000')
WHITE  = white
GRAY   = HexColor('#8A9AB0')
DGRAY  = HexColor('#2D3748')
LGRAY  = HexColor('#CBD5E0')
NAVY2  = HexColor('#0A4D9E')   # slightly lighter navy for variety
CYAN_SOFT = HexColor('#E0FAFE')  # very light cyan tint

# ── Font Paths ────────────────────────────────────────────────────────────────
FONT_DIR = '/Users/milton/clawd/fonts/inter/inter4/extras/ttf'

def register_fonts():
    fonts = {
        'Inter-Light':      'Inter-Light.ttf',
        'Inter-Regular':    'Inter-Regular.ttf',
        'Inter-Medium':     'Inter-Medium.ttf',
        'Inter-SemiBold':   'Inter-SemiBold.ttf',
        'Inter-Bold':       'Inter-Bold.ttf',
        'Inter-ExtraBold':  'Inter-ExtraBold.ttf',
        'Inter-Black':      'Inter-Black.ttf',
        'Inter-ExtraLight': 'Inter-ExtraLight.ttf',
    }
    for name, filename in fonts.items():
        path = os.path.join(FONT_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        else:
            print(f"Warning: font not found: {path}")

register_fonts()

# ── Page Content Data ─────────────────────────────────────────────────────────
SECTIONS = [
    {
        'num': '01',
        'title': 'Why Hospitality Needs 24/7 IT Support',
        'subtitle': 'Always-on operations, peak season pressure, guest-facing systems',
        'body': [
            ('para', "Hospitality operates around the clock. A server crash at 2 AM during peak season does not wait for business hours. A Wi-Fi outage in a 300-room resort triggers hundreds of guest complaints within minutes. In hospitality, IT is not back-office — it is the guest experience."),
            ('heading3', 'The Hospitality IT Challenge'),
            ('bullet_pairs', [
                ('Always-On Operations', 'Hotels, resorts, and venues operate 24/7/365. Front desk check-ins happen at midnight. Room service flows through POS systems at 3 AM. Housekeeping relies on mobile devices. Any downtime directly impacts the guest experience and revenue.'),
                ('Peak Season Pressure', 'Occupancy surges place enormous strain on networks, PMS systems, and payment processing. Seasonal peaks bring 2–4 devices per guest requiring high-density Wi-Fi. The worst time for an IT failure is precisely when it is most likely to occur.'),
                ('Complex Vendor Ecosystem', 'Hospitality IT involves PMS providers (Opera, Mews, Protel), POS systems (Micros, Lightspeed), IPTV, door lock systems, CCTV, and VoIP. Coordinating between them requires deep domain knowledge.'),
                ('Staff Turnover', 'Hospitality has one of the highest staff turnover rates of any industry. Seasonal hiring means constant onboarding and offboarding of accounts, devices, and credentials — creating operational overhead and security risk.'),
                ('Payment & Privacy Compliance', 'PCI DSS and GDPR are non-negotiable. Guest databases contain PII, payment systems process card transactions continuously, and strict network segmentation must be maintained at all times.'),
                ('Mobile Coverage Gaps', 'Thick walls, basements, and large conference areas create signal dead zones that frustrate guests and hinder staff. Comprehensive 4G/5G coverage (DAS) is an increasingly expected amenity.'),
            ]),
            ('callout', 'The bottom line: Hospitality IT demands proactive 24/7 monitoring and rapid incident response. Reactive support is not an option when guest satisfaction and revenue are on the line.'),
            ('heading3', 'Hospitality Systems We Help Protect'),
            ('table', {
                'headers': ['System', 'Key Platforms', 'Why It Matters'],
                'rows': [
                    ('Property Management System (PMS)', 'Opera, Mews, Protel, Hotelogix', 'Reservations, check-in/out, billing, housekeeping — the heart of operations'),
                    ('Point of Sale (POS)', 'Micros, Lightspeed, Toast', 'Restaurant, bar, and room-service transactions. Must be available 24/7'),
                    ('Guest Wi-Fi', 'Aruba, Cisco Meraki, Ubiquiti', 'The single most common guest complaint when it fails. Non-negotiable.'),
                    ('VoIP & Telephony', 'Teams Phone, Cisco, Avaya', 'Guest-room phones and reception lines. Downtime means missed bookings'),
                    ('Digital Key & Smart Locks', 'Assa Abloy, Dormakaba', 'Keyless entry requires constant connectivity between locks and PMS'),
                    ('CCTV & Access Control', 'Hikvision, Axis, Genetec', 'Critical for guest safety and regulatory compliance'),
                    ('Booking Engines & OTAs', 'Booking.com, Expedia, SiteMinder', 'Real-time inventory sync. A failure can cause overbookings or lost revenue'),
                    ('IPTV & Digital Signage', 'Samsung LYNK, LG Pro:Centric', 'In-room entertainment and lobby displays require constant monitoring'),
                ]
            }),
        ]
    },
    {
        'num': '02',
        'title': 'CDMA Services Overview',
        'subtitle': 'Three pillars: Resilient Infrastructure, Secure Operations, Hotel-Grade Productivity',
        'body': [
            ('para', "CDMA provides a comprehensive suite of managed IT and cybersecurity services structured around three integrated pillars designed specifically for hospitality. All services are delivered white-label — your clients never know we exist."),
            ('heading3', 'Three Integrated Pillars'),
            ('pillar', ('Resilient Infrastructure', 'SD-WAN with automatic failover, Wi-Fi 6/6E high-density networks, enterprise LAN switching with secure VLAN segmentation, and full isolation of guest, PMS, IoT, and admin networks. Your critical systems are always available and performing optimally.')),
            ('pillar', ('Secure Operations', '24/7 network monitoring and MDR/SOC services, advanced endpoint protection and threat detection, continuous vulnerability management, and automated backup and disaster recovery. Your data, guests, and property are protected around the clock.')),
            ('pillar', ('Hotel-Grade Productivity', 'PMS/POS system continuity and monitoring, Teams Phone and VoIP support, IPTV and digital signage management, conference AV, and guest application support. Staff are empowered; guests enjoy superior connectivity.')),
            ('heading3', 'Key Services at a Glance'),
            ('table', {
                'headers': ['Service', 'What It Does', 'Primary Hospitality Benefit'],
                'rows': [
                    ('NOC (24/7)', 'Proactive monitoring, maintenance, and remediation of servers, network devices, and endpoints', 'Guest Wi-Fi uptime, PMS/POS reliability, peak-season readiness'),
                    ('Service Desk (24/7)', 'First-contact technical support for hotel staff via phone and email (white-label)', 'Fast resolution, seasonal staff onboarding, minimal guest disruption'),
                    ('Guest Wi-Fi & Captive Portal', 'Wi-Fi 6/6E high-density wireless, branded portal, PMS integration, analytics', 'Superior connectivity, conference revenue, marketing data capture'),
                    ('Cybersecurity / MDR', '24/7 SOC, EDR, SIEM, next-gen firewall, threat isolation in 15 minutes', 'Ransomware protection, PCI DSS and GDPR compliance support'),
                    ('Mobile DAS', 'Nextivity-powered 4G/5G distributed antenna systems', 'Ubiquitous cellular coverage for guests and staff throughout property'),
                    ('Backup & DR', 'Immutable backups with 15-min RPO, offsite replication, tested DR runbooks', 'Rapid recovery from ransomware, hardware failure, or natural disaster'),
                    ('Deep Dive Assessment', 'RMM platform audit and optimisation, alert tuning for hospitality', 'Reduced noise, better visibility, hospitality-aligned maintenance windows'),
                    ('Project Services', 'New openings, SD-WAN, Wi-Fi 6/6E, migrations, network redesigns', 'On-time delivery, zero guest disruption, documented procedures'),
                ]
            }),
        ]
    },
    {
        'num': '03',
        'title': 'Hospitality Network Architecture',
        'subtitle': 'SD-WAN, VLAN segmentation, access control, SIEM monitoring layers',
        'body': [
            ('para', "A properly segmented network protects guest data, ensures PCI compliance, and maintains performance across all property systems simultaneously. CDMA designs, deploys, and manages enterprise-grade network architectures tailored to the specific demands of hospitality operations."),
            ('callout', 'Micro-segmentation principle: A compromised guest device must never be able to reach payment systems or property management infrastructure. This is enforced at the VLAN level — not just firewall rules — for true defence in depth.'),
            ('heading3', 'Five-Layer Architecture'),
            ('numbered_items', [
                ('01 — Internet & SD-WAN Layer', 'Dual-ISP failover with intelligent traffic routing ensures continuous connectivity even during provider outages. LTE/5G backup ensures VoIP reception can always take reservations even during primary internet failures.'),
                ('02 — Core Security & Switching', 'Next-generation firewall with application awareness and intrusion prevention creates secure network boundaries with deep packet inspection. Managed core switches provide the backbone for all VLAN segregation.'),
                ('03 — VLAN Segmentation', 'Minimum six isolated VLANs: Guest Wi-Fi, Staff/Administration, PMS/POS (PCI-scoped), CCTV, IPTV, IoT devices, and Management. Payment systems sit in their own PCI-scoped segment with no lateral access.'),
                ('04 — Access Control & Captive Portal', 'Branded captive portal with RADIUS authentication. Guests are automatically provisioned access at check-in and removed at check-out via PMS integration. Voucher codes and time-limited access support conference guests.'),
                ('05 — Monitoring & Logging (SIEM)', 'A SIEM platform collects security events, traffic patterns, and system health metrics for 24/7 threat detection. Anomaly detection identifies suspicious behaviour in real time.'),
            ]),
            ('heading3', 'What CDMA Deploys in Hospitality Networks'),
            ('table', {
                'headers': ['Technology', 'Details'],
                'rows': [
                    ('SD-WAN', 'Intelligent dual-ISP failover with automatic traffic rerouting and LTE/5G backup'),
                    ('Wi-Fi 6/6E', 'High-density APs with seamless roaming, per-room bandwidth management, channel optimisation'),
                    ('Enterprise LAN', 'Managed switching with VLAN tagging, QoS prioritisation for PMS/POS, redundant uplinks'),
                    ('VLAN Segmentation', 'Six+ isolated segments: Guest, Staff, PMS/POS (PCI), CCTV, IPTV, IoT, Management'),
                    ('Next-Gen Firewall', 'Deep packet inspection, application awareness, intrusion prevention, web filtering'),
                    ('RADIUS & Captive Portal', 'Centralised authentication with PMS integration, marketing analytics, voucher codes'),
                ]
            }),
        ]
    },
    {
        'num': '04',
        'title': 'NOC for Hospitality',
        'subtitle': 'Proactive monitoring, incident response, coverage tiers, certifications',
        'body': [
            ('para', "Our Network Operations Centre provides 24/7 proactive monitoring, management, and remediation of your hospitality IT infrastructure — keeping guest-facing and back-office systems running without interruption."),
            ('two_col', [
                ('How Does It Work?', 'We monitor your infrastructure using your existing RMM platform or our own SaaS-based monitoring agents. Our NOC team analyses alerts, takes corrective action, and escalates to you only when necessary.'),
                ('Why It Matters in Hospitality', 'A failed firewall at a resort can take down guest Wi-Fi, POS terminals, and door lock controllers simultaneously. Proactive monitoring catches degradation before it becomes a guest-impacting outage.'),
            ]),
            ('heading3', 'What We Monitor'),
            ('bullets', [
                'Guest Wi-Fi access points, controllers, and uptime',
                'VoIP system connectivity and call routing',
                'PMS/POS system availability and response times',
                'Server CPU, memory, disk utilisation, and health',
                'Firewall and network device status and performance',
                'Internet connectivity and SD-WAN failover events',
                'Backup job success and failure with alerting',
                'Endpoint agent status and patch compliance',
                'CCTV and access control system connectivity',
                'UPS and power monitoring for critical equipment',
            ]),
            ('heading3', 'NOC Service Tiers'),
            ('table', {
                'headers': ['Tier', 'Coverage', 'Response Time', 'Scope'],
                'rows': [
                    ('Essential', '24/7 monitoring', 'Alerts within 15 min', 'Core infrastructure monitoring and alerting'),
                    ('Standard', '24/7 monitoring + remediation', 'Incident response <30 min', 'Monitoring, remediation, monthly reports'),
                    ('Premium', '24/7 monitoring + remediation + proactive', 'Priority <15 min', 'Full proactive management, quarterly reviews, dedicated engineer'),
                ]
            }),
        ]
    },
    {
        'num': '05',
        'title': 'Service Desk for Hospitality Teams',
        'subtitle': 'End-user support, user account management, vendor coordination',
        'body': [
            ('para', "CDMA's white-label Service Desk provides 24/7 first-contact technical support for hotel staff, ensuring that IT issues are resolved quickly and professionally — with your branding, not ours."),
            ('heading3', 'Service Desk Capabilities'),
            ('bullet_pairs', [
                ('24/7 Availability', 'Round-the-clock support via phone and email. Staff can reach us at 3 AM when a check-in system fails during peak arrival.'),
                ('White-Label Operation', 'We answer in your name. Guests and staff experience seamless support under your brand identity.'),
                ('Seasonal Onboarding', 'Rapid account provisioning and device setup for seasonal staff. Offboarding at season end to maintain security hygiene.'),
                ('Vendor Coordination', 'We liaise with PMS, POS, IPTV, and other vendors on your behalf — eliminating the time lost coordinating between multiple suppliers.'),
                ('Ticket Management', 'Full ITSM ticketing with SLA tracking, escalation paths, and detailed reporting on resolution times and recurring issues.'),
                ('Remote & On-Site', 'Remote-first resolution with on-site dispatch capability for issues that cannot be resolved remotely.'),
            ]),
            ('heading3', 'Common Hospitality Service Desk Requests'),
            ('bullets', [
                'Guest Wi-Fi connection issues and captive portal troubleshooting',
                'Staff account creation, password resets, and access rights',
                'PMS/POS connectivity and application support',
                'Printer, scanner, and peripheral device issues',
                'Email and Microsoft 365 support for hotel management',
                'VoIP and Teams Phone configuration and troubleshooting',
                'New device setup and configuration',
                'Software installation and licensing management',
            ]),
        ]
    },
    {
        'num': '06',
        'title': 'Guest Wi-Fi & Captive Portal',
        'subtitle': 'Wi-Fi 6/6E design, branded portal, network analytics, conference revenue',
        'body': [
            ('para', "Guest Wi-Fi is the most visible IT service in any hospitality property. CDMA designs, deploys, and manages enterprise-grade Wi-Fi infrastructure that delivers exceptional connectivity for guests while protecting property operations."),
            ('heading3', 'Wi-Fi 6/6E Design Principles'),
            ('bullet_pairs', [
                ('High-Density Coverage', 'Purpose-designed access point placement for high-density environments including conference halls, pool areas, and guest rooms. Every square metre covered.'),
                ('Seamless Roaming', 'Guests move freely throughout the property without reconnecting. 802.11r fast transition ensures uninterrupted VoIP and streaming.'),
                ('Per-Room Bandwidth Management', 'Intelligent QoS policies ensure fair bandwidth allocation. Premium guests can receive elevated allocations without manual configuration.'),
                ('Network Analytics', 'Real-time visibility into device counts, bandwidth consumption, and signal quality. Data feeds marketing insights about guest behaviour patterns.'),
            ]),
            ('heading3', 'Captive Portal Features'),
            ('bullets', [
                'Fully branded portal with hotel logo, colours, and messaging',
                'PMS integration — automatic guest access at check-in, revoked at check-out',
                'Tiered access: complimentary basic, premium paid tiers for high-bandwidth guests',
                'Conference and event voucher codes with time-limited and bandwidth-limited access',
                'Marketing consent capture integrated with CRM systems',
                'Multi-language support for international guests',
                'GDPR-compliant data handling and retention policies',
                'Analytics dashboard: session counts, peak usage times, device types',
            ]),
            ('callout', 'Revenue opportunity: Conference and events Wi-Fi can generate significant additional income through tiered access packages. CDMA can design and implement monetisation models for event spaces.'),
        ]
    },
    {
        'num': '07',
        'title': 'Property Systems Continuity',
        'subtitle': 'PMS/POS monitoring, IPTV, digital signage, Teams Phone & VoIP',
        'body': [
            ('para', "Hotel operations depend on a constellation of interconnected systems. CDMA monitors and manages the full technology stack — from property management and point-of-sale to in-room entertainment and communication platforms."),
            ('heading3', 'Systems We Monitor and Support'),
            ('table', {
                'headers': ['System', 'Coverage', 'Key Risk'],
                'rows': [
                    ('PMS (Opera, Mews, Protel)', '24/7 uptime monitoring, connectivity assurance', 'Front desk paralysis, check-in failures'),
                    ('POS (Micros, Lightspeed)', 'Transaction monitoring, failover support', 'Revenue loss, guest frustration at F&B outlets'),
                    ('IPTV (Samsung LYNK, LG Pro)', 'Channel availability, system restarts', 'Guest experience degradation'),
                    ('Digital Signage', 'Content delivery monitoring, display uptime', 'Brand and information gaps'),
                    ('Teams Phone / VoIP', 'Call quality monitoring, extension availability', 'Missed reservations, reception downtime'),
                    ('Conference AV', 'Pre-event testing, live monitoring', 'Event failures affecting revenue'),
                    ('Digital Key Systems', 'API integration monitoring', 'Guest lockouts, security incidents'),
                ]
            }),
        ]
    },
    {
        'num': '08',
        'title': 'Cybersecurity for Hotels',
        'subtitle': 'Prevent, Detect & Respond, MDR/SOC, PCI DSS, GDPR alignment',
        'body': [
            ('para', "Hotels are high-value targets for cybercriminals. Guest payment data, personal information, and the need for continuous operations make hospitality properties attractive and vulnerable. CDMA's layered security approach addresses every threat vector."),
            ('heading3', 'Three Layers of Protection'),
            ('numbered_items', [
                ('Prevent', 'Next-generation firewall with application awareness and web filtering. Network micro-segmentation ensuring PCI-scoped POS systems are isolated. Endpoint protection on all managed devices. Vulnerability scanning and patch management.'),
                ('Detect', '24/7 SIEM monitoring with correlation rules tuned for hospitality environments. Anomaly detection identifying unusual traffic patterns. User behaviour analytics. Threat intelligence feeds updated in real time.'),
                ('Respond', 'Managed Detection and Response (MDR) with 15-minute threat isolation SLA. Documented incident response playbooks. Forensic capability. Post-incident reporting with root cause analysis and remediation recommendations.'),
            ]),
            ('heading3', 'Compliance Alignment'),
            ('bullet_pairs', [
                ('PCI DSS', 'Cardholder data environment scoping, network segmentation validation, quarterly vulnerability scanning, penetration testing coordination.'),
                ('GDPR', 'Data mapping support, breach notification procedures, processor agreement templates, privacy impact assessment support.'),
                ('ISO 27001:2022', 'CDMA operates under ISO 27001:2022 certification, ensuring information security management best practices across all services.'),
                ('NIS2 / DORA', 'Advisory support for properties falling under NIS2 or financial services obligations through management company structures.'),
            ]),
        ]
    },
    {
        'num': '09',
        'title': 'Mobile DAS Solutions',
        'subtitle': 'Nextivity-powered 4G/5G coverage, eliminating dead zones throughout property',
        'body': [
            ('para', "Mobile signal dead zones frustrate guests and impede staff communications. CDMA deploys Distributed Antenna Systems (DAS) powered by Nextivity technology to deliver consistent 4G/5G coverage throughout even the most challenging property layouts."),
            ('heading3', 'The Challenge'),
            ('para', "Thick concrete walls, underground car parks, basement conference rooms, and large atrium spaces all create cellular dead zones. Guests complain. Staff cannot receive calls or use mobile applications. Emergency communications may be compromised."),
            ('heading3', 'CDMA\'s Nextivity DAS Solution'),
            ('bullet_pairs', [
                ('Carrier-Agnostic Coverage', 'Nextivity systems amplify all major carrier signals simultaneously — guests on any network receive improved coverage without carrier partnerships or site licensing complexity.'),
                ('Passive & Active DAS', 'We design and install both passive distributed antenna systems for smaller properties and active DAS for large resort complexes or multi-storey hotels.'),
                ('4G & 5G Ready', 'Future-proof infrastructure supporting both 4G LTE and 5G NR frequencies, ensuring your investment remains relevant as networks evolve.'),
                ('Professional Survey & Design', 'Site RF surveys identify coverage gaps precisely. System design ensures every area — including pool decks, spa, and underground parking — receives adequate signal.'),
            ]),
        ]
    },
    {
        'num': '10',
        'title': 'Backup & Disaster Recovery',
        'subtitle': '15-min RPO, immutable backups, documented DR runbooks, tested recovery',
        'body': [
            ('para', "A ransomware attack, hardware failure, or natural disaster can bring hospitality operations to a standstill. CDMA's backup and disaster recovery services ensure rapid recovery with documented, tested runbooks — not last-minute improvisation."),
            ('heading3', 'Key Metrics'),
            ('table', {
                'headers': ['Metric', 'CDMA Standard', 'Why It Matters'],
                'rows': [
                    ('Recovery Point Objective (RPO)', '15 minutes', 'Maximum data loss window — only 15 minutes of transactions at risk'),
                    ('Recovery Time Objective (RTO)', 'Defined per system tier', 'How quickly systems are restored — prioritised for PMS and POS first'),
                    ('Backup Frequency', 'Continuous to hourly depending on criticality', 'Critical systems backed up continuously; others on schedules'),
                    ('Retention Period', 'Configurable — typically 30/90/365 days', 'Meets regulatory requirements for financial and guest data'),
                    ('Offsite Replication', 'Encrypted offsite copy always maintained', 'Site disaster cannot destroy primary and backup simultaneously'),
                    ('Immutability', 'Write-once backup repositories', 'Ransomware cannot encrypt or delete backup data'),
                ]
            }),
            ('heading3', 'DR Runbooks'),
            ('para', "Every managed property has a documented disaster recovery runbook specific to its technology stack. Runbooks are tested at least annually (more frequently for Premium tier). Recovery procedures cover ransomware, hardware failure, ISP outage, and site-level disasters."),
        ]
    },
    {
        'num': '11',
        'title': 'Deep Dive Assessment',
        'subtitle': 'RMM platform audit, alert noise reduction, maintenance optimisation',
        'body': [
            ('para', "Before full managed services engagement, CDMA conducts a structured Deep Dive Assessment of the existing IT environment. This surfaces configuration debt, security gaps, and optimisation opportunities — providing a clear baseline for service delivery."),
            ('heading3', 'Assessment Scope'),
            ('bullets', [
                'RMM platform configuration review and alert threshold optimisation',
                'Network topology mapping and security posture review',
                'Firewall rule audit and redundancy identification',
                'Backup configuration validation and test recovery',
                'Endpoint inventory and patch status baseline',
                'Vulnerability scan across managed infrastructure',
                'Hospitality-specific maintenance window recommendations',
                'Current monitoring coverage gap identification',
            ]),
            ('heading3', 'Deliverables'),
            ('bullet_pairs', [
                ('Executive Summary Report', 'Business-language overview of findings, risks, and recommended priorities for senior management.'),
                ('Technical Detail Report', 'Configuration-level findings, remediation steps, and implementation priorities for the IT team.'),
                ('Remediation Roadmap', 'Prioritised action plan with timelines and resource requirements.'),
                ('Baseline Documentation', 'Network diagrams, asset inventory, and configuration snapshots for ongoing reference.'),
            ]),
        ]
    },
    {
        'num': '12',
        'title': 'Project Services for Hospitality',
        'subtitle': 'New openings, migrations, network redesigns, seasonal rollouts',
        'body': [
            ('para', "Beyond ongoing managed services, CDMA delivers complex technology projects for hospitality properties — from new hotel openings to full network redesigns and system migrations."),
            ('heading3', 'Project Capabilities'),
            ('bullet_pairs', [
                ('New Hotel Openings', 'End-to-end technology deployment for new properties — network infrastructure, Wi-Fi, PMS integration, VoIP, and cabling. On-site presence through opening and staff training included.'),
                ('Network Redesigns', 'Legacy infrastructure replacement with modern SD-WAN, Wi-Fi 6/6E, and micro-segmented architecture. Zero-downtime migration planning.'),
                ('SD-WAN Deployment', 'ISP procurement support, hardware installation, configuration, and handover. Dual-ISP failover tested before go-live.'),
                ('Wi-Fi 6/6E Upgrades', 'Site survey, access point placement design, installation, and tuning. Coverage validation with client sign-off.'),
                ('Seasonal Rollouts', 'Pre-season infrastructure checks, capacity additions, and system updates. Pre-peak readiness assessments for resorts with significant occupancy variation.'),
                ('PMS/POS Migrations', 'Coordination with PMS and POS vendors for platform migrations. Network preparation, testing, and cutover support.'),
            ]),
        ]
    },
    {
        'num': '13',
        'title': 'Onboarding Process',
        'subtitle': 'Nine-step structured onboarding for single sites and multi-property groups',
        'body': [
            ('para', "CDMA's structured onboarding process ensures smooth transitions from existing providers or from unmanaged environments. Every engagement follows a documented nine-step process adapted for single properties and multi-site groups."),
            ('numbered_items', [
                ('Discovery & Scoping', 'Initial discovery call to understand the property, existing infrastructure, current pain points, and service requirements. Contract and commercial terms agreed.'),
                ('Technical Discovery', 'Remote and on-site technical assessment of existing infrastructure. Network diagrams, asset inventories, and credential collection.'),
                ('Platform Integration', 'Integration of property systems into CDMA NOC and Service Desk platforms. RMM agent deployment, monitoring configuration.'),
                ('Baseline & Tuning', 'Alert threshold establishment, maintenance window configuration, escalation path definition. First week of monitoring with tuning.'),
                ('Security Hardening', 'Firewall rule review, network segmentation validation, endpoint protection deployment, backup configuration.'),
                ('Service Desk Activation', 'Staff communication about new service desk contact details, ticketing procedures, and escalation paths. White-label configuration.'),
                ('Knowledge Transfer', 'Documentation of property-specific procedures, vendor contacts, and escalation preferences for NOC and Service Desk teams.'),
                ('Go-Live', 'Full service commencement. Dedicated contact point for first 30 days to address any service delivery adjustments.'),
                ('30-Day Review', 'Service delivery review meeting. Alert volume analysis, ticket trends, and service optimisation recommendations.'),
            ]),
        ]
    },
    {
        'num': '14',
        'title': 'Service Level Agreement (SLA)',
        'subtitle': 'Essential / Standard / Premium tiers with defined response times',
        'body': [
            ('para', "CDMA's tiered SLA structure provides flexibility for properties with different requirements and budgets while maintaining clear, contractual performance commitments."),
            ('table', {
                'headers': ['Tier', 'Essential', 'Standard', 'Premium'],
                'rows': [
                    ('Monitoring', '24/7', '24/7', '24/7'),
                    ('P1 Response', '30 minutes', '15 minutes', '5 minutes'),
                    ('P2 Response', '2 hours', '1 hour', '30 minutes'),
                    ('P3 Response', 'Next business day', '4 hours', '2 hours'),
                    ('Service Desk', 'Business hours', '24/7', '24/7 dedicated'),
                    ('Monthly Reporting', '✓', '✓', '✓ + executive summary'),
                    ('Quarterly Reviews', '—', '✓', '✓ + dedicated engineer'),
                    ('Pre-Peak Assessment', '—', '—', '✓ annually'),
                ]
            }),
            ('heading3', 'Priority Definitions'),
            ('bullet_pairs', [
                ('Priority 1 (Critical)', 'Complete service outage affecting guest-facing systems, PMS/POS unavailability, or active security incident. Requires immediate response.'),
                ('Priority 2 (High)', 'Significant degradation of key systems, partial connectivity loss, or security alert requiring investigation. Response within SLA tier window.'),
                ('Priority 3 (Medium)', 'Single-user or non-critical system issues, service requests, and informational alerts. Resolved within business cycle.'),
                ('Priority 4 (Low)', 'Enhancement requests, scheduled maintenance, and documentation updates. Addressed in next scheduled review.'),
            ]),
        ]
    },
    {
        'num': '15',
        'title': 'Escalation Process',
        'subtitle': 'NOC and Service Desk escalation paths, timeframes, and contacts',
        'body': [
            ('para', "Clear escalation paths ensure that every issue reaches the right person at the right time — whether at CDMA or within your organisation."),
            ('heading3', 'NOC Escalation Path'),
            ('numbered_items', [
                ('Level 1 — NOC Analyst', 'First response: alert triage, initial remediation attempt, documentation.'),
                ('Level 2 — Senior NOC Engineer', 'Escalated within 15–30 minutes if unresolved. Advanced troubleshooting, vendor engagement.'),
                ('Level 3 — NOC Team Lead', 'Management escalation for P1 incidents. Client notification, stakeholder updates every 30 minutes.'),
                ('Level 4 — CDMA Management', 'For incidents exceeding 2 hours or with significant business impact. Executive communication and resource allocation.'),
            ]),
            ('heading3', 'Service Desk Escalation Path'),
            ('numbered_items', [
                ('Level 1 — Service Desk Agent', 'First contact: issue logging, initial troubleshooting, basic resolution.'),
                ('Level 2 — Service Desk Senior', 'Escalated for complex issues or when Level 1 resolution time exceeds SLA target.'),
                ('Level 3 — Technical Specialist', 'Engineering-level investigation, vendor liaison, on-site dispatch coordination.'),
                ('Level 4 — Service Delivery Manager', 'Client relationship management for recurring issues or service dissatisfaction.'),
            ]),
            ('callout', 'All P1 incidents trigger automatic notification to your designated contacts via SMS and email within 5 minutes of detection — regardless of time of day.'),
        ]
    },
    {
        'num': '16',
        'title': 'Security and Compliance',
        'subtitle': 'ISO 27001:2022, NIS2, DORA, GDPR, PCI DSS, SOC 2 Type II',
        'body': [
            ('para', "CDMA operates under a rigorous security and compliance framework, ensuring that our services meet international standards and regulatory requirements applicable to our hospitality clients."),
            ('heading3', 'Certifications & Frameworks'),
            ('table', {
                'headers': ['Framework', 'Status', 'Relevance to Hospitality'],
                'rows': [
                    ('ISO 27001:2022', 'CDMA certified', 'Information security management — baseline for all service delivery'),
                    ('PCI DSS', 'Advisory and support services', 'Guest payment card data protection and network segmentation'),
                    ('GDPR', 'Compliant + client support', 'Guest personal data handling, breach notification, DPA templates'),
                    ('SOC 2 Type II', 'In progress', 'Security, availability, and confidentiality assurance for MSP clients'),
                    ('NIS2', 'Advisory', 'Network and information security for relevant hospitality operators'),
                    ('DORA', 'Advisory', 'Digital operational resilience for hospitality groups with financial services linkage'),
                ]
            }),
        ]
    },
    {
        'num': '17',
        'title': 'About CDMA',
        'subtitle': 'Established 2011, 56 countries, 6 continents, offices in Nicosia, Dubai & Athens',
        'body': [
            ('para', "CDMA Services Ltd was established in 2011 with a vision to deliver enterprise-grade managed IT and cybersecurity services to organisations of all sizes across global markets."),
            ('heading3', 'By the Numbers'),
            ('table', {
                'headers': ['Metric', 'Detail'],
                'rows': [
                    ('Founded', '2011'),
                    ('Global Reach', '56 countries across 6 continents'),
                    ('Offices', 'Nicosia (HQ), Dubai, Athens'),
                    ('Certifications', 'ISO 27001:2022, multiple vendor certifications'),
                    ('Service Model', 'White-label managed services and cybersecurity'),
                    ('Availability', '24/7/365 NOC and Service Desk'),
                    ('Specialisations', 'Hospitality, healthcare, financial services, and enterprise'),
                ]
            }),
            ('heading3', 'Our Hospitality Expertise'),
            ('para', "CDMA has extensive experience supporting hospitality organisations across the Mediterranean, Middle East, and beyond. Our teams understand the seasonal pressures, system interdependencies, and compliance requirements unique to the hotel industry — delivering IT support that truly understands the hospitality context."),
            ('heading3', 'Contact'),
            ('bullet_pairs', [
                ('Web', 'cdma.com.cy'),
                ('Email', 'sales@cdma.com.cy'),
                ('Phone', '+357 22 028014'),
                ('HQ', 'Nicosia, Cyprus'),
            ]),
        ]
    },
]

TOC_ENTRIES = [
    ('01', 'Why Hospitality Needs 24/7 IT Support', 'Always-on operations, peak season pressure, guest-facing systems'),
    ('02', 'CDMA Services Overview', 'Three pillars: Resilient Infrastructure, Secure Operations, Hotel-Grade Productivity'),
    ('03', 'Hospitality Network Architecture', 'SD-WAN, VLAN segmentation, access control, SIEM monitoring layers'),
    ('04', 'NOC for Hospitality', 'Proactive monitoring, incident response, coverage tiers, certifications'),
    ('05', 'Service Desk for Hospitality Teams', 'End-user support, user account management, vendor coordination'),
    ('06', 'Guest Wi-Fi & Captive Portal', 'Wi-Fi 6/6E design, branded portal, network analytics, conference revenue'),
    ('07', 'Property Systems Continuity', 'PMS/POS monitoring, IPTV, digital signage, Teams Phone & VoIP'),
    ('08', 'Cybersecurity for Hotels', 'Prevent, Detect & Respond, MDR/SOC, PCI DSS, GDPR alignment'),
    ('09', 'Mobile DAS Solutions', 'Nextivity-powered 4G/5G coverage, eliminating dead zones throughout property'),
    ('10', 'Backup & Disaster Recovery', '15-min RPO, immutable backups, documented DR runbooks, tested recovery'),
    ('11', 'Deep Dive Assessment', 'RMM platform audit, alert noise reduction, maintenance optimisation'),
    ('12', 'Project Services for Hospitality', 'New openings, migrations, network redesigns, seasonal rollouts'),
    ('13', 'Onboarding Process', 'Nine-step structured onboarding for single sites and multi-property groups'),
    ('14', 'Service Level Agreement (SLA)', 'Essential / Standard / Premium tiers with defined response times'),
    ('15', 'Escalation Process', 'NOC and Service Desk escalation paths, timeframes, and contacts'),
    ('16', 'Security and Compliance', 'ISO 27001:2022, NIS2, DORA, GDPR, PCI DSS, SOC 2 Type II'),
    ('17', 'About CDMA', 'Established 2011, 56 countries, 6 continents, offices in Nicosia, Dubai & Athens'),
]


# ── Low-level Drawing Helpers ─────────────────────────────────────────────────

def draw_header_bar(c, page_w, page_h, is_landscape=True):
    """Thin navy top bar with page branding."""
    bar_h = 8 * mm
    c.setFillColor(NAVY)
    c.rect(0, page_h - bar_h, page_w, bar_h, fill=1, stroke=0)
    # Cyan accent strip
    c.setFillColor(CYAN)
    c.rect(0, page_h - bar_h - 1.5, page_w * 0.25, 1.5, fill=1, stroke=0)

def draw_footer(c, page_w, page_h, page_num, total=None):
    """Footer with brand line."""
    footer_y = 8 * mm
    # Light separator line
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(15 * mm, footer_y + 4 * mm, page_w - 15 * mm, footer_y + 4 * mm)
    # Left: company info
    c.setFont('Inter-Regular', 7)
    c.setFillColor(GRAY)
    c.drawString(15 * mm, footer_y, 'CDMA Services Ltd  |  cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    # Right: page number
    c.setFont('Inter-SemiBold', 7)
    c.setFillColor(NAVY)
    pg_str = f'Page {page_num}'
    c.drawRightString(page_w - 15 * mm, footer_y, pg_str)

def draw_interior_header(c, page_w, page_h, doc_title='CDMA HOSPITALITY PLAYBOOK'):
    """Minimal top bar for interior pages."""
    bar_h = 10 * mm
    c.setFillColor(NAVY)
    c.rect(0, page_h - bar_h, page_w, bar_h, fill=1, stroke=0)
    c.setFont('Inter-SemiBold', 8)
    c.setFillColor(WHITE)
    c.drawString(15 * mm, page_h - bar_h + 3.2 * mm, doc_title)
    # Cyan accent
    c.setFillColor(CYAN)
    c.setFont('Inter-Regular', 7)
    c.drawRightString(page_w - 15 * mm, page_h - bar_h + 3.2 * mm, 'cdma.com.cy  |  +357 22 028014')

def draw_section_number_accent(c, x, y, num_str, radius=14):
    """Draw a navy circle with section number."""
    c.setFillColor(NAVY)
    c.circle(x + radius, y - radius, radius, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont('Inter-Bold', 11)
    c.drawCentredString(x + radius, y - radius - 3.5, num_str)


# ── Cover Page ────────────────────────────────────────────────────────────────

def draw_cover_landscape(c, page_w, page_h):
    """Premium landscape cover page."""
    W, H = page_w, page_h

    # Full navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Large cyan geometric accent — top-right quadrant
    c.setFillColor(CYAN)
    # Big arc / quarter circle decorative
    c.saveState()
    c.setFillAlpha(0.08)
    c.circle(W, H, H * 0.8, fill=1, stroke=0)
    c.restoreState()

    # Cyan solid strip — left edge
    c.setFillColor(CYAN)
    c.rect(0, 0, 6 * mm, H, fill=1, stroke=0)

    # Subtle grid dots pattern (decorative)
    c.setFillColor(WHITE)
    c.saveState()
    c.setFillAlpha(0.04)
    for row in range(0, int(H / (8 * mm)) + 1):
        for col in range(0, int(W / (8 * mm)) + 1):
            c.circle(col * 8 * mm, row * 8 * mm, 1.5, fill=1, stroke=0)
    c.restoreState()

    # Horizontal cyan line accent
    c.setFillColor(CYAN)
    c.rect(20 * mm, H * 0.52, W * 0.55, 1.5, fill=1, stroke=0)

    # ── Text ──
    left_x = 22 * mm
    center_y = H * 0.5

    # CDMA — large
    c.setFont('Inter-Black', 80)
    c.setFillColor(WHITE)
    c.drawString(left_x, center_y + 45, 'CDMA')

    # HOSPITALITY — medium bold
    c.setFont('Inter-Bold', 38)
    c.setFillColor(CYAN)
    c.drawString(left_x, center_y + 5, 'HOSPITALITY')

    # PLAYBOOK — medium regular
    c.setFont('Inter-Light', 38)
    c.setFillColor(WHITE)
    c.drawString(left_x, center_y - 32, 'PLAYBOOK')

    # Divider line
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.5)
    c.line(left_x, center_y - 48, left_x + 120 * mm, center_y - 48)

    # Subtitle
    c.setFont('Inter-Light', 11)
    c.setFillColor(HexColor('#A8BFDA'))
    c.drawString(left_x, center_y - 62, 'A Comprehensive Guide to CDMA\'s Managed IT &')
    c.drawString(left_x, center_y - 75, 'Cybersecurity Services for Hospitality Organisations')

    # Edition
    c.setFont('Inter-SemiBold', 9)
    c.setFillColor(CYAN)
    c.drawString(left_x, center_y - 95, 'MAY 2025 EDITION')

    # Bottom info bar
    bar_h = 14 * mm
    c.setFillColor(HexColor('#021f42'))
    c.rect(0, 0, W, bar_h, fill=1, stroke=0)
    c.setFont('Inter-Regular', 8)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(22 * mm, 4.5 * mm, 'CDMA Services Ltd  |  cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 8)
    c.setFillColor(CYAN)
    c.drawRightString(W - 22 * mm, 4.5 * mm, 'CONFIDENTIAL')

    # Right side decorative text
    c.saveState()
    c.translate(W - 18 * mm, H / 2)
    c.rotate(90)
    c.setFont('Inter-ExtraLight', 9)
    c.setFillColor(HexColor('#1a4070'))
    c.drawCentredString(0, 0, 'MANAGED IT  ·  CYBERSECURITY  ·  HOSPITALITY TECHNOLOGY')
    c.restoreState()


def draw_cover_portrait(c, page_w, page_h):
    """Premium portrait cover page."""
    W, H = page_w, page_h

    # Full navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Cyan left strip
    c.setFillColor(CYAN)
    c.rect(0, 0, 5 * mm, H, fill=1, stroke=0)

    # Large decorative circle (top right)
    c.saveState()
    c.setFillColor(CYAN)
    c.setFillAlpha(0.06)
    c.circle(W, H, H * 0.6, fill=1, stroke=0)
    c.restoreState()

    # Subtle grid dots
    c.saveState()
    c.setFillColor(WHITE)
    c.setFillAlpha(0.03)
    for row in range(0, int(H / (10 * mm)) + 1):
        for col in range(0, int(W / (10 * mm)) + 1):
            c.circle(col * 10 * mm, row * 10 * mm, 1.5, fill=1, stroke=0)
    c.restoreState()

    # Upper cyan accent strip
    c.setFillColor(CYAN)
    c.rect(15 * mm, H * 0.55, W * 0.65, 1.5, fill=1, stroke=0)

    # ── Text ──
    left_x = 17 * mm
    title_y = H * 0.54

    # CDMA
    c.setFont('Inter-Black', 70)
    c.setFillColor(WHITE)
    c.drawString(left_x, title_y + 50, 'CDMA')

    # HOSPITALITY
    c.setFont('Inter-Bold', 32)
    c.setFillColor(CYAN)
    c.drawString(left_x, title_y + 12, 'HOSPITALITY')

    # PLAYBOOK
    c.setFont('Inter-Light', 32)
    c.setFillColor(WHITE)
    c.drawString(left_x, title_y - 22, 'PLAYBOOK')

    # Line
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.5)
    c.line(left_x, title_y - 36, left_x + 80 * mm, title_y - 36)

    # Subtitle — wrapped
    c.setFont('Inter-Light', 10)
    c.setFillColor(HexColor('#A8BFDA'))
    c.drawString(left_x, title_y - 50, 'A Comprehensive Guide to CDMA\'s')
    c.drawString(left_x, title_y - 62, 'Managed IT & Cybersecurity Services')
    c.drawString(left_x, title_y - 74, 'for Hospitality Organisations')

    # Edition
    c.setFont('Inter-SemiBold', 8)
    c.setFillColor(CYAN)
    c.drawString(left_x, title_y - 92, 'MAY 2025 EDITION')

    # Bottom bar
    bar_h = 16 * mm
    c.setFillColor(HexColor('#021f42'))
    c.rect(0, 0, W, bar_h, fill=1, stroke=0)
    c.setFont('Inter-Regular', 7.5)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(17 * mm, 10 * mm, 'cdma.com.cy  |  sales@cdma.com.cy')
    c.drawString(17 * mm, 4.5 * mm, '+357 22 028014  |  CDMA Services Ltd')
    c.setFont('Inter-SemiBold', 7.5)
    c.setFillColor(CYAN)
    c.drawRightString(W - 17 * mm, 7 * mm, 'CONFIDENTIAL')


# ── Introduction Page ─────────────────────────────────────────────────────────

def draw_intro(c, page_w, page_h, is_landscape, page_num):
    W, H = page_w, page_h
    draw_interior_header(c, W, H)
    draw_footer(c, W, H, page_num)

    margin = 15 * mm
    header_h = 10 * mm
    footer_h = 14 * mm
    content_y = H - header_h - 8 * mm
    content_w = W - 2 * margin

    # Section label
    c.setFont('Inter-SemiBold', 9)
    c.setFillColor(CYAN)
    c.drawString(margin, content_y, 'INTRODUCTION')

    content_y -= 10 * mm

    # Title
    c.setFont('Inter-Bold', 24)
    c.setFillColor(NAVY)
    c.drawString(margin, content_y, 'Hospitality Never Sleeps.')

    content_y -= 8 * mm

    # Cyan line
    c.setFillColor(CYAN)
    c.rect(margin, content_y, 30 * mm, 2, fill=1, stroke=0)

    content_y -= 8 * mm

    # Body text
    intro_text = (
        "Your guests expect seamless connectivity, instant service, and zero downtime — "
        "24 hours a day, 365 days a year. Behind every smooth check-in, reliable guest Wi-Fi "
        "connection, and flawless point-of-sale transaction sits a complex IT infrastructure "
        "that demands constant attention."
    )
    _draw_wrapped_text(c, intro_text, margin, content_y, content_w, 'Inter-Regular', 10.5, DGRAY, 14)
    content_y -= _text_height(intro_text, content_w, 10.5, 14) + 6 * mm

    para2 = (
        "This playbook has been created specifically for hospitality organisations and the "
        "Managed Service Providers (MSPs) who support them. It explores CDMA's full suite of "
        "services in the context of hotel groups, resorts, boutique properties, and hospitality "
        "venues — explaining how our NOC, Service Desk, cybersecurity, network architecture, "
        "and project capabilities address the unique demands of this fast-moving industry."
    )
    _draw_wrapped_text(c, para2, margin, content_y, content_w, 'Inter-Regular', 10.5, DGRAY, 14)
    content_y -= _text_height(para2, content_w, 10.5, 14) + 6 * mm

    para3 = (
        "Whether you manage a single property or a portfolio spanning multiple countries, CDMA "
        "provides the always-on IT backbone that hospitality demands — from guest Wi-Fi and "
        "captive portal design to Mobile DAS, backup and disaster recovery, and 24/7 managed "
        "detection and response."
    )
    _draw_wrapped_text(c, para3, margin, content_y, content_w, 'Inter-Regular', 10.5, DGRAY, 14)
    content_y -= _text_height(para3, content_w, 10.5, 14) + 8 * mm

    # Callout box
    callout_text = (
        "All CDMA services are delivered on a white-label basis. From your guests' and staff's "
        "perspective, we operate as a seamless extension of your own IT team."
    )
    _draw_callout(c, callout_text, margin, content_y, content_w)


# ── Table of Contents ──────────────────────────────────────────────────────────

def draw_toc(c, page_w, page_h, is_landscape, page_num):
    W, H = page_w, page_h
    draw_interior_header(c, W, H)
    draw_footer(c, W, H, page_num)

    margin = 15 * mm
    header_h = 10 * mm
    content_y = H - header_h - 10 * mm
    content_w = W - 2 * margin

    # Title
    c.setFont('Inter-SemiBold', 9)
    c.setFillColor(CYAN)
    c.drawString(margin, content_y, 'CONTENTS')
    content_y -= 8 * mm

    c.setFont('Inter-Bold', 22)
    c.setFillColor(NAVY)
    c.drawString(margin, content_y, 'Table of Contents')
    content_y -= 5 * mm

    c.setFillColor(CYAN)
    c.rect(margin, content_y, 25 * mm, 2, fill=1, stroke=0)
    content_y -= 10 * mm

    # TOC entries
    row_h = 8.5 * mm
    for idx, (num, title, subtitle) in enumerate(TOC_ENTRIES):
        if content_y < 20 * mm:
            break

        # Alternating background
        if idx % 2 == 0:
            c.setFillColor(HexColor('#F7F9FB'))
            c.rect(margin, content_y - row_h + 2.5 * mm, content_w, row_h, fill=1, stroke=0)

        # Number badge
        badge_r = 5.5 * mm
        c.setFillColor(NAVY)
        c.circle(margin + badge_r, content_y - 1 * mm, badge_r, fill=1, stroke=0)
        c.setFont('Inter-Bold', 7)
        c.setFillColor(WHITE)
        c.drawCentredString(margin + badge_r, content_y - 3, num)

        # Title
        c.setFont('Inter-SemiBold', 9.5)
        c.setFillColor(NAVY)
        c.drawString(margin + badge_r * 2 + 3 * mm, content_y + 0.5 * mm, title)

        # Subtitle
        c.setFont('Inter-Light', 8)
        c.setFillColor(GRAY)
        c.drawString(margin + badge_r * 2 + 3 * mm, content_y - 4.5 * mm, subtitle)

        # Cyan dot on right
        c.setFillColor(CYAN)
        c.circle(W - margin - 2, content_y - 1 * mm, 2.5, fill=1, stroke=0)

        content_y -= row_h


# ── Section Content Page ───────────────────────────────────────────────────────

def draw_section(c, page_w, page_h, section, page_num):
    W, H = page_w, page_h
    draw_interior_header(c, W, H)
    draw_footer(c, W, H, page_num)

    margin = 15 * mm
    header_h = 10 * mm
    footer_h = 14 * mm
    content_y = H - header_h - 8 * mm
    content_w = W - 2 * margin
    bottom_limit = footer_h + 4 * mm

    # Section number + title area — navy bar
    sec_bar_h = 18 * mm
    c.setFillColor(NAVY)
    c.rect(0, content_y - sec_bar_h, W, sec_bar_h, fill=1, stroke=0)

    # Section number
    c.setFont('Inter-Black', 28)
    c.setFillColor(CYAN)
    c.drawString(margin, content_y - sec_bar_h + 5, section['num'])

    # Title
    c.setFont('Inter-Bold', is_big_font(section['title']))
    c.setFillColor(WHITE)
    c.drawString(margin + 22 * mm, content_y - sec_bar_h / 2 + 2, section['title'])

    # Subtitle
    c.setFont('Inter-Light', 8.5)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(margin + 22 * mm, content_y - sec_bar_h + 5, section['subtitle'])

    content_y -= sec_bar_h + 8 * mm

    # Render body items
    for item in section['body']:
        if content_y < bottom_limit:
            break
        content_y = render_item(c, item, margin, content_y, content_w, bottom_limit)


def is_big_font(title):
    if len(title) > 35:
        return 12
    return 14


def render_item(c, item, margin, y, content_w, bottom_limit):
    """Render a body item and return updated y position."""
    kind = item[0]
    data = item[1]

    if y < bottom_limit:
        return y

    if kind == 'para':
        h = _draw_wrapped_text(c, data, margin, y, content_w, 'Inter-Regular', 9.5, DGRAY, 13.5)
        return y - h - 5 * mm

    elif kind == 'heading3':
        if y - 14 * mm < bottom_limit:
            return y
        c.setFont('Inter-SemiBold', 11)
        c.setFillColor(NAVY)
        c.drawString(margin, y, data)
        # Cyan underline
        c.setFillColor(CYAN)
        c.rect(margin, y - 2, 18 * mm, 1.5, fill=1, stroke=0)
        return y - 11 * mm

    elif kind == 'bullet_pairs':
        for (head, body) in data:
            if y < bottom_limit + 10 * mm:
                break
            # Cyan dot
            c.setFillColor(CYAN)
            c.circle(margin + 3, y - 2, 2.5, fill=1, stroke=0)
            # Head
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            c.drawString(margin + 8 * mm, y, head)
            y -= 5.5 * mm
            # Body
            h = _draw_wrapped_text(c, body, margin + 8 * mm, y, content_w - 8 * mm, 'Inter-Regular', 9, DGRAY, 13)
            y -= h + 4 * mm
        return y

    elif kind == 'bullets':
        for bullet in data:
            if y < bottom_limit + 6 * mm:
                break
            c.setFillColor(CYAN)
            c.circle(margin + 3, y - 2, 2, fill=1, stroke=0)
            h = _draw_wrapped_text(c, bullet, margin + 7 * mm, y, content_w - 7 * mm, 'Inter-Regular', 9, DGRAY, 13)
            y -= h + 3.5 * mm
        return y

    elif kind == 'callout':
        if y - 20 * mm < bottom_limit:
            return y
        _draw_callout(c, data, margin, y, content_w)
        h = _callout_height(data, content_w)
        return y - h - 5 * mm

    elif kind == 'table':
        return draw_mini_table(c, data, margin, y, content_w, bottom_limit)

    elif kind == 'numbered_items':
        for (head, body) in data:
            if y < bottom_limit + 12 * mm:
                break
            # Number circle
            c.setFillColor(NAVY)
            c.circle(margin + 4 * mm, y - 2, 4 * mm, fill=1, stroke=0)
            c.setFont('Inter-Bold', 8)
            c.setFillColor(WHITE)
            step_num = head.split('—')[0].strip() if '—' in head else head[:2]
            c.drawCentredString(margin + 4 * mm, y - 4.5, step_num)
            # Heading
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            step_title = head.split('—')[1].strip() if '—' in head else head
            c.drawString(margin + 10 * mm, y, step_title)
            y -= 5.5 * mm
            h = _draw_wrapped_text(c, body, margin + 10 * mm, y, content_w - 10 * mm, 'Inter-Regular', 9, DGRAY, 13)
            y -= h + 4 * mm
        return y

    elif kind == 'pillar':
        (head, body) = data
        if y < bottom_limit + 14 * mm:
            return y
        # Left cyan bar
        pillar_h = _text_height(body, content_w - 12 * mm, 9, 13) + 12 * mm
        c.setFillColor(CYAN)
        c.rect(margin, y - pillar_h + 5 * mm, 3, pillar_h, fill=1, stroke=0)
        c.setFont('Inter-SemiBold', 10)
        c.setFillColor(NAVY)
        c.drawString(margin + 6 * mm, y, head)
        y -= 6 * mm
        h = _draw_wrapped_text(c, body, margin + 6 * mm, y, content_w - 6 * mm, 'Inter-Regular', 9, DGRAY, 13)
        return y - h - 5 * mm

    elif kind == 'two_col':
        col_w = (content_w - 5 * mm) / 2
        max_y = y
        for i, (head, body) in enumerate(data):
            col_x = margin + i * (col_w + 5 * mm)
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            c.drawString(col_x, y, head)
            c.setFillColor(CYAN)
            c.rect(col_x, y - 2, 15 * mm, 1, fill=1, stroke=0)
            body_y = y - 7 * mm
            h = _draw_wrapped_text(c, body, col_x, body_y, col_w, 'Inter-Regular', 9, DGRAY, 13)
            new_y = body_y - h
            max_y = min(max_y, new_y)
        return max_y - 5 * mm

    return y


def draw_mini_table(c, data, margin, y, content_w, bottom_limit):
    headers = data['headers']
    rows = data['rows']
    n_cols = len(headers)
    col_w = content_w / n_cols

    row_h = 7.5 * mm
    header_h = 8 * mm

    if y - (len(rows) + 1) * row_h - header_h < bottom_limit:
        # Truncate rows
        max_rows = max(3, int((y - bottom_limit - header_h) // row_h))
        rows = rows[:max_rows]

    # Header row
    c.setFillColor(NAVY)
    c.rect(margin, y - header_h, content_w, header_h, fill=1, stroke=0)
    for i, h in enumerate(headers):
        c.setFont('Inter-SemiBold', 8)
        c.setFillColor(WHITE)
        c.drawString(margin + i * col_w + 3 * mm, y - header_h + 2.5 * mm, h)

    y -= header_h

    for ridx, row in enumerate(rows):
        # Alt row bg
        if ridx % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(margin, y - row_h, content_w, row_h, fill=1, stroke=0)

        for cidx, cell in enumerate(row):
            c.setFont('Inter-Regular', 8)
            c.setFillColor(DGRAY)
            # Truncate cell text
            cell_str = str(cell)
            if len(cell_str) > 60:
                cell_str = cell_str[:57] + '...'
            c.drawString(margin + cidx * col_w + 3 * mm, y - row_h + 2.5 * mm, cell_str)

        y -= row_h

    # Bottom border
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(margin, y, margin + content_w, y)

    return y - 5 * mm


# ── Outro Page ────────────────────────────────────────────────────────────────

def draw_outro_landscape(c, page_w, page_h, page_num):
    W, H = page_w, page_h

    # Navy bg
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Decorative circle top right
    c.saveState()
    c.setFillColor(CYAN)
    c.setFillAlpha(0.07)
    c.circle(W, H, H * 0.75, fill=1, stroke=0)
    c.restoreState()

    # Cyan left strip
    c.setFillColor(CYAN)
    c.rect(0, 0, 6 * mm, H, fill=1, stroke=0)

    # Bottom bar
    c.setFillColor(HexColor('#021f42'))
    c.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    c.setFont('Inter-Regular', 7.5)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(22 * mm, 10 * mm, 'CDMA Services Ltd — May 2025 — Confidential')
    c.drawString(22 * mm, 4 * mm, 'cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 7.5)
    c.setFillColor(CYAN)
    c.drawRightString(W - 22 * mm, 7 * mm, f'Page {page_num}')

    # Main message
    center_y = H * 0.52
    c.setFont('Inter-Light', 14)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(22 * mm, center_y + 60, 'YOUR HOSPITALITY IT PARTNER')

    c.setFillColor(CYAN)
    c.rect(22 * mm, center_y + 55, 60 * mm, 1.5, fill=1, stroke=0)

    c.setFont('Inter-Black', 38)
    c.setFillColor(WHITE)
    c.drawString(22 * mm, center_y + 18, 'Always On.')

    c.setFont('Inter-Light', 38)
    c.setFillColor(CYAN)
    c.drawString(22 * mm, center_y - 18, 'Always Secure.')

    c.setFont('Inter-Bold', 11)
    c.setFillColor(WHITE)
    c.drawString(22 * mm, center_y - 42, 'Always With You.')

    # Contact block
    c.setFont('Inter-SemiBold', 9)
    c.setFillColor(HexColor('#A8BFDA'))
    c.drawString(22 * mm, center_y - 65, 'GET IN TOUCH')

    c.setFillColor(CYAN)
    c.rect(22 * mm, center_y - 68, 12 * mm, 1, fill=1, stroke=0)

    contacts = [
        ('Web', 'cdma.com.cy'),
        ('Email', 'sales@cdma.com.cy'),
        ('Phone', '+357 22 028014'),
        ('HQ', 'Nicosia, Cyprus'),
    ]
    cy = center_y - 80
    for label, value in contacts:
        c.setFont('Inter-Light', 9)
        c.setFillColor(HexColor('#8AAAC5'))
        c.drawString(22 * mm, cy, label + ':')
        c.setFont('Inter-Regular', 9)
        c.setFillColor(WHITE)
        c.drawString(38 * mm, cy, value)
        cy -= 8.5 * mm

    # ISO badge
    c.setFillColor(HexColor('#1a4070'))
    c.roundRect(W - 80 * mm, center_y - 40, 60 * mm, 70 * mm, 5, fill=1, stroke=0)
    c.setFont('Inter-Bold', 9)
    c.setFillColor(CYAN)
    c.drawCentredString(W - 50 * mm, center_y + 22, 'ISO 27001:2022')
    c.setFont('Inter-Light', 8)
    c.setFillColor(WHITE)
    c.drawCentredString(W - 50 * mm, center_y + 12, 'Certified')
    c.setFillColor(LGRAY)
    c.rect(W - 73 * mm, center_y + 6, 46 * mm, 0.5, fill=1, stroke=0)
    cert_items = ['56 Countries', '6 Continents', '24/7/365 NOC', 'White-Label']
    cy2 = center_y
    for ci in cert_items:
        c.setFillColor(CYAN)
        c.circle(W - 69 * mm, cy2 - 2, 2, fill=1, stroke=0)
        c.setFont('Inter-Regular', 8)
        c.setFillColor(WHITE)
        c.drawString(W - 65 * mm, cy2 - 4, ci)
        cy2 -= 8 * mm


def draw_outro_portrait(c, page_w, page_h, page_num):
    W, H = page_w, page_h

    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.saveState()
    c.setFillColor(CYAN)
    c.setFillAlpha(0.07)
    c.circle(W, H, H * 0.6, fill=1, stroke=0)
    c.restoreState()

    c.setFillColor(CYAN)
    c.rect(0, 0, 5 * mm, H, fill=1, stroke=0)

    # Bottom bar
    c.setFillColor(HexColor('#021f42'))
    c.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    c.setFont('Inter-Regular', 7)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(15 * mm, 10 * mm, 'CDMA Services Ltd  |  cdma.com.cy')
    c.drawString(15 * mm, 4 * mm, 'sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 7)
    c.setFillColor(CYAN)
    c.drawRightString(W - 15 * mm, 7 * mm, f'Page {page_num}')

    # Text
    center_x = W / 2
    cy = H * 0.58

    c.setFont('Inter-Light', 11)
    c.setFillColor(HexColor('#8AAAC5'))
    c.drawCentredString(center_x, cy + 55, 'YOUR HOSPITALITY IT PARTNER')

    c.setFillColor(CYAN)
    c.rect(center_x - 30 * mm, cy + 50, 60 * mm, 1.5, fill=1, stroke=0)

    c.setFont('Inter-Black', 32)
    c.setFillColor(WHITE)
    c.drawCentredString(center_x, cy + 20, 'Always On.')

    c.setFont('Inter-Light', 28)
    c.setFillColor(CYAN)
    c.drawCentredString(center_x, cy - 6, 'Always Secure.')

    c.setFont('Inter-Bold', 12)
    c.setFillColor(WHITE)
    c.drawCentredString(center_x, cy - 22, 'Always With You.')

    # Contact block
    c.setFont('Inter-SemiBold', 8)
    c.setFillColor(HexColor('#A8BFDA'))
    c.drawCentredString(center_x, cy - 40, 'GET IN TOUCH')
    c.setFillColor(CYAN)
    c.rect(center_x - 12 * mm, cy - 43, 24 * mm, 1, fill=1, stroke=0)

    contacts = [
        ('Web', 'cdma.com.cy'),
        ('Email', 'sales@cdma.com.cy'),
        ('Phone', '+357 22 028014'),
        ('HQ', 'Nicosia, Cyprus'),
    ]
    cy2 = cy - 54
    for label, value in contacts:
        c.setFont('Inter-Light', 8.5)
        c.setFillColor(HexColor('#8AAAC5'))
        c.drawCentredString(center_x - 12 * mm, cy2, label + ':')
        c.setFont('Inter-Regular', 8.5)
        c.setFillColor(WHITE)
        c.drawString(center_x - 5 * mm, cy2, value)
        cy2 -= 8 * mm

    # ISO badge
    badge_y = cy2 - 10 * mm
    c.setFillColor(HexColor('#1a4070'))
    c.roundRect(center_x - 30 * mm, badge_y - 30 * mm, 60 * mm, 35 * mm, 5, fill=1, stroke=0)
    c.setFont('Inter-Bold', 9)
    c.setFillColor(CYAN)
    c.drawCentredString(center_x, badge_y - 5 * mm, 'ISO 27001:2022  |  56 Countries')
    c.setFont('Inter-Light', 8)
    c.setFillColor(WHITE)
    c.drawCentredString(center_x, badge_y - 13 * mm, '24/7/365 NOC  |  White-Label Services')
    c.drawCentredString(center_x, badge_y - 21 * mm, 'Nicosia  ·  Dubai  ·  Athens')


# ── Text Utilities ────────────────────────────────────────────────────────────

def _draw_wrapped_text(c, text, x, y, max_w, font, size, color, line_h):
    """Draw wrapped text, return total height used."""
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines = []
    line = []
    for word in words:
        test = ' '.join(line + [word])
        if c.stringWidth(test, font, size) <= max_w:
            line.append(word)
        else:
            if line:
                lines.append(' '.join(line))
            line = [word]
    if line:
        lines.append(' '.join(line))

    for i, l in enumerate(lines):
        c.drawString(x, y - i * line_h, l)

    return len(lines) * line_h


def _text_height(text, max_w, size, line_h):
    """Estimate height of wrapped text block."""
    chars_per_line = max_w / (size * 0.52)
    words = text.split()
    lines = 0
    line_len = 0
    for word in words:
        if line_len + len(word) + 1 > chars_per_line:
            lines += 1
            line_len = len(word)
        else:
            line_len += len(word) + 1
    lines += 1
    return lines * line_h


def _draw_callout(c, text, x, y, max_w):
    """Draw a callout box with cyan left border."""
    box_h = _callout_height(text, max_w)
    # Light bg
    c.setFillColor(CYAN_SOFT)
    c.rect(x, y - box_h, max_w, box_h, fill=1, stroke=0)
    # Cyan left bar
    c.setFillColor(CYAN)
    c.rect(x, y - box_h, 3, box_h, fill=1, stroke=0)
    # Text
    _draw_wrapped_text(c, text, x + 6 * mm, y - 4 * mm, max_w - 8 * mm, 'Inter-Light', 9, NAVY, 13)


def _callout_height(text, max_w):
    return _text_height(text, max_w - 8 * mm, 9, 13) + 8 * mm


# ── Main Build ────────────────────────────────────────────────────────────────

def build_pdf(output_path, is_landscape=True):
    page_size = landscape(A4) if is_landscape else A4
    page_w, page_h = page_size

    c = canvas.Canvas(output_path, pagesize=page_size)
    c.setTitle('CDMA Hospitality Playbook')
    c.setAuthor('CDMA Services Ltd')
    c.setSubject('Managed IT & Cybersecurity for Hospitality')

    page_num = 1

    # 1. Cover
    if is_landscape:
        draw_cover_landscape(c, page_w, page_h)
    else:
        draw_cover_portrait(c, page_w, page_h)
    c.showPage()
    page_num += 1

    # 2. Introduction
    draw_intro(c, page_w, page_h, is_landscape, page_num)
    c.showPage()
    page_num += 1

    # 3. Table of Contents
    draw_toc(c, page_w, page_h, is_landscape, page_num)
    c.showPage()
    page_num += 1

    # 4–20. Sections
    for section in SECTIONS:
        draw_section(c, page_w, page_h, section, page_num)
        c.showPage()
        page_num += 1

    # Final. Outro
    if is_landscape:
        draw_outro_landscape(c, page_w, page_h, page_num)
    else:
        draw_outro_portrait(c, page_w, page_h, page_num)
    c.showPage()

    c.save()
    print(f"✅ Built: {output_path}")


if __name__ == '__main__':
    out_dir = '/Users/milton/clawd'
    build_pdf(f'{out_dir}/CDMA_Hospitality_Playbook_Landscape_v2.pdf', is_landscape=True)
    build_pdf(f'{out_dir}/CDMA_Hospitality_Playbook_Portrait_v2.pdf', is_landscape=False)
    print("🎉 Both PDFs generated successfully.")
