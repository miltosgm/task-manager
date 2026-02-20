#!/usr/bin/env python3
"""
CDMA Hospitality Playbook - Premium Redesign v3
Fixes: complete tables with wrapped text, multi-page overflow, improved TOC
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Brand Colors ───────────────────────────────────────────────────────────────
NAVY      = HexColor('#053a75')
CYAN      = HexColor('#00e1fc')
LIGHT     = HexColor('#F0F3F5')
WHITE     = white
GRAY      = HexColor('#8A9AB0')
DGRAY     = HexColor('#2D3748')
LGRAY     = HexColor('#CBD5E0')
NAVY2     = HexColor('#0A4D9E')
CYAN_SOFT = HexColor('#E0FAFE')
DARK_BG   = HexColor('#021f42')
MID_NAVY  = HexColor('#1a4070')

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

register_fonts()

# ── Text Utilities ─────────────────────────────────────────────────────────────

def wrap_text(c, text, font, size, max_w):
    """Wrap text to fit max_w. Returns list of line strings."""
    words = str(text).split()
    lines, line = [], []
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
    return lines or ['']

def draw_wrapped(c, text, x, y, max_w, font, size, color, line_h):
    """Draw wrapped text block. Returns height consumed."""
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap_text(c, text, font, size, max_w)
    for i, l in enumerate(lines):
        c.drawString(x, y - i * line_h, l)
    return len(lines) * line_h

def text_height_estimate(text, max_w, font, size, line_h):
    """Estimate wrapped text height without a canvas."""
    chars_per_line = max(1, max_w / (size * 0.52))
    words = str(text).split()
    lines, line_len = 1, 0
    for word in words:
        if line_len + len(word) + 1 > chars_per_line:
            lines += 1
            line_len = len(word)
        else:
            line_len += len(word) + 1
    return lines * line_h


# ── Page Builder Class ─────────────────────────────────────────────────────────

class PageBuilder:
    """Manages page lifecycle: header/footer, y tracking, new-page logic."""

    def __init__(self, c, page_w, page_h, is_landscape):
        self.c = c
        self.page_w = page_w
        self.page_h = page_h
        self.is_landscape = is_landscape
        self.margin = 15 * mm
        self.header_h = 10 * mm
        self.footer_h = 14 * mm
        self.page_num = 1
        self.content_bottom = self.footer_h + 6 * mm
        self.content_w = page_w - 2 * self.margin

    def content_top(self):
        return self.page_h - self.header_h - 8 * mm

    def start_interior_page(self, title='CDMA HOSPITALITY PLAYBOOK'):
        draw_interior_header(self.c, self.page_w, self.page_h, title)
        draw_footer(self.c, self.page_w, self.page_h, self.page_num)
        return self.content_top()

    def new_page(self, title='CDMA HOSPITALITY PLAYBOOK'):
        self.c.showPage()
        self.page_num += 1
        return self.start_interior_page(title)

    def ensure_space(self, y, needed, title='CDMA HOSPITALITY PLAYBOOK'):
        """If not enough vertical space, start a new page. Returns new y."""
        if y - needed < self.content_bottom:
            return self.new_page(title)
        return y


# ── Shared Drawing Helpers ─────────────────────────────────────────────────────

def draw_interior_header(c, page_w, page_h, doc_title='CDMA HOSPITALITY PLAYBOOK'):
    bar_h = 10 * mm
    c.setFillColor(NAVY)
    c.rect(0, page_h - bar_h, page_w, bar_h, fill=1, stroke=0)
    c.setFont('Inter-SemiBold', 8)
    c.setFillColor(WHITE)
    c.drawString(15 * mm, page_h - bar_h + 3.2 * mm, doc_title)
    c.setFillColor(CYAN)
    c.setFont('Inter-Regular', 7)
    c.drawRightString(page_w - 15 * mm, page_h - bar_h + 3.2 * mm, 'cdma.com.cy  |  +357 22 028014')

def draw_footer(c, page_w, page_h, page_num):
    footer_y = 8 * mm
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(15 * mm, footer_y + 4 * mm, page_w - 15 * mm, footer_y + 4 * mm)
    c.setFont('Inter-Regular', 7)
    c.setFillColor(GRAY)
    c.drawString(15 * mm, footer_y, 'CDMA Services Ltd  |  cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 7)
    c.setFillColor(NAVY)
    c.drawRightString(page_w - 15 * mm, footer_y, f'Page {page_num}')


# ── Table Renderer (multi-page safe) ──────────────────────────────────────────

def draw_table(pb, headers, rows, y, col_widths=None):
    """
    Draw a table. Handles wrapped cell text and multi-page overflow.
    pb: PageBuilder
    headers: list of str
    rows: list of tuples
    y: current y position
    col_widths: optional list of relative widths (must sum ~= 1.0)
    Returns updated y.
    """
    c = pb.c
    margin = pb.margin
    content_w = pb.content_w
    n_cols = len(headers)

    # Build column widths
    if col_widths:
        cols = [content_w * w for w in col_widths]
    else:
        cols = [content_w / n_cols] * n_cols

    HEADER_FONT = 'Inter-SemiBold'
    HEADER_SIZE = 8
    CELL_FONT   = 'Inter-Regular'
    CELL_SIZE   = 8
    LINE_H      = 11
    PAD_X       = 3 * mm
    PAD_Y_TOP   = 3 * mm
    PAD_Y_BOT   = 2.5 * mm

    # Pre-compute row heights
    def row_height(row_cells, font, size):
        max_h = 0
        for i, cell in enumerate(row_cells):
            cell_w = cols[i] - 2 * PAD_X
            h = text_height_estimate(str(cell), cell_w, font, size, LINE_H)
            if h > max_h:
                max_h = h
        return max_h + PAD_Y_TOP + PAD_Y_BOT

    header_h = row_height(headers, HEADER_FONT, HEADER_SIZE)

    # Draw header — ensure it fits
    y = pb.ensure_space(y, header_h + 15, 'CDMA HOSPITALITY PLAYBOOK')

    # Header row
    c.setFillColor(NAVY)
    c.rect(margin, y - header_h, content_w, header_h, fill=1, stroke=0)
    x_cursor = margin
    for i, h in enumerate(headers):
        lines = wrap_text(c, h, HEADER_FONT, HEADER_SIZE, cols[i] - 2 * PAD_X)
        c.setFont(HEADER_FONT, HEADER_SIZE)
        c.setFillColor(WHITE)
        for li, line in enumerate(lines):
            c.drawString(x_cursor + PAD_X, y - PAD_Y_TOP - li * LINE_H, line)
        x_cursor += cols[i]
    y -= header_h

    # Data rows
    for ridx, row in enumerate(rows):
        rh = row_height(row, CELL_FONT, CELL_SIZE)

        # Check space; if not enough, new page and redraw mini-header
        if y - rh < pb.content_bottom:
            y = pb.new_page()
            # Continued header
            c.setFillColor(MID_NAVY)
            c.rect(margin, y - header_h, content_w, header_h, fill=1, stroke=0)
            x_cursor = margin
            c.setFont(HEADER_FONT, HEADER_SIZE)
            c.setFillColor(WHITE)
            for i, h in enumerate(headers):
                lines = wrap_text(c, h, HEADER_FONT, HEADER_SIZE, cols[i] - 2 * PAD_X)
                for li, line in enumerate(lines):
                    c.drawString(x_cursor + PAD_X, y - PAD_Y_TOP - li * LINE_H, line)
                x_cursor += cols[i]
            y -= header_h

        # Alternating bg
        if ridx % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(margin, y - rh, content_w, rh, fill=1, stroke=0)

        # Cell text
        x_cursor = margin
        for cidx, cell in enumerate(row):
            cell_w = cols[cidx] - 2 * PAD_X
            lines = wrap_text(c, str(cell), CELL_FONT, CELL_SIZE, cell_w)
            c.setFont(CELL_FONT, CELL_SIZE)
            c.setFillColor(DGRAY)
            for li, line in enumerate(lines):
                c.drawString(x_cursor + PAD_X, y - PAD_Y_TOP - li * LINE_H, line)
            x_cursor += cols[cidx]

        # Light row border
        c.setStrokeColor(LGRAY)
        c.setLineWidth(0.3)
        c.line(margin, y - rh, margin + content_w, y - rh)
        y -= rh

    # Bottom border
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.5)
    c.line(margin, y, margin + content_w, y)
    return y - 5 * mm


# ── Section Content Renderer ───────────────────────────────────────────────────

def render_section_content(pb, section):
    """Render all body items for a section, handling page breaks."""
    c = pb.c
    margin = pb.margin
    content_w = pb.content_w
    bottom = pb.content_bottom
    title_tag = f"Section {section['num']} — CDMA HOSPITALITY PLAYBOOK"

    # Section header bar (navy, full-width)
    y = pb.content_top()
    sec_bar_h = 18 * mm
    c.setFillColor(NAVY)
    c.rect(0, y - sec_bar_h, pb.page_w, sec_bar_h, fill=1, stroke=0)
    # Section number
    c.setFont('Inter-Black', 28)
    c.setFillColor(CYAN)
    c.drawString(margin, y - sec_bar_h + 5, section['num'])
    # Title (auto-size)
    tlen = len(section['title'])
    tfont = 11 if tlen > 40 else (13 if tlen > 30 else 15)
    c.setFont('Inter-Bold', tfont)
    c.setFillColor(WHITE)
    # Wrap title if needed
    title_lines = wrap_text(c, section['title'], 'Inter-Bold', tfont,
                            pb.page_w - margin - 25 * mm)
    for li, tl in enumerate(title_lines):
        c.drawString(margin + 22 * mm, y - 5 - li * (tfont + 2), tl)
    # Subtitle
    c.setFont('Inter-Light', 8)
    c.setFillColor(HexColor('#8AAAC5'))
    sub_y = y - sec_bar_h + 4
    c.drawString(margin + 22 * mm, sub_y, section['subtitle'][:90])

    y -= sec_bar_h + 8 * mm

    for item in section['body']:
        kind = item[0]
        data = item[1]
        y = render_item(pb, kind, data, y, title_tag)

    return y


def render_item(pb, kind, data, y, page_title):
    c = pb.c
    margin = pb.margin
    content_w = pb.content_w
    bottom = pb.content_bottom
    LINE_H = 13.5

    def ensure(needed):
        nonlocal y
        y = pb.ensure_space(y, needed, page_title)
        return y

    if kind == 'para':
        ensure(20)
        h = draw_wrapped(c, data, margin, y, content_w,
                         'Inter-Regular', 9.5, DGRAY, LINE_H)
        y -= h + 5 * mm
        return y

    elif kind == 'heading3':
        ensure(16)
        c.setFont('Inter-SemiBold', 11)
        c.setFillColor(NAVY)
        c.drawString(margin, y, data)
        c.setFillColor(CYAN)
        c.rect(margin, y - 2, 18 * mm, 1.5, fill=1, stroke=0)
        y -= 11 * mm
        return y

    elif kind == 'bullets':
        for bullet in data:
            bh = text_height_estimate(bullet, content_w - 7 * mm, 'Inter-Regular', 9, 13)
            ensure(bh + 4)
            c.setFillColor(CYAN)
            c.circle(margin + 3, y - 2, 2, fill=1, stroke=0)
            draw_wrapped(c, bullet, margin + 7 * mm, y, content_w - 7 * mm,
                         'Inter-Regular', 9, DGRAY, 13)
            y -= bh + 3.5 * mm
        return y

    elif kind == 'bullet_pairs':
        for head, body in data:
            bh = text_height_estimate(body, content_w - 8 * mm, 'Inter-Regular', 9, 13)
            needed = bh + 5.5 * mm + 4 * mm
            ensure(needed)
            c.setFillColor(CYAN)
            c.circle(margin + 3, y - 2, 2.5, fill=1, stroke=0)
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            c.drawString(margin + 8 * mm, y, head)
            y -= 5.5 * mm
            h = draw_wrapped(c, body, margin + 8 * mm, y, content_w - 8 * mm,
                              'Inter-Regular', 9, DGRAY, 13)
            y -= h + 4 * mm
        return y

    elif kind == 'callout':
        ch = text_height_estimate(data, content_w - 8 * mm, 'Inter-Light', 9, 13) + 8 * mm
        ensure(ch + 4)
        c.setFillColor(CYAN_SOFT)
        c.rect(margin, y - ch, content_w, ch, fill=1, stroke=0)
        c.setFillColor(CYAN)
        c.rect(margin, y - ch, 3, ch, fill=1, stroke=0)
        draw_wrapped(c, data, margin + 6 * mm, y - 4 * mm, content_w - 8 * mm,
                     'Inter-Light', 9, NAVY, 13)
        y -= ch + 5 * mm
        return y

    elif kind == 'table':
        headers = data['headers']
        rows    = data['rows']
        col_widths = data.get('col_widths', None)
        y = draw_table(pb, headers, rows, y, col_widths)
        return y

    elif kind == 'numbered_items':
        for step_head, body in data:
            bh = text_height_estimate(body, content_w - 10 * mm, 'Inter-Regular', 9, 13)
            needed = bh + 5.5 * mm + 4 * mm
            ensure(needed)
            c.setFillColor(NAVY)
            c.circle(margin + 4 * mm, y - 2, 4 * mm, fill=1, stroke=0)
            c.setFont('Inter-Bold', 8)
            c.setFillColor(WHITE)
            step_num = step_head.split('—')[0].strip() if '—' in step_head else step_head[:3]
            c.drawCentredString(margin + 4 * mm, y - 4.5, step_num)
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            step_title = step_head.split('—')[1].strip() if '—' in step_head else step_head
            c.drawString(margin + 10 * mm, y, step_title)
            y -= 5.5 * mm
            h = draw_wrapped(c, body, margin + 10 * mm, y, content_w - 10 * mm,
                              'Inter-Regular', 9, DGRAY, 13)
            y -= h + 4 * mm
        return y

    elif kind == 'pillar':
        head, body = data
        bh = text_height_estimate(body, content_w - 6 * mm, 'Inter-Regular', 9, 13)
        needed = bh + 6 * mm + 5 * mm
        ensure(needed)
        pillar_h = bh + 6 * mm
        c.setFillColor(CYAN)
        c.rect(margin, y - pillar_h + 5 * mm, 3, pillar_h, fill=1, stroke=0)
        c.setFont('Inter-SemiBold', 10)
        c.setFillColor(NAVY)
        c.drawString(margin + 6 * mm, y, head)
        y -= 6 * mm
        h = draw_wrapped(c, body, margin + 6 * mm, y, content_w - 6 * mm,
                         'Inter-Regular', 9, DGRAY, 13)
        y -= h + 5 * mm
        return y

    elif kind == 'two_col':
        col_w = (content_w - 5 * mm) / 2
        # measure max height
        max_needed = 0
        for head, body in data:
            bh = text_height_estimate(body, col_w, 'Inter-Regular', 9, 13)
            max_needed = max(max_needed, bh + 7 * mm + 2)
        ensure(max_needed + 4)
        for i, (head, body) in enumerate(data):
            col_x = margin + i * (col_w + 5 * mm)
            c.setFont('Inter-SemiBold', 9.5)
            c.setFillColor(NAVY)
            c.drawString(col_x, y, head)
            c.setFillColor(CYAN)
            c.rect(col_x, y - 2, 15 * mm, 1, fill=1, stroke=0)
            draw_wrapped(c, body, col_x, y - 7 * mm, col_w,
                         'Inter-Regular', 9, DGRAY, 13)
        y -= max_needed + 5 * mm
        return y

    return y


# ── Section Content Data ───────────────────────────────────────────────────────

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
                'col_widths': [0.28, 0.30, 0.42],
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
                'col_widths': [0.22, 0.40, 0.38],
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
                'col_widths': [0.28, 0.72],
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
                'col_widths': [0.18, 0.22, 0.22, 0.38],
                'rows': [
                    ('Essential', '24/7 monitoring', 'Alerts within 15 min', 'Core infrastructure monitoring and alerting'),
                    ('Standard', '24/7 monitoring + remediation', 'Incident response within 30 minutes', 'Monitoring, remediation, monthly reports'),
                    ('Premium', '24/7 monitoring + remediation + proactive management', 'Priority within 15 minutes', 'Full proactive management, quarterly reviews, dedicated engineer'),
                ]
            }),
            ('heading3', 'Certifications & Tooling'),
            ('bullets', [
                'ISO 27001:2022 certified — information security management across all service delivery',
                'Compatible with all leading RMM platforms: ConnectWise, Datto, NinjaRMM, Atera',
                'ITSM ticketing fully integrated for SLA tracking and reporting',
                'Dedicated hospitality playbooks for PMS/POS maintenance windows',
            ]),
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
            ('heading3', 'Service Desk Performance Metrics'),
            ('table', {
                'headers': ['Metric', 'Target (Standard)', 'Target (Premium)'],
                'col_widths': [0.40, 0.30, 0.30],
                'rows': [
                    ('First Contact Resolution Rate', '> 70%', '> 80%'),
                    ('P1 Acknowledgement', 'Within 15 minutes', 'Within 5 minutes'),
                    ('P2 Response', 'Within 1 hour', 'Within 30 minutes'),
                    ('P3 Resolution', 'Within 4 hours', 'Within 2 hours'),
                    ('Customer Satisfaction (CSAT)', '> 90%', '> 95%'),
                    ('Monthly Reporting', 'Standard summary', 'Executive dashboard'),
                ]
            }),
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
            ('heading3', 'Wi-Fi Infrastructure Summary'),
            ('table', {
                'headers': ['Component', 'Specification', 'Benefit'],
                'col_widths': [0.25, 0.35, 0.40],
                'rows': [
                    ('Access Points', 'Wi-Fi 6/6E (802.11ax/be), MU-MIMO, OFDMA', 'More devices, faster speeds, less interference'),
                    ('Controllers', 'Cloud or on-prem (Aruba, Cisco, Meraki, Ubiquiti)', 'Centralised management, remote troubleshooting'),
                    ('Roaming', '802.11r/k/v fast BSS transition', 'Seamless handoffs across APs during movement'),
                    ('QoS', 'Per-SSID bandwidth policies, application prioritisation', 'PMS/VoIP prioritised over guest streaming'),
                    ('Monitoring', '24/7 NOC visibility, uptime alerts, client analytics', 'Proactive issue detection before guests complain'),
                    ('Security', 'WPA3, network isolation, client firewalling', 'Guest devices cannot reach staff or PMS VLANs'),
                ]
            }),
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
                'headers': ['System', 'Coverage', 'Key Risk if Down'],
                'col_widths': [0.28, 0.30, 0.42],
                'rows': [
                    ('PMS (Opera, Mews, Protel)', '24/7 uptime monitoring, connectivity assurance, application health', 'Front desk paralysis, check-in failures, revenue loss'),
                    ('POS (Micros, Lightspeed)', 'Transaction monitoring, failover support, periodic health checks', 'Revenue loss, guest frustration at F&B outlets, end-of-day reconciliation failure'),
                    ('IPTV (Samsung LYNK, LG Pro)', 'Channel availability monitoring, controller restarts, stream health', 'Guest experience degradation, complaint volumes increase'),
                    ('Digital Signage', 'Content delivery monitoring, display uptime, scheduling accuracy', 'Brand and information gaps in lobbies and conference spaces'),
                    ('Teams Phone / VoIP', 'Call quality monitoring, extension availability, trunk status', 'Missed reservations, reception downtime, emergency communication failure'),
                    ('Conference AV', 'Pre-event systems testing, live monitoring during events', 'Event failures affecting revenue and reputation'),
                    ('Digital Key Systems', 'API integration health monitoring, lock response times', 'Guest lockouts, security incidents, brand damage'),
                    ('Booking Engines & OTAs', 'Channel manager sync monitoring, rate/availability push health', 'Overbookings, rate parity issues, missed revenue'),
                ]
            }),
            ('heading3', 'Maintenance Windows'),
            ('para', "All scheduled maintenance activities are performed during low-occupancy periods specific to each property. CDMA works with each property to define optimal maintenance windows that minimise guest impact while ensuring systems remain current and secure."),
            ('callout', 'Critical rule: PMS and POS systems are never patched or restarted during check-in/check-out peaks or active F&B service hours. Our hospitality-aware maintenance schedules respect operational realities.'),
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
                ('01 — Prevent', 'Next-generation firewall with application awareness and web filtering. Network micro-segmentation ensuring PCI-scoped POS systems are isolated. Endpoint protection on all managed devices. Vulnerability scanning and patch management to close known attack vectors before they are exploited.'),
                ('02 — Detect', '24/7 SIEM monitoring with correlation rules tuned for hospitality environments. Anomaly detection identifying unusual traffic patterns. User behaviour analytics to spot compromised credentials. Threat intelligence feeds updated in real time from global sources.'),
                ('03 — Respond', 'Managed Detection and Response (MDR) with 15-minute threat isolation SLA. Documented incident response playbooks specific to hospitality. Forensic capability for post-incident investigation. Post-incident reporting with root cause analysis and remediation recommendations.'),
            ]),
            ('heading3', 'Compliance Alignment'),
            ('bullet_pairs', [
                ('PCI DSS', 'Cardholder data environment scoping, network segmentation validation, quarterly vulnerability scanning, and penetration testing coordination. We help you define, document, and maintain your PCI scope.'),
                ('GDPR', 'Guest personal data handling guidance, breach notification procedures, data processor agreement templates, and privacy impact assessment support for new technology deployments.'),
                ('ISO 27001:2022', 'CDMA operates under ISO 27001:2022 certification, ensuring information security management best practices are applied across all service delivery activities.'),
                ('NIS2 / DORA', 'Advisory support for hospitality properties and management groups falling under NIS2 obligations or with financial services linkage requiring DORA compliance.'),
            ]),
            ('heading3', 'Cybersecurity Services Summary'),
            ('table', {
                'headers': ['Service', 'Description', 'Coverage'],
                'col_widths': [0.25, 0.45, 0.30],
                'rows': [
                    ('Next-Gen Firewall', 'Application-aware, IPS, web filtering, SSL inspection', '24/7 active'),
                    ('EDR / Endpoint Protection', 'AI-based threat detection, behavioural analysis, rollback', 'All managed endpoints'),
                    ('SIEM & Log Management', 'Centralised event correlation, threat hunting, alerting', '24/7 monitoring'),
                    ('MDR / SOC', 'Human-led threat investigation, 15-min isolation SLA', '24/7 response'),
                    ('Vulnerability Management', 'Authenticated scanning, risk scoring, remediation tracking', 'Monthly + on-demand'),
                    ('Penetration Testing', 'External, internal, and Wi-Fi penetration testing', 'Annual or as required'),
                    ('Phishing Simulation', 'Staff awareness campaigns, click-rate reporting', 'Quarterly campaigns'),
                    ('Incident Response', 'Forensic investigation, containment, recovery', 'On-demand + retainer'),
                ]
            }),
        ]
    },
    {
        'num': '09',
        'title': 'Mobile DAS Solutions',
        'subtitle': 'Nextivity-powered 4G/5G coverage, eliminating dead zones throughout property',
        'body': [
            ('para', "Mobile signal dead zones frustrate guests and impede staff communications. CDMA deploys Distributed Antenna Systems (DAS) powered by Nextivity technology to deliver consistent 4G/5G coverage throughout even the most challenging property layouts."),
            ('heading3', 'The Challenge'),
            ('para', "Thick concrete walls, underground car parks, basement conference rooms, and large atrium spaces all create cellular dead zones. Guests complain. Staff cannot receive calls or use mobile applications. Emergency communications may be compromised in areas where signal is weak or absent."),
            ('heading3', "CDMA's Nextivity DAS Solution"),
            ('bullet_pairs', [
                ('Carrier-Agnostic Coverage', 'Nextivity systems amplify all major carrier signals simultaneously — guests on any network receive improved coverage without carrier partnerships or site licensing complexity.'),
                ('Passive & Active DAS', 'We design and install both passive distributed antenna systems for smaller properties and active DAS for large resort complexes or multi-storey hotels.'),
                ('4G & 5G Ready', 'Future-proof infrastructure supporting both 4G LTE and 5G NR frequencies, ensuring your investment remains relevant as networks evolve.'),
                ('Professional Survey & Design', 'Site RF surveys identify coverage gaps precisely. System design ensures every area — including pool decks, spa, and underground parking — receives adequate signal.'),
                ('Monitoring & Maintenance', 'CDMA remotely monitors DAS performance and proactively addresses signal degradation before guests experience issues.'),
            ]),
            ('heading3', 'DAS Deployment Summary'),
            ('table', {
                'headers': ['Area Type', 'DAS Type', 'Typical Coverage Outcome'],
                'col_widths': [0.30, 0.25, 0.45],
                'rows': [
                    ('Guest Rooms (multi-storey)', 'Passive DAS or active per-floor', '-65 to -75 dBm signal strength throughout'),
                    ('Conference & Banquet Halls', 'Active DAS with distributed antennas', 'Full carrier coverage across all seating areas'),
                    ('Underground Car Parks', 'Passive leaky feeder or active', 'Consistent voice and data coverage at -70 dBm'),
                    ('Spa, Pool, Outdoor Areas', 'External antennas + internal passive', 'Coverage extended to all guest amenity areas'),
                    ('Restaurant & Bar Areas', 'Integrated with building DAS', 'Strong signal for POS, staff devices, and guests'),
                    ('Back-of-House / Kitchens', 'Passive extension from main DAS', 'Staff communications uninterrupted'),
                ]
            }),
        ]
    },
    {
        'num': '10',
        'title': 'Backup & Disaster Recovery',
        'subtitle': '15-min RPO, immutable backups, documented DR runbooks, tested recovery',
        'body': [
            ('para', "A ransomware attack, hardware failure, or natural disaster can bring hospitality operations to a standstill. CDMA's backup and disaster recovery services ensure rapid recovery with documented, tested runbooks — not last-minute improvisation."),
            ('heading3', 'Key Recovery Metrics'),
            ('table', {
                'headers': ['Metric', 'CDMA Standard', 'Why It Matters for Hospitality'],
                'col_widths': [0.28, 0.22, 0.50],
                'rows': [
                    ('Recovery Point Objective (RPO)', '15 minutes', 'Maximum data loss window — only 15 minutes of transactions at risk'),
                    ('Recovery Time Objective (RTO)', 'Defined per system tier', 'PMS and POS are prioritised first for restoration'),
                    ('Backup Frequency', 'Continuous to hourly depending on criticality', 'Critical systems backed up continuously; others on defined schedules'),
                    ('Retention Period', 'Configurable — typically 30/90/365 days', 'Meets regulatory requirements for financial and guest data'),
                    ('Offsite Replication', 'Encrypted offsite copy always maintained', 'Site disaster cannot destroy primary and backup simultaneously'),
                    ('Immutability', 'Write-once backup repositories', 'Ransomware cannot encrypt or delete backup data'),
                    ('Encryption', 'AES-256 at rest and in transit', 'Backup data protected against interception and theft'),
                ]
            }),
            ('heading3', 'DR Runbooks'),
            ('para', "Every managed property has a documented disaster recovery runbook specific to its technology stack. Runbooks cover the following scenarios: ransomware attack, critical hardware failure, ISP outage, site-level disaster (fire, flood), and cloud platform outage."),
            ('para', "Runbooks are tested at least annually (more frequently for Premium tier clients). Each test produces a formal report with recovery time measurements, gaps identified, and remediation actions assigned."),
            ('heading3', 'Backup Coverage by System'),
            ('table', {
                'headers': ['System', 'Backup Method', 'RPO', 'Recovery Priority'],
                'col_widths': [0.25, 0.30, 0.15, 0.30],
                'rows': [
                    ('PMS Server', 'Continuous replication + hourly snapshot', '15 min', 'Priority 1 — restore first'),
                    ('POS Systems', 'Hourly image backup + transaction log', '1 hour', 'Priority 1 — restore first'),
                    ('File & Document Servers', 'Daily full + hourly incremental', '1 hour', 'Priority 2'),
                    ('Email & Collaboration', 'Cloud-native backup (M365 third-party)', '24 hours', 'Priority 2'),
                    ('CCTV Footage', 'Local NVR + 30-day cloud retention', 'Real-time', 'Priority 3'),
                    ('Network Configuration', 'Daily automated config backup', '24 hours', 'Priority 2'),
                    ('Security Logs / SIEM', 'Immutable log archive, 12 months minimum', 'Real-time', 'Priority 3 (compliance)'),
                ]
            }),
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
                'PMS/POS integration health and dependency mapping',
                'Wi-Fi infrastructure survey and coverage gap assessment',
            ]),
            ('heading3', 'Deliverables'),
            ('table', {
                'headers': ['Deliverable', 'Audience', 'Contents'],
                'col_widths': [0.28, 0.20, 0.52],
                'rows': [
                    ('Executive Summary Report', 'Senior Management', 'Business-language overview of findings, risks, and recommended priorities'),
                    ('Technical Detail Report', 'IT Team', 'Configuration-level findings, remediation steps, and implementation priorities'),
                    ('Remediation Roadmap', 'IT + Management', 'Prioritised action plan with timelines, resource requirements, and risk ratings'),
                    ('Baseline Documentation', 'IT Team + NOC', 'Network diagrams, asset inventory, and configuration snapshots for ongoing reference'),
                    ('Alert Tuning Report', 'NOC / MSP', 'Recommended alert thresholds, suppression rules, and escalation paths'),
                ]
            }),
            ('heading3', 'Assessment Timeline'),
            ('numbered_items', [
                ('01 — Kick-off', 'Introductory call to align on scope, access requirements, and timeline. Credential and access collection initiated.'),
                ('02 — Remote Discovery', 'Automated tooling gathers asset inventory, patch status, alert history, and network configuration data.'),
                ('03 — On-Site Visit', 'Physical inspection of server rooms, network closets, Wi-Fi coverage, and critical infrastructure.'),
                ('04 — Analysis', 'CDMA engineers analyse all collected data against hospitality best-practice benchmarks.'),
                ('05 — Reporting', 'Full report suite delivered. Findings presented in debrief meeting with stakeholders.'),
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
                ('PMS/POS Migrations', 'Coordination with PMS and POS vendors for platform migrations. Network preparation, testing, and cutover support with rollback procedures.'),
            ]),
            ('heading3', 'Project Delivery Standards'),
            ('table', {
                'headers': ['Phase', 'Activities', 'Output'],
                'col_widths': [0.18, 0.47, 0.35],
                'rows': [
                    ('Discovery', 'Requirements gathering, site survey, vendor liaison, existing infrastructure review', 'Scope document, project plan, risk register'),
                    ('Design', 'Network design, equipment specification, vendor selection, budget finalisation', 'Design document, bill of materials, configuration templates'),
                    ('Build', 'Equipment procurement, staging and configuration, pre-deployment testing', 'Configured and tested equipment, cutover plan'),
                    ('Deploy', 'On-site installation, system integration, staff training, go-live support', 'Live system, handover documentation, as-built diagrams'),
                    ('Handover', 'Documentation package, NOC integration, post-project review', 'Full documentation, monitoring configured, lessons learned'),
                ]
            }),
        ]
    },
    {
        'num': '13',
        'title': 'Onboarding Process',
        'subtitle': 'Nine-step structured onboarding for single sites and multi-property groups',
        'body': [
            ('para', "CDMA's structured onboarding process ensures smooth transitions from existing providers or from unmanaged environments. Every engagement follows a documented nine-step process adapted for single properties and multi-site groups."),
            ('numbered_items', [
                ('01 — Discovery & Scoping', 'Initial discovery call to understand the property, existing infrastructure, current pain points, and service requirements. Contract and commercial terms agreed.'),
                ('02 — Technical Discovery', 'Remote and on-site technical assessment of existing infrastructure. Network diagrams, asset inventories, and credential collection.'),
                ('03 — Platform Integration', 'Integration of property systems into CDMA NOC and Service Desk platforms. RMM agent deployment, monitoring configuration.'),
                ('04 — Baseline & Tuning', 'Alert threshold establishment, maintenance window configuration, escalation path definition. First week of monitoring with active tuning.'),
                ('05 — Security Hardening', 'Firewall rule review, network segmentation validation, endpoint protection deployment, backup configuration verification.'),
                ('06 — Service Desk Activation', 'Staff communication about new service desk contact details, ticketing procedures, and escalation paths. White-label configuration complete.'),
                ('07 — Knowledge Transfer', 'Documentation of property-specific procedures, vendor contacts, and escalation preferences for NOC and Service Desk teams.'),
                ('08 — Go-Live', 'Full service commencement. Dedicated contact point for first 30 days to address any service delivery adjustments.'),
                ('09 — 30-Day Review', 'Service delivery review meeting. Alert volume analysis, ticket trends, and service optimisation recommendations.'),
            ]),
            ('heading3', 'Onboarding Timeline by Property Type'),
            ('table', {
                'headers': ['Property Type', 'Typical Onboarding Duration', 'Key Complexity Factors'],
                'col_widths': [0.28, 0.22, 0.50],
                'rows': [
                    ('Single boutique hotel (< 50 rooms)', '2–3 weeks', 'Limited existing documentation; often unmanaged infrastructure'),
                    ('Mid-scale hotel (50–200 rooms)', '3–4 weeks', 'Multiple vendor systems; PMS integration complexity'),
                    ('Large resort (200+ rooms)', '4–6 weeks', 'High device count; multi-building network; complex VLAN design'),
                    ('Multi-property group (2–5 sites)', '6–10 weeks', 'Standardisation across sites; phased rollout; group-level reporting'),
                    ('Multi-property group (5+ sites)', '10–16 weeks', 'Full standardisation programme; dedicated project management required'),
                ]
            }),
        ]
    },
    {
        'num': '14',
        'title': 'Service Level Agreement (SLA)',
        'subtitle': 'Essential / Standard / Premium tiers with defined response times',
        'body': [
            ('para', "CDMA's tiered SLA structure provides flexibility for properties with different requirements and budgets while maintaining clear, contractual performance commitments."),
            ('table', {
                'headers': ['SLA Metric', 'Essential', 'Standard', 'Premium'],
                'col_widths': [0.30, 0.23, 0.23, 0.24],
                'rows': [
                    ('Monitoring Hours', '24/7', '24/7', '24/7'),
                    ('P1 Response Time', '30 minutes', '15 minutes', '5 minutes'),
                    ('P2 Response Time', '2 hours', '1 hour', '30 minutes'),
                    ('P3 Response Time', 'Next business day', '4 hours', '2 hours'),
                    ('Service Desk Coverage', 'Business hours', '24/7', '24/7 dedicated queue'),
                    ('Monthly Reporting', 'Standard summary', 'Detailed report', 'Executive summary + KPI dashboard'),
                    ('Quarterly Business Review', 'Not included', 'Included', 'Included + dedicated engineer'),
                    ('Pre-Peak Readiness Check', 'Not included', 'Not included', 'Included annually'),
                    ('Dedicated Account Manager', 'Not included', 'Shared', 'Dedicated'),
                    ('Proactive Maintenance', 'Reactive only', 'Scheduled maintenance', 'Proactive + predictive'),
                ]
            }),
            ('heading3', 'Priority Definitions'),
            ('table', {
                'headers': ['Priority', 'Definition', 'Examples'],
                'col_widths': [0.15, 0.35, 0.50],
                'rows': [
                    ('P1 — Critical', 'Complete service outage affecting guest-facing systems or active security incident', 'PMS down, guest Wi-Fi offline property-wide, POS failure, ransomware detected'),
                    ('P2 — High', 'Significant degradation of key systems or partial connectivity loss', 'Slow PMS, intermittent Wi-Fi, VoIP quality issues, single-building connectivity loss'),
                    ('P3 — Medium', 'Single-user or non-critical system issues or service requests', 'Individual device problem, new user setup, software update request'),
                    ('P4 — Low', 'Enhancement requests, scheduled maintenance, or documentation updates', 'Report customisation, policy review, documentation updates'),
                ]
            }),
        ]
    },
    {
        'num': '15',
        'title': 'Escalation Process',
        'subtitle': 'NOC and Service Desk escalation paths, timeframes, and contacts',
        'body': [
            ('para', "Clear escalation paths ensure that every issue reaches the right person at the right time — whether at CDMA or within your organisation."),
            ('heading3', 'NOC Escalation Path'),
            ('table', {
                'headers': ['Level', 'Role', 'Trigger', 'Actions'],
                'col_widths': [0.12, 0.22, 0.28, 0.38],
                'rows': [
                    ('L1', 'NOC Analyst', 'Alert received', 'Triage, initial remediation attempt, documentation, client notification for P1'),
                    ('L2', 'Senior NOC Engineer', 'Unresolved after 15–30 min', 'Advanced troubleshooting, vendor engagement, parallel remediation tracks'),
                    ('L3', 'NOC Team Lead', 'P1 incidents or > 1 hour', 'Management escalation, stakeholder updates every 30 min, resource allocation'),
                    ('L4', 'CDMA Management', '> 2 hours or significant business impact', 'Executive communication, emergency resources, executive-level client contact'),
                ]
            }),
            ('heading3', 'Service Desk Escalation Path'),
            ('table', {
                'headers': ['Level', 'Role', 'Trigger', 'Actions'],
                'col_widths': [0.12, 0.22, 0.28, 0.38],
                'rows': [
                    ('L1', 'Service Desk Agent', 'Ticket created', 'Issue logging, initial troubleshooting, basic resolution attempt'),
                    ('L2', 'Service Desk Senior', 'Complex issue or SLA risk', 'Advanced troubleshooting, vendor coordination, on-site assessment'),
                    ('L3', 'Technical Specialist', 'Engineering-level investigation required', 'Deep technical investigation, vendor escalation, on-site dispatch coordination'),
                    ('L4', 'Service Delivery Manager', 'Recurring issues or client dissatisfaction', 'Root cause review, service improvement plan, client relationship management'),
                ]
            }),
            ('callout', 'All P1 incidents trigger automatic notification to your designated contacts via SMS and email within 5 minutes of detection — regardless of time of day.'),
            ('heading3', 'Client Escalation Contacts'),
            ('para', "Each client has a named Service Delivery Manager (SDM) as their primary escalation contact within CDMA. The SDM is responsible for service quality, monthly reporting, quarterly reviews, and acting as an advocate within CDMA for the client's needs."),
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
                'headers': ['Framework', 'CDMA Status', 'Relevance to Hospitality'],
                'col_widths': [0.22, 0.22, 0.56],
                'rows': [
                    ('ISO 27001:2022', 'CDMA certified', 'Information security management — baseline for all service delivery and data handling'),
                    ('PCI DSS', 'Advisory and support services', 'Guest payment card data protection, network segmentation, quarterly scanning'),
                    ('GDPR', 'Compliant + client support services', 'Guest personal data handling, breach notification, DPA templates for processors'),
                    ('SOC 2 Type II', 'In progress', 'Security, availability, and confidentiality assurance for MSP and enterprise clients'),
                    ('NIS2 Directive', 'Advisory services', 'Network and information security obligations for relevant hospitality operators'),
                    ('DORA', 'Advisory services', 'Digital operational resilience for hospitality groups with financial services linkage'),
                    ('Cyber Essentials Plus', 'CDMA certified', 'UK-aligned baseline security controls demonstrating fundamental cyber hygiene'),
                ]
            }),
            ('heading3', 'Data Handling Principles'),
            ('bullets', [
                'All client data is processed under a formal Data Processing Agreement (DPA)',
                'Data is stored in EU-based infrastructure with encrypted transmission and storage',
                'Access to client environments is strictly role-based with full audit logging',
                'Encryption at rest (AES-256) and in transit (TLS 1.2+) for all managed data',
                'Annual penetration testing of CDMA internal systems by independent assessors',
                'Security awareness training for all CDMA staff, mandatory annually',
                'Supplier and subcontractor security assessments conducted before engagement',
            ]),
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
                'col_widths': [0.30, 0.70],
                'rows': [
                    ('Founded', '2011'),
                    ('Global Reach', '56 countries across 6 continents'),
                    ('Office Locations', 'Nicosia (HQ), Dubai, Athens'),
                    ('Certifications', 'ISO 27001:2022, Cyber Essentials Plus, multiple vendor certifications'),
                    ('Service Model', 'White-label managed IT, cybersecurity, and project services'),
                    ('NOC & Service Desk', '24/7/365 operations with dedicated hospitality playbooks'),
                    ('Specialisations', 'Hospitality, healthcare, financial services, and enterprise'),
                    ('Languages', 'English, Greek, Arabic — multilingual support available'),
                ]
            }),
            ('heading3', 'Our Hospitality Expertise'),
            ('para', "CDMA has extensive experience supporting hospitality organisations across the Mediterranean, Middle East, and beyond. Our teams understand the seasonal pressures, system interdependencies, and compliance requirements unique to the hotel industry — delivering IT support that truly understands the hospitality context."),
            ('callout', 'White-label delivery means your guests and staff experience seamless, professionally branded IT support — they never know CDMA is behind it.'),
            ('heading3', 'Contact Us'),
            ('table', {
                'headers': ['Channel', 'Contact'],
                'col_widths': [0.20, 0.80],
                'rows': [
                    ('Website', 'cdma.com.cy'),
                    ('Sales Email', 'sales@cdma.com.cy'),
                    ('Phone', '+357 22 028014'),
                    ('Headquarters', 'Nicosia, Cyprus'),
                    ('Regional Office', 'Dubai, UAE'),
                    ('Regional Office', 'Athens, Greece'),
                ]
            }),
        ]
    },
]

TOC_ENTRIES = [(s['num'], s['title'], s['subtitle']) for s in SECTIONS]

# ── Cover Pages ────────────────────────────────────────────────────────────────

def draw_cover_landscape(c, W, H):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    # Decorative bg circle
    c.saveState(); c.setFillColor(CYAN); c.setFillAlpha(0.06)
    c.circle(W, H, H * 0.85, fill=1, stroke=0); c.restoreState()
    # Left cyan strip
    c.setFillColor(CYAN); c.rect(0, 0, 6 * mm, H, fill=1, stroke=0)
    # Cyan accent line
    c.setFillColor(CYAN); c.rect(22 * mm, H * 0.515, W * 0.55, 1.5, fill=1, stroke=0)
    # Text
    lx = 22 * mm; cy = H * 0.5
    c.setFont('Inter-Black', 78); c.setFillColor(WHITE); c.drawString(lx, cy + 44, 'CDMA')
    c.setFont('Inter-Bold', 36); c.setFillColor(CYAN);  c.drawString(lx, cy + 5, 'HOSPITALITY')
    c.setFont('Inter-Light', 36); c.setFillColor(WHITE); c.drawString(lx, cy - 30, 'PLAYBOOK')
    c.setFont('Inter-Light', 10.5); c.setFillColor(HexColor('#A8BFDA'))
    c.drawString(lx, cy - 58, "A Comprehensive Guide to CDMA's Managed IT &")
    c.drawString(lx, cy - 71, "Cybersecurity Services for Hospitality Organisations")
    c.setFont('Inter-SemiBold', 9); c.setFillColor(CYAN)
    c.drawString(lx, cy - 91, 'MAY 2025 EDITION')
    # Bottom bar
    c.setFillColor(DARK_BG); c.rect(0, 0, W, 14 * mm, fill=1, stroke=0)
    c.setFont('Inter-Regular', 8); c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(22 * mm, 4.5 * mm, 'CDMA Services Ltd  |  cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 8); c.setFillColor(CYAN)
    c.drawRightString(W - 22 * mm, 4.5 * mm, 'CONFIDENTIAL')

def draw_cover_portrait(c, W, H):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.saveState(); c.setFillColor(CYAN); c.setFillAlpha(0.06)
    c.circle(W, H, H * 0.65, fill=1, stroke=0); c.restoreState()
    c.setFillColor(CYAN); c.rect(0, 0, 5 * mm, H, fill=1, stroke=0)
    c.setFillColor(CYAN); c.rect(15 * mm, H * 0.55, W * 0.65, 1.5, fill=1, stroke=0)
    lx = 17 * mm; cy = H * 0.54
    c.setFont('Inter-Black', 68); c.setFillColor(WHITE); c.drawString(lx, cy + 48, 'CDMA')
    c.setFont('Inter-Bold', 30); c.setFillColor(CYAN);  c.drawString(lx, cy + 12, 'HOSPITALITY')
    c.setFont('Inter-Light', 30); c.setFillColor(WHITE); c.drawString(lx, cy - 20, 'PLAYBOOK')
    c.setFont('Inter-Light', 10); c.setFillColor(HexColor('#A8BFDA'))
    c.drawString(lx, cy - 49, "A Comprehensive Guide to CDMA's")
    c.drawString(lx, cy - 61, "Managed IT & Cybersecurity Services")
    c.drawString(lx, cy - 73, "for Hospitality Organisations")
    c.setFont('Inter-SemiBold', 8); c.setFillColor(CYAN)
    c.drawString(lx, cy - 91, 'MAY 2025 EDITION')
    c.setFillColor(DARK_BG); c.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    c.setFont('Inter-Regular', 7.5); c.setFillColor(HexColor('#8AAAC5'))
    c.drawString(17 * mm, 10 * mm, 'cdma.com.cy  |  sales@cdma.com.cy')
    c.drawString(17 * mm, 4 * mm, '+357 22 028014  |  CDMA Services Ltd')
    c.setFont('Inter-SemiBold', 7.5); c.setFillColor(CYAN)
    c.drawRightString(W - 17 * mm, 7 * mm, 'CONFIDENTIAL')


# ── Introduction Page ──────────────────────────────────────────────────────────

def draw_intro(pb):
    c = pb.c; margin = pb.margin; W = pb.page_w
    y = pb.start_interior_page()
    c.setFont('Inter-SemiBold', 9); c.setFillColor(CYAN)
    c.drawString(margin, y, 'INTRODUCTION')
    y -= 10 * mm
    c.setFont('Inter-Bold', 22); c.setFillColor(NAVY)
    c.drawString(margin, y, 'Hospitality Never Sleeps.')
    y -= 6 * mm
    c.setFillColor(CYAN); c.rect(margin, y, 30 * mm, 2, fill=1, stroke=0)
    y -= 9 * mm
    paras = [
        "Your guests expect seamless connectivity, instant service, and zero downtime — 24 hours a day, 365 days a year. Behind every smooth check-in, reliable guest Wi-Fi connection, and flawless point-of-sale transaction sits a complex IT infrastructure that demands constant attention.",
        "This playbook has been created specifically for hospitality organisations and the Managed Service Providers (MSPs) who support them. It explores CDMA's full suite of services in the context of hotel groups, resorts, boutique properties, and hospitality venues — explaining how our NOC, Service Desk, cybersecurity, network architecture, and project capabilities address the unique demands of this fast-moving industry.",
        "Whether you manage a single property or a portfolio spanning multiple countries, CDMA provides the always-on IT backbone that hospitality demands — from guest Wi-Fi and captive portal design to Mobile DAS, backup and disaster recovery, and 24/7 managed detection and response.",
    ]
    for p in paras:
        h = draw_wrapped(c, p, margin, y, pb.content_w, 'Inter-Regular', 10.5, DGRAY, 14)
        y -= h + 6 * mm
    # Callout
    ct = "All CDMA services are delivered on a white-label basis. From your guests' and staff's perspective, we operate as a seamless extension of your own IT team."
    ch = text_height_estimate(ct, pb.content_w - 8*mm, 'Inter-Light', 9.5, 13.5) + 9*mm
    c.setFillColor(CYAN_SOFT); c.rect(margin, y - ch, pb.content_w, ch, fill=1, stroke=0)
    c.setFillColor(CYAN); c.rect(margin, y - ch, 3, ch, fill=1, stroke=0)
    draw_wrapped(c, ct, margin + 6*mm, y - 4*mm, pb.content_w - 8*mm, 'Inter-Light', 9.5, NAVY, 13.5)


# ── Table of Contents ──────────────────────────────────────────────────────────

def draw_toc(pb):
    c = pb.c; margin = pb.margin; W = pb.page_w
    y = pb.start_interior_page()
    c.setFont('Inter-SemiBold', 9); c.setFillColor(CYAN)
    c.drawString(margin, y, 'CONTENTS')
    y -= 8 * mm
    c.setFont('Inter-Bold', 22); c.setFillColor(NAVY)
    c.drawString(margin, y, 'Table of Contents')
    y -= 5 * mm
    c.setFillColor(CYAN); c.rect(margin, y, 25 * mm, 2, fill=1, stroke=0)
    y -= 9 * mm

    # Two-column layout for TOC
    col_w = (pb.content_w - 8 * mm) / 2
    entries_left  = TOC_ENTRIES[:9]
    entries_right = TOC_ENTRIES[9:]
    row_h = 9 * mm

    for col_idx, entries in enumerate([entries_left, entries_right]):
        col_x = margin + col_idx * (col_w + 8 * mm)
        ey = y
        for num, title, subtitle in entries:
            # Badge
            c.setFillColor(NAVY)
            c.circle(col_x + 5.5*mm, ey - 1*mm, 5.5*mm, fill=1, stroke=0)
            c.setFont('Inter-Bold', 7); c.setFillColor(WHITE)
            c.drawCentredString(col_x + 5.5*mm, ey - 3, num)
            # Title
            tx = col_x + 13 * mm
            c.setFont('Inter-SemiBold', 8.5); c.setFillColor(NAVY)
            # Truncate long title
            title_str = title if len(title) < 42 else title[:39] + '...'
            c.drawString(tx, ey + 0.5*mm, title_str)
            # Subtitle
            c.setFont('Inter-Light', 7); c.setFillColor(GRAY)
            sub_str = subtitle if len(subtitle) < 52 else subtitle[:49] + '...'
            c.drawString(tx, ey - 4.5*mm, sub_str)
            # Separator line
            c.setStrokeColor(LIGHT); c.setLineWidth(0.3)
            c.line(col_x, ey - row_h + 1*mm, col_x + col_w, ey - row_h + 1*mm)
            ey -= row_h


# ── Outro Pages ────────────────────────────────────────────────────────────────

def draw_outro(c, W, H, page_num, is_landscape):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.saveState(); c.setFillColor(CYAN); c.setFillAlpha(0.07)
    c.circle(W, H, H * (0.75 if is_landscape else 0.6), fill=1, stroke=0); c.restoreState()
    strip = 6 * mm if is_landscape else 5 * mm
    c.setFillColor(CYAN); c.rect(0, 0, strip, H, fill=1, stroke=0)
    # Bottom bar
    c.setFillColor(DARK_BG); c.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    c.setFont('Inter-Regular', 7.5); c.setFillColor(HexColor('#8AAAC5'))
    lx = 22 * mm if is_landscape else 15 * mm
    c.drawString(lx, 10 * mm, 'CDMA Services Ltd — May 2025 — Confidential')
    c.drawString(lx, 4 * mm, 'cdma.com.cy  |  sales@cdma.com.cy  |  +357 22 028014')
    c.setFont('Inter-SemiBold', 7.5); c.setFillColor(CYAN)
    c.drawRightString(W - lx, 7 * mm, f'Page {page_num}')
    # Main text
    cx = W / 2 if not is_landscape else None
    if is_landscape:
        lx2 = 22 * mm; cy = H * 0.52
        c.setFont('Inter-Light', 13); c.setFillColor(HexColor('#8AAAC5'))
        c.drawString(lx2, cy + 58, 'YOUR HOSPITALITY IT PARTNER')
        c.setFillColor(CYAN); c.rect(lx2, cy + 53, 60*mm, 1.5, fill=1, stroke=0)
        c.setFont('Inter-Black', 36); c.setFillColor(WHITE); c.drawString(lx2, cy + 18, 'Always On.')
        c.setFont('Inter-Light', 36); c.setFillColor(CYAN);  c.drawString(lx2, cy - 18, 'Always Secure.')
        c.setFont('Inter-Bold', 12); c.setFillColor(WHITE);  c.drawString(lx2, cy - 40, 'Always With You.')
        c.setFont('Inter-SemiBold', 9); c.setFillColor(HexColor('#A8BFDA'))
        c.drawString(lx2, cy - 62, 'GET IN TOUCH')
        c.setFillColor(CYAN); c.rect(lx2, cy - 65, 14*mm, 1, fill=1, stroke=0)
        contacts = [('Web', 'cdma.com.cy'), ('Email', 'sales@cdma.com.cy'),
                    ('Phone', '+357 22 028014'), ('HQ', 'Nicosia, Cyprus')]
        cy2 = cy - 76
        for label, val in contacts:
            c.setFont('Inter-Light', 9); c.setFillColor(HexColor('#8AAAC5'))
            c.drawString(lx2, cy2, label + ':')
            c.setFont('Inter-Regular', 9); c.setFillColor(WHITE)
            c.drawString(lx2 + 18*mm, cy2, val)
            cy2 -= 8.5 * mm
        # ISO badge (right side)
        bx = W - 85 * mm; by = cy - 38; bw = 65 * mm; bh = 68 * mm
        c.setFillColor(MID_NAVY); c.roundRect(bx, by, bw, bh, 5, fill=1, stroke=0)
        c.setFont('Inter-Bold', 9.5); c.setFillColor(CYAN)
        c.drawCentredString(bx + bw/2, by + bh - 14*mm, 'ISO 27001:2022')
        c.setFont('Inter-Light', 8.5); c.setFillColor(WHITE)
        c.drawCentredString(bx + bw/2, by + bh - 23*mm, 'Certified')
        c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
        c.line(bx + 6*mm, by + bh - 27*mm, bx + bw - 6*mm, by + bh - 27*mm)
        items = ['56 Countries', '6 Continents', '24/7/365 NOC', 'White-Label MSP']
        iy = by + bh - 36*mm
        for item in items:
            c.setFillColor(CYAN); c.circle(bx + 10*mm, iy, 2.5, fill=1, stroke=0)
            c.setFont('Inter-Regular', 8.5); c.setFillColor(WHITE)
            c.drawString(bx + 14*mm, iy - 3, item)
            iy -= 9 * mm
    else:
        cy = H * 0.58
        c.setFont('Inter-Light', 11); c.setFillColor(HexColor('#8AAAC5'))
        c.drawCentredString(W/2, cy + 55, 'YOUR HOSPITALITY IT PARTNER')
        c.setFillColor(CYAN); c.rect(W/2 - 30*mm, cy + 50, 60*mm, 1.5, fill=1, stroke=0)
        c.setFont('Inter-Black', 30); c.setFillColor(WHITE); c.drawCentredString(W/2, cy + 20, 'Always On.')
        c.setFont('Inter-Light', 27); c.setFillColor(CYAN);  c.drawCentredString(W/2, cy - 6, 'Always Secure.')
        c.setFont('Inter-Bold', 12); c.setFillColor(WHITE);  c.drawCentredString(W/2, cy - 24, 'Always With You.')
        c.setFont('Inter-SemiBold', 8); c.setFillColor(HexColor('#A8BFDA'))
        c.drawCentredString(W/2, cy - 44, 'GET IN TOUCH')
        c.setFillColor(CYAN); c.rect(W/2 - 15*mm, cy - 47, 30*mm, 1, fill=1, stroke=0)
        contacts = [('Web', 'cdma.com.cy'), ('Email', 'sales@cdma.com.cy'),
                    ('Phone', '+357 22 028014'), ('HQ', 'Nicosia, Cyprus')]
        cy2 = cy - 60
        for label, val in contacts:
            c.setFont('Inter-Light', 9); c.setFillColor(HexColor('#8AAAC5'))
            c.drawString(W/2 - 40*mm, cy2, label + ':')
            c.setFont('Inter-Regular', 9); c.setFillColor(WHITE)
            c.drawString(W/2 - 20*mm, cy2, val)
            cy2 -= 9 * mm
        # Badge
        bx = W/2 - 35*mm; by = cy2 - 10*mm; bw = 70*mm; bh = 38*mm
        c.setFillColor(MID_NAVY); c.roundRect(bx, by, bw, bh, 5, fill=1, stroke=0)
        c.setFont('Inter-Bold', 9); c.setFillColor(CYAN)
        c.drawCentredString(W/2, by + 28*mm, 'ISO 27001:2022  |  56 Countries')
        c.setFont('Inter-Light', 8); c.setFillColor(WHITE)
        c.drawCentredString(W/2, by + 20*mm, '24/7/365 NOC  |  White-Label Services')
        c.drawCentredString(W/2, by + 12*mm, 'Nicosia  ·  Dubai  ·  Athens')


# ── Main Build ─────────────────────────────────────────────────────────────────

def build_pdf(output_path, is_landscape=True):
    page_size = landscape(A4) if is_landscape else A4
    W, H = page_size
    c = rl_canvas.Canvas(output_path, pagesize=page_size)
    c.setTitle('CDMA Hospitality Playbook')
    c.setAuthor('CDMA Services Ltd')
    c.setSubject('Managed IT & Cybersecurity for Hospitality')

    pb = PageBuilder(c, W, H, is_landscape)

    # 1. Cover
    if is_landscape:
        draw_cover_landscape(c, W, H)
    else:
        draw_cover_portrait(c, W, H)
    c.showPage(); pb.page_num += 1

    # 2. Introduction
    pb.start_interior_page()
    draw_intro(pb)
    c.showPage(); pb.page_num += 1

    # 3. Table of Contents
    pb.start_interior_page()
    draw_toc(pb)
    c.showPage(); pb.page_num += 1

    # 4-20. Sections
    for section in SECTIONS:
        pb.start_interior_page()
        render_section_content(pb, section)
        c.showPage(); pb.page_num += 1

    # Outro
    draw_outro(c, W, H, pb.page_num, is_landscape)
    c.showPage()

    c.save()
    print(f"✅ Built: {output_path}  (pages: {pb.page_num})")


if __name__ == '__main__':
    out = '/Users/milton/clawd'
    build_pdf(f'{out}/CDMA_Hospitality_Playbook_Landscape_v3.pdf', is_landscape=True)
    build_pdf(f'{out}/CDMA_Hospitality_Playbook_Portrait_v3.pdf',  is_landscape=False)
    print("🎉 Both v3 PDFs generated.")
