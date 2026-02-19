#!/usr/bin/env python3
"""
Holaprime Share of Voice Analysis Report — v2
White background, fixed cover, better spacing, cleaner charts
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ── Brand palette (white background version) ─────────────────────────────────
GOLD        = colors.HexColor("#B8860B")   # dark gold on white
LIGHT_GOLD  = colors.HexColor("#C9A84C")
DARK_BG     = colors.HexColor("#1A1A1A")
WHITE       = colors.white
OFF_WHITE   = colors.HexColor("#FAFAF8")
LIGHT_GRAY  = colors.HexColor("#F2F2F0")
MID_GRAY    = colors.HexColor("#888888")
DARK_GRAY   = colors.HexColor("#333333")
TABLE_HDR   = colors.HexColor("#1A1600")
TABLE_ALT1  = colors.HexColor("#FFFFFF")
TABLE_ALT2  = colors.HexColor("#F9F6EC")
BLUE        = colors.HexColor("#1565C0")
GREEN       = colors.HexColor("#2E7D32")

# Chart colours per brand
BAR_COLORS  = ["#1565C0","#2E7D32","#E65100","#6A1B9A","#B8860B"]
HOLA_COLOR  = "#B8860B"

# ── Data ─────────────────────────────────────────────────────────────────────
BRANDS    = ["FTMO","Topstep","fundednext","E8 Markets","holaprime"]
MENTIONS  = [7149, 5001, 4861, 2561, 334]
SOV_VOL   = [35.4, 24.8, 24.1, 12.7, 1.7]
REACH     = [15_900_000, 11_400_000, 9_400_000, 1_439_000, 863_000]
SOV_REACH = [41.4, 29.7, 24.5, 3.7, 2.2]
RPM       = [2225, 2280, 1934, 562, 2583]
MOM_VOL   = [8.8, 94.1, 28.6, 141.9, 115.1]
MOM_REACH = [27.1, 193.1, 18.6, 140.4, 1143.8]
POSITIONS = ["🥇 Market Leader","🥈 Strong #2","🥉 Close #3","4th - Mid-tier","5th - Emerging"]


# ── Chart helpers ─────────────────────────────────────────────────────────────
def chart_buf(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=160, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf


def style_axes(ax, fig, title):
    fig.patch.set_facecolor('#FAFAF8')
    ax.set_facecolor('#FFFFFF')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(colors='#555555')
    ax.set_title(title, color='#1A1A1A', fontsize=11, pad=10, fontweight='bold', loc='left')
    ax.grid(axis='x', color='#EEEEEE', linewidth=0.8, zorder=0)


def bar_sov_volume():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    y = np.arange(len(BRANDS))
    bars = ax.barh(y, SOV_VOL, color=BAR_COLORS, height=0.5, zorder=3)
    bars[-1].set_edgecolor(HOLA_COLOR)
    bars[-1].set_linewidth(2)

    for bar, val in zip(bars, SOV_VOL):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val}%", va='center', ha='left', color='#333333', fontsize=9, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(BRANDS, color='#333333', fontsize=10)
    ax.set_xlabel("Share of Voice (%)", color='#555555', fontsize=9)
    ax.set_xlim(0, 43)
    style_axes(ax, fig, "Fig 1 — Share of Voice by Mention Volume")
    fig.tight_layout(pad=1.4)
    return chart_buf(fig)


def bar_sov_reach():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    y = np.arange(len(BRANDS))
    bars = ax.barh(y, SOV_REACH, color=BAR_COLORS, height=0.5, zorder=3)
    bars[-1].set_edgecolor(HOLA_COLOR)
    bars[-1].set_linewidth(2)

    for bar, val in zip(bars, SOV_REACH):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val}%", va='center', ha='left', color='#333333', fontsize=9, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(BRANDS, color='#333333', fontsize=10)
    ax.set_xlabel("Share of Voice — Reach (%)", color='#555555', fontsize=9)
    ax.set_xlim(0, 50)
    style_axes(ax, fig, "Fig 3 — Share of Voice by Reach & Amplification")
    fig.tight_layout(pad=1.4)
    return chart_buf(fig)


def bar_mom_growth():
    """
    Page 4 chart — cleaner: split into two separate panels side by side
    so the extreme holaprime reach value (+1,143%) doesn't crush everything else.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2))
    fig.patch.set_facecolor('#FAFAF8')

    x = np.arange(len(BRANDS))
    short = [b.replace(" Markets","") for b in BRANDS]

    # — Panel 1: Mention Volume Growth —
    ax1.set_facecolor('#FFFFFF')
    bars1 = ax1.bar(x, MOM_VOL, color=BAR_COLORS, width=0.55, zorder=3, edgecolor='white', linewidth=0.5)
    bars1[-1].set_edgecolor(HOLA_COLOR)
    bars1[-1].set_linewidth(2)
    for bar, val in zip(bars1, MOM_VOL):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
                 f"+{val:.0f}%", ha='center', va='bottom', color='#333333', fontsize=8, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(short, color='#333333', fontsize=9, rotation=15, ha='right')
    ax1.set_ylabel("Growth %", color='#555555', fontsize=9)
    ax1.set_title("Mention Volume Growth\n(Month-over-Month)", color='#1A1A1A', fontsize=10,
                  fontweight='bold', loc='left', pad=6)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#CCCCCC')
    ax1.spines['bottom'].set_color('#CCCCCC')
    ax1.tick_params(colors='#555555')
    ax1.grid(axis='y', color='#EEEEEE', linewidth=0.8, zorder=0)
    ax1.set_ylim(0, 175)

    # — Panel 2: Reach Growth (log scale so holaprime doesn't eat everything) —
    ax2.set_facecolor('#FFFFFF')
    bars2 = ax2.bar(x, MOM_REACH, color=BAR_COLORS, width=0.55, zorder=3, edgecolor='white', linewidth=0.5)
    bars2[-1].set_edgecolor(HOLA_COLOR)
    bars2[-1].set_linewidth(2)
    for bar, val in zip(bars2, MOM_REACH):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
                 f"+{val:.0f}%", ha='center', va='bottom', color='#333333', fontsize=8, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(short, color='#333333', fontsize=9, rotation=15, ha='right')
    ax2.set_ylabel("Growth % (note: log scale)", color='#555555', fontsize=9)
    ax2.set_title("Reach Amplification Growth\n(Month-over-Month)", color='#1A1A1A', fontsize=10,
                  fontweight='bold', loc='left', pad=6)
    ax2.set_yscale('log')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#CCCCCC')
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(colors='#555555', which='both')
    ax2.grid(axis='y', color='#EEEEEE', linewidth=0.8, zorder=0, which='both')
    ax2.set_ylim(10, 2500)
    # annotate holaprime separately
    ax2.annotate("holaprime\n+1,143.8%", xy=(x[-1], MOM_REACH[-1]),
                 xytext=(x[-1]-0.8, 800),
                 arrowprops=dict(arrowstyle='->', color=HOLA_COLOR, lw=1.5),
                 color=HOLA_COLOR, fontsize=8, fontweight='bold')

    fig.suptitle("Fig 2 — Month-over-Month Growth: Mention Volume & Reach", color='#1A1A1A',
                 fontsize=11, fontweight='bold', x=0.02, ha='left', y=1.01)
    fig.tight_layout(pad=1.5)
    return chart_buf(fig)


def bar_reach_efficiency():
    fig, ax = plt.subplots(figsize=(8, 3.6))
    bars = ax.bar(BRANDS, RPM, color=BAR_COLORS, width=0.55, zorder=3, edgecolor='white', linewidth=0.5)
    bars[-1].set_edgecolor(HOLA_COLOR)
    bars[-1].set_linewidth(2.5)

    for bar, val in zip(bars, RPM):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+15,
                f"{val:,}", ha='center', va='bottom', color='#333333', fontsize=9, fontweight='bold')

    ax.set_xticklabels(BRANDS, color='#333333', fontsize=9)
    ax.set_ylabel("Reach per Mention", color='#555555', fontsize=9)
    ax.set_ylim(0, 3200)
    style_axes(ax, fig, "Fig 4 — Reach Efficiency: Impressions per Mention")
    fig.tight_layout(pad=1.4)
    return chart_buf(fig)


def pie_sov():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    fig.patch.set_facecolor('#FAFAF8')

    wedge_props = dict(width=0.55, edgecolor='white', linewidth=2)
    explode = [0, 0, 0, 0, 0.1]

    for ax, vals, title in [(ax1, SOV_VOL, "Mention Volume"),
                             (ax2, SOV_REACH, "Reach Share")]:
        ax.set_facecolor('#FAFAF8')
        wedges, texts, autotexts = ax.pie(
            vals, colors=BAR_COLORS, autopct='%1.1f%%',
            startangle=90, explode=explode,
            wedgeprops=wedge_props, pctdistance=0.75, labels=None
        )
        for t in autotexts:
            t.set_fontsize(7.5)
            t.set_color('#1A1A1A')
        ax.set_title(title, color='#1A1A1A', fontsize=10, fontweight='bold')

    patches = [mpatches.Patch(color=c, label=b) for c, b in zip(BAR_COLORS, BRANDS)]
    fig.legend(handles=patches, loc='lower center', ncol=5,
               facecolor='#FAFAF8', edgecolor='#CCCCCC', labelcolor='#333333',
               fontsize=9, bbox_to_anchor=(0.5, -0.04))
    fig.suptitle("Fig 5 — Market Share Distribution: Volume vs Reach",
                 color='#1A1A1A', fontsize=11, fontweight='bold', x=0.02, ha='left')
    fig.tight_layout(pad=1.2)
    return chart_buf(fig)


# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    S = {}

    S['report_tag'] = ParagraphStyle('report_tag',
        fontName='Helvetica', fontSize=8.5, textColor=MID_GRAY,
        spaceAfter=2, alignment=TA_LEFT)

    S['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=26, textColor=DARK_GRAY,
        spaceAfter=6, spaceBefore=0, alignment=TA_LEFT, leading=30)

    S['cover_sub1'] = ParagraphStyle('cover_sub1',
        fontName='Helvetica-Bold', fontSize=14, textColor=GOLD,
        spaceAfter=4, spaceBefore=0, alignment=TA_LEFT)

    S['cover_sub2'] = ParagraphStyle('cover_sub2',
        fontName='Helvetica', fontSize=11, textColor=MID_GRAY,
        spaceAfter=16, spaceBefore=0, alignment=TA_LEFT)

    S['h1'] = ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=14, textColor=DARK_GRAY,
        spaceBefore=18, spaceAfter=6, borderPad=0)

    S['h2'] = ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#555500"),
        spaceBefore=14, spaceAfter=5)

    S['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY,
        leading=15, spaceAfter=8, alignment=TA_JUSTIFY)

    S['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY,
        leading=14, leftIndent=16, spaceAfter=5, bulletIndent=4)

    S['caption'] = ParagraphStyle('caption',
        fontName='Helvetica-Oblique', fontSize=8, textColor=MID_GRAY,
        spaceAfter=6, spaceBefore=2, alignment=TA_LEFT)

    S['callout'] = ParagraphStyle('callout',
        fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.HexColor("#5A3E00"),
        leading=15, spaceBefore=8, spaceAfter=8,
        backColor=colors.HexColor("#FFF8DC"),
        leftIndent=10, rightIndent=10, borderPad=8)

    S['footer'] = ParagraphStyle('footer',
        fontName='Helvetica', fontSize=7.5, textColor=MID_GRAY,
        spaceAfter=0, alignment=TA_RIGHT)

    S['section_intro'] = ParagraphStyle('section_intro',
        fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor("#555555"),
        leading=15, spaceAfter=10, alignment=TA_JUSTIFY,
        leftIndent=0)

    return S


# ── Table helpers ─────────────────────────────────────────────────────────────
def light_table(data, col_widths, hdr_rows=1):
    tbl = Table(data, colWidths=col_widths, repeatRows=hdr_rows)
    tbl.setStyle(TableStyle([
        # Header — gold background, dark text, clearly readable on white page
        ('BACKGROUND',    (0,0), (-1,hdr_rows-1), colors.HexColor("#C9A84C")),
        ('TEXTCOLOR',     (0,0), (-1,hdr_rows-1), colors.HexColor("#1A1A1A")),
        ('FONTNAME',      (0,0), (-1,hdr_rows-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,hdr_rows-1), 8.5),
        ('TOPPADDING',    (0,0), (-1,hdr_rows-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,hdr_rows-1), 8),
        ('ALIGN',         (0,0), (-1,hdr_rows-1), 'CENTER'),
        # Body
        ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR',     (0,1), (-1,-1), DARK_GRAY),
        ('TOPPADDING',    (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [TABLE_ALT1, TABLE_ALT2]),
        # Lines
        ('LINEBELOW',     (0,0), (-1,hdr_rows-1), 1.5, colors.HexColor("#8B6914")),
        ('LINEBELOW',     (0,-1), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('INNERGRID',     (0,1), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
        ('BOX',           (0,0), (-1,-1), 0.8, colors.HexColor("#C9A84C")),
        # Alignment
        ('ALIGN',         (1,1), (-1,-1), 'CENTER'),
        ('ALIGN',         (0,1), (0,-1), 'LEFT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ]))
    return tbl


# ── Page callbacks ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # White background
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Gold top stripe
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 5*mm, w, 5*mm, fill=1, stroke=0)
    # Light gold thin line below stripe
    canvas.setFillColor(colors.HexColor("#F0E0A0"))
    canvas.rect(0, h - 6*mm, w, 1*mm, fill=1, stroke=0)
    # Footer bar
    canvas.setFillColor(colors.HexColor("#F5F0E0"))
    canvas.rect(0, 0, w, 11*mm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#DDCCAA"))
    canvas.setLineWidth(0.5)
    canvas.line(0, 11*mm, w, 11*mm)
    # Footer text
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(15*mm, 4*mm,
        "CY: +357 7000 1372   ·   mg@growth-onomics.com   ·   www.growth-onomics.com")
    canvas.drawRightString(w - 15*mm, 4*mm, f"Page {doc.page}")
    canvas.restoreState()


# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    out = "/Users/milton/clawd/Holaprime_SoV_Report_Enhanced.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=22*mm, bottomMargin=20*mm,
        title="Holaprime Share of Voice Analysis Report"
    )
    S = make_styles()
    story = []

    # ─── COVER PAGE ──────────────────────────────────────────────────────────
    story.append(Paragraph("growth-onomics   ·   Competitive Intelligence", S['report_tag']))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("Share of Voice", S['cover_title']))
    story.append(Paragraph("Analysis Report", S['cover_title']))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=5))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("holaprime vs Competitor Prop Firms", S['cover_sub1']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Analysis Period: January 18 – February 18, 2026", S['cover_sub2']))

    # Key stats mini-table on cover
    cover_stats = [
        ["Competitive Set", "FTMO · Topstep · fundednext · E8 Markets"],
        ["Total Market Mentions", "20,194"],
        ["Total Market Reach", "38.4M impressions"],
        ["Report Date", "February 2026"],
    ]
    cs_tbl = Table(cover_stats, colWidths=[55*mm, 100*mm])
    cs_tbl.setStyle(TableStyle([
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',   (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('TEXTCOLOR',  (0,0), (0,-1), DARK_GRAY),
        ('TEXTCOLOR',  (1,0), (1,-1), colors.HexColor("#555555")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',(0,0), (-1,-1), 0),
        ('LINEBELOW',  (0,0), (-1,-1), 0.4, colors.HexColor("#DDCCAA")),
        ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
    ]))
    story.append(cs_tbl)
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(
        "Prepared by Growth-onomics Strategic Intelligence Division · Confidential",
        S['report_tag']))

    story.append(PageBreak())

    # ─── SECTION 1: VOLUME SOV ────────────────────────────────────────────────
    story.append(Paragraph("1. Market Share Analysis: Volume & Visibility", S['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=8))

    story.append(Paragraph("1.1  Share of Voice by Mention Volume", S['h2']))
    story.append(Paragraph(
        "The proprietary trading firm market demonstrates significant concentration, with established players "
        "dominating the conversation landscape. Out of <b>20,194 total mentions</b> captured across all digital "
        "channels during the 32-day analysis period, the distribution reveals a highly competitive but uneven "
        "playing field.",
        S['body']))

    # Chart
    img_vol = Image(bar_sov_volume(), width=165*mm, height=70*mm)
    story.append(img_vol)
    story.append(Spacer(1, 3*mm))

    # Table
    _th = ParagraphStyle('_th', fontName='Helvetica-Bold', fontSize=8,
                         textColor=colors.HexColor("#1A1A1A"), leading=11, alignment=TA_CENTER)
    vol_hdrs = [Paragraph(h, _th) for h in
                ["Brand", "Mentions", "Share\nof Voice", "Position", "Gap to\nLeader", "MoM\nTrend"]]
    gap_lbl  = ["—", "-2,148 (−30%)", "-2,288 (−32%)", "-4,588 (−64%)", "-6,815 (−95%)"]
    mom_lbl  = ["+8.8%", "+94.1%", "+28.6%", "+141.9%", "+115.1%"]
    vol_data = [vol_hdrs] + [
        [b, f"{m:,}", f"{s}%", pos, gap, mom]
        for b, m, s, pos, gap, mom in zip(BRANDS, MENTIONS, SOV_VOL, POSITIONS, gap_lbl, mom_lbl)
    ]
    cw = [30*mm, 22*mm, 26*mm, 32*mm, 30*mm, 25*mm]
    t = light_table(vol_data, cw)
    # Highlight holaprime row
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#FFF8DC")),
        ('TEXTCOLOR',  (0,5), (-1,5), colors.HexColor("#5A3E00")),
        ('FONTNAME',   (0,5), (-1,5), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        "⚡ Market Concentration: The top 3 players (FTMO, Topstep, fundednext) collectively command "
        "<b>84.3%</b> of all online conversations, leaving only 15.7% of the discussion space for "
        "emerging and mid-tier competitors. holaprime is the <b>fastest-growing brand</b> in this window.",
        S['callout']))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Challenges & Opportunities", S['h2']))

    cols_data = [
        [Paragraph("<b>Challenges</b>", ParagraphStyle('ch',fontName='Helvetica-Bold',fontSize=9.5,textColor=colors.HexColor("#8B0000"),spaceAfter=4)),
         Paragraph("<b>Opportunities</b>", ParagraphStyle('op',fontName='Helvetica-Bold',fontSize=9.5,textColor=colors.HexColor("#1A5C00"),spaceAfter=4))],
        [Paragraph("• High barrier to entry in brand awareness\n• Established competitors have loyal communities\n• Significant investment required to compete on volume", ParagraphStyle('cb',fontName='Helvetica',fontSize=9,leading=14,textColor=DARK_GRAY,spaceAfter=0)),
         Paragraph("• Topstep shows 26.1% negative sentiment — audience is up for grabs\n• Fragmented 15.7% market share is contestable\n• Quality-over-quantity approach differentiates holaprime", ParagraphStyle('ob',fontName='Helvetica',fontSize=9,leading=14,textColor=DARK_GRAY,spaceAfter=0))],
    ]
    cols_tbl = Table(cols_data, colWidths=[82*mm, 82*mm])
    cols_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#FFF0F0")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F0FFF0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),
        ('RIGHTPADDING',(0,0),(-1,-1),10),
        ('BOX',        (0,0),(0,-1), 0.5, colors.HexColor("#FFCCCC")),
        ('BOX',        (1,0),(1,-1), 0.5, colors.HexColor("#CCFFCC")),
        ('VALIGN',     (0,0),(-1,-1),'TOP'),
    ]))
    story.append(cols_tbl)

    story.append(PageBreak())

    # ─── SECTION 1.2: REACH ──────────────────────────────────────────────────
    story.append(Paragraph("1.2  Share of Voice by Reach & Amplification", S['h2']))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#DDCCAA"), spaceAfter=8))

    story.append(Paragraph(
        "While mention volume provides one dimension of market presence, reach metrics reveal the true "
        "amplification and audience impact of each brand's content. The total combined reach across all "
        "analyzed prop firms reached <b>38,426,000 impressions</b> during the study period.",
        S['body']))

    img_reach = Image(bar_sov_reach(), width=165*mm, height=70*mm)
    story.append(img_reach)
    story.append(Spacer(1, 3*mm))

    _th2 = ParagraphStyle('_th2', fontName='Helvetica-Bold', fontSize=8,
                          textColor=colors.HexColor("#1A1A1A"), leading=11, alignment=TA_CENTER)
    reach_hdrs = [Paragraph(h, _th2) for h in
                  ["Brand", "Total\nReach", "Reach\nSoV", "Reach /\nMention",
                   "Efficiency\nRank", "Reach\nGrowth MoM"]]
    eff_ranks  = ["3rd","2nd","4th","5th","🥇 1st"]
    reach_data = [reach_hdrs] + [
        [b, f"{r/1e6:.1f}M", f"{sr}%", f"{rpm:,}", eff, f"+{rg:.1f}%"]
        for b,r,sr,rpm,eff,rg in zip(BRANDS,REACH,SOV_REACH,RPM,eff_ranks,MOM_REACH)
    ]
    cw2 = [28*mm, 26*mm, 24*mm, 28*mm, 24*mm, 35*mm]
    t2 = light_table(reach_data, cw2)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#FFF8DC")),
        ('TEXTCOLOR',  (0,5), (-1,5), colors.HexColor("#5A3E00")),
        ('FONTNAME',   (0,5), (-1,5), 'Helvetica-Bold'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        "🏆 Critical Discovery — The Reach Efficiency Advantage: Despite ranking last in absolute mention "
        "volume, holaprime achieves the <b>highest reach efficiency in the entire competitive set</b> at "
        "<b>2,583 impressions per mention</b> — outperforming even market leader FTMO by 16.1%.",
        S['callout']))

    story.append(Spacer(1, 4*mm))
    img_eff = Image(bar_reach_efficiency(), width=165*mm, height=70*mm)
    story.append(img_eff)
    story.append(Spacer(1, 3*mm))

    eff_bullets = [
        "<b>+16.5%</b> more efficient than Topstep (2,583 vs 2,280)",
        "<b>+33.6%</b> more efficient than fundednext (2,583 vs 1,934)",
        "<b>+359.6%</b> more efficient than E8 Markets (2,583 vs 562)",
        "<b>+16.1%</b> more efficient than FTMO (2,583 vs 2,225)",
    ]
    for b in eff_bullets:
        story.append(Paragraph(f"• {b}", S['bullet']))

    story.append(PageBreak())

    # ─── SECTION 2: MoM GROWTH (Page 4) ──────────────────────────────────────
    story.append(Paragraph("2. Month-over-Month Growth Analysis", S['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=8))

    story.append(Paragraph(
        "Tracking growth momentum across the 32-day period reveals a clear divergence: while established "
        "players show steady or moderate growth, holaprime and E8 Markets are the breakout stories. "
        "The two panels below separate mention volume growth from reach growth to give each metric "
        "appropriate scale — the numbers are too different to plot together meaningfully.",
        S['body']))

    img_mom = Image(bar_mom_growth(), width=165*mm, height=82*mm)
    story.append(img_mom)
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "Note: Reach Growth is displayed on a logarithmic scale. holaprime's +1,143.8% reach growth would "
        "make all other bars invisible on a linear scale — this chart design preserves readability for all brands.",
        S['caption']))

    story.append(Spacer(1, 8*mm))

    # MoM summary table
    story.append(Paragraph("Growth Summary Table", S['h2']))

    # Use short wrapped header labels via Paragraph so nothing gets clipped
    hdr_style = ParagraphStyle('th',
        fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#1A1A1A"),
        leading=11, alignment=TA_CENTER)
    mom_hdrs = [
        Paragraph("Brand",              hdr_style),
        Paragraph("Jan\nMentions",      hdr_style),
        Paragraph("Feb\nMentions",      hdr_style),
        Paragraph("Volume\nGrowth MoM", hdr_style),
        Paragraph("Jan\nReach",         hdr_style),
        Paragraph("Feb\nReach",         hdr_style),
        Paragraph("Reach\nGrowth MoM",  hdr_style),
    ]
    jan_m = [int(t / (1 + g/100)) for t, g in zip(MENTIONS, MOM_VOL)]
    feb_m = [t - j for t, j in zip(MENTIONS, jan_m)]
    jan_r = [int(r / (1 + g/100)) for r, g in zip(REACH, MOM_REACH)]
    feb_r = [r - j for r, j in zip(REACH, jan_r)]
    mom_data = [mom_hdrs] + [
        [b, f"{jm:,}", f"{fm:,}", f"+{g:.1f}%",
         f"{jr/1e6:.2f}M", f"{fr/1e6:.2f}M", f"+{gr:.1f}%"]
        for b,jm,fm,g,jr,fr,gr in zip(BRANDS,jan_m,feb_m,MOM_VOL,jan_r,feb_r,MOM_REACH)
    ]
    cw3 = [26*mm, 22*mm, 22*mm, 26*mm, 22*mm, 22*mm, 26*mm]
    t3 = light_table(mom_data, cw3)
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#FFF8DC")),
        ('FONTNAME',   (0,5), (-1,5), 'Helvetica-Bold'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t3)

    story.append(PageBreak())

    # ─── SECTION 3: DISTRIBUTION OVERVIEW ────────────────────────────────────
    story.append(Paragraph("3. Market Share Distribution Overview", S['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=8))

    story.append(Paragraph(
        "The pie charts below visualize the same competitive landscape from a proportional perspective — "
        "comparing each brand's slice of total mentions against its slice of total reach. "
        "The gap between holaprime's mention share (1.7%) and reach share (2.2%) highlights its "
        "above-average content amplification.",
        S['body']))

    img_pie = Image(pie_sov(), width=165*mm, height=75*mm)
    story.append(img_pie)
    story.append(Spacer(1, 8*mm))

    # ─── SECTION 4: STRATEGIC INSIGHTS ───────────────────────────────────────
    story.append(Paragraph("4. Key Insights & Strategic Implications", S['h1']))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=8))

    insights = [
        ("4.1  Market Concentration Risk",
         "The top 3 players control 84.3% of conversations — a high barrier to entry for brand awareness. "
         "However, this also means the fragmented 15.7% tail is highly contestable, and holaprime's "
         "superior content efficiency gives it a structural edge in capturing quality impressions at scale."),
        ("4.2  holaprime's Growth Trajectory",
         "With +115.1% MoM volume growth and +1,143.8% MoM reach growth, holaprime is the fastest-growing "
         "brand in the competitive set on both dimensions. This asymmetric growth is a leading indicator of "
         "accelerating brand awareness heading into Q1 2026."),
        ("4.3  Quality-Over-Quantity Strategy",
         "holaprime's reach efficiency (#1 at 2,583 impressions/mention) indicates high-quality content "
         "placements in high-authority channels. Scaling content output while maintaining this quality "
         "standard will compound the reach advantage rapidly as volume increases."),
        ("4.4  Competitive Vulnerability Windows",
         "Topstep shows 26.1% negative sentiment in community discussions — a clear opportunity for "
         "holaprime to capture dissatisfied audiences. E8 Markets' volume surge (+141.9% MoM) signals "
         "an emerging near-term competitor that should be monitored closely."),
    ]
    for title, body in insights:
        story.append(Paragraph(title, S['h2']))
        story.append(Paragraph(body, S['body']))
        story.append(Spacer(1, 2*mm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDCCAA"), spaceAfter=6))
    story.append(Paragraph(
        "Report prepared by Growth-onomics  ·  Solonos 48, Nicosia  ·  "
        "CY: +357 7000 1372  ·  mg@growth-onomics.com",
        S['footer']))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅ PDF saved: {out}")
    return out


if __name__ == "__main__":
    build()
