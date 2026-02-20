#!/usr/bin/env python3
"""
Growthonomics-branded Share of Voice Report PDF generator
Uses reportlab + matplotlib
"""
import os
import io
import math
import tempfile
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
from PIL import Image as PILImage

# ─── BRAND COLORS ──────────────────────────────────────────────────────────────
DARK_BG   = "#010522"      # main dark navy background
DARK_BG2  = "#050D3E"      # slightly lighter section bg
DARK_ROW  = "#0A1550"      # table row background
LIGHT_ROW = "#0F1E65"      # alternating table row
ORANGE    = "#F8A626"      # primary accent / orange
GOLD      = "#FFBB5A"      # secondary gold / CTA
WHITE     = "#FFFFFF"
LIGHT_TXT = "#B8C4D4"     # muted text
TEAL      = "#1ECBCA"      # highlight teal
GREEN     = "#46D021"
RED_NEG   = "#FF3928"
HOLAPRIME = "#F8A626"      # holaprime highlight

# convert hex to reportlab color
def hx(h):
    h = h.lstrip('#')
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return colors.Color(r/255, g/255, b/255)

# ─── PAGE DIMENSIONS ──────────────────────────────────────────────────────────
PW, PH = A4   # 595.27 x 841.89 points

# ─── LOGO ─────────────────────────────────────────────────────────────────────
LOGO_URL = "https://growth-onomics.com/wp-content/uploads/2024/09/Group.png"
LOGO_PATH = "/tmp/growthonomics_logo.png"

def download_logo():
    if not os.path.exists(LOGO_PATH):
        try:
            req = urllib.request.Request(LOGO_URL, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req) as r, open(LOGO_PATH, 'wb') as f:
                f.write(r.read())
            print("Logo downloaded.")
        except Exception as e:
            print(f"Logo download failed: {e}")
            return None
    return LOGO_PATH

# ─── CHART HELPERS ────────────────────────────────────────────────────────────
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    return buf

def chart_to_image(buf, width_pts, height_pts):
    img = Image(buf, width=width_pts, height=height_pts)
    return img

BRAND_COLORS_LIST = [
    "#F8A626",  # FTMO - orange
    "#FFBB5A",  # Topstep - gold
    "#1ECBCA",  # fundednext - teal
    "#625DF5",  # E8 Markets - purple
    "#46D021",  # holaprime - green
]

BRAND_COLORS_MAP = {
    "FTMO":       "#F8A626",
    "Topstep":    "#FFBB5A",
    "fundednext": "#1ECBCA",
    "E8 Markets": "#625DF5",
    "holaprime":  "#46D021",
}

def make_horiz_bar_chart(brands, values, title, fmt="{:.1f}%", width_in=7, height_in=2.8):
    """Horizontal bar chart showing SoV"""
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG2)

    bar_colors = [BRAND_COLORS_MAP.get(b, "#888888") for b in brands]
    y_pos = range(len(brands))
    bars = ax.barh(list(y_pos), values, color=bar_colors, height=0.55, 
                   edgecolor='none', zorder=3)

    # value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                fmt.format(val),
                va='center', ha='left', color=WHITE, fontsize=9, fontweight='bold',
                fontfamily='Arial')

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(brands, color=WHITE, fontsize=10, fontfamily='Arial')
    ax.set_xlim(0, max(values) * 1.25)
    ax.tick_params(axis='x', colors='#555577')
    ax.xaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#333355')
    ax.set_title(title, color=ORANGE, fontsize=11, fontweight='bold',
                 fontfamily='Arial', pad=10)
    ax.grid(axis='x', color='#111133', linewidth=0.5, zorder=0)
    ax.invert_yaxis()
    fig.tight_layout(pad=0.5)
    return fig

def make_grouped_bar_chart(brands, jan_vals, feb_vals, title, ylabel="Mentions", width_in=7, height_in=2.8):
    """Grouped bar chart for month-over-month comparison"""
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG2)

    x = np.arange(len(brands))
    w = 0.35
    b1 = ax.bar(x - w/2, jan_vals, w, label='Jan', color='#3A4A8A', edgecolor='none', zorder=3)
    b2 = ax.bar(x + w/2, feb_vals, w, label='Feb',
                color=[BRAND_COLORS_MAP.get(b, "#F8A626") for b in brands],
                edgecolor='none', zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(brands, color=WHITE, fontsize=9, fontfamily='Arial')
    ax.tick_params(axis='y', colors='#555577', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#333355')
    ax.spines['left'].set_color('#333355')
    ax.set_title(title, color=ORANGE, fontsize=11, fontweight='bold',
                 fontfamily='Arial', pad=10)
    ax.set_ylabel(ylabel, color=LIGHT_TXT, fontsize=8, fontfamily='Arial')
    ax.yaxis.label.set_color(LIGHT_TXT)
    ax.tick_params(axis='y', colors=LIGHT_TXT)
    ax.grid(axis='y', color='#111133', linewidth=0.5, zorder=0)
    ax.legend(loc='upper right', facecolor='#0A1550', edgecolor='#333355',
              labelcolor=WHITE, fontsize=8)
    fig.tight_layout(pad=0.5)
    return fig

def make_growth_bar_chart(brands, growth_vals, title, width_in=7, height_in=2.8):
    """Bar chart for MoM growth %"""
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG2)

    bar_colors = [BRAND_COLORS_MAP.get(b, "#888888") for b in brands]
    x = np.arange(len(brands))
    bars = ax.bar(x, growth_vals, color=bar_colors, width=0.5, edgecolor='none', zorder=3)

    for bar, val in zip(bars, growth_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(growth_vals)*0.02,
                f"+{val:.1f}%" if val >= 0 else f"{val:.1f}%",
                ha='center', va='bottom', color=WHITE, fontsize=8, fontweight='bold',
                fontfamily='Arial')

    ax.set_xticks(x)
    ax.set_xticklabels(brands, color=WHITE, fontsize=9, fontfamily='Arial')
    ax.tick_params(axis='y', colors=LIGHT_TXT, labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#333355')
    ax.spines['left'].set_color('#333355')
    ax.set_title(title, color=ORANGE, fontsize=11, fontweight='bold',
                 fontfamily='Arial', pad=10)
    ax.set_ylabel("Growth %", color=LIGHT_TXT, fontsize=8, fontfamily='Arial')
    ax.grid(axis='y', color='#111133', linewidth=0.5, zorder=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'+{x:.0f}%' if x >= 0 else f'{x:.0f}%'))
    fig.tight_layout(pad=0.5)
    return fig

def make_reach_growth_log_chart(brands, growth_vals, title, width_in=7, height_in=2.8):
    """Log-scale bar chart for reach growth"""
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG2)

    bar_colors = [BRAND_COLORS_MAP.get(b, "#888888") for b in brands]
    x = np.arange(len(brands))
    # use log scale - shift so minimum positive
    log_vals = [math.log10(max(v, 1) + 1) for v in growth_vals]
    bars = ax.bar(x, log_vals, color=bar_colors, width=0.5, edgecolor='none', zorder=3)

    for bar, val in zip(bars, growth_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"+{val:.1f}%",
                ha='center', va='bottom', color=WHITE, fontsize=8, fontweight='bold',
                fontfamily='Arial')

    ax.set_xticks(x)
    ax.set_xticklabels(brands, color=WHITE, fontsize=9, fontfamily='Arial')
    ax.tick_params(axis='y', colors=LIGHT_TXT, labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#333355')
    ax.spines['left'].set_color('#333355')
    ax.set_title(title, color=ORANGE, fontsize=11, fontweight='bold',
                 fontfamily='Arial', pad=10)
    ax.set_ylabel("Reach Growth (log scale)", color=LIGHT_TXT, fontsize=8, fontfamily='Arial')
    ax.yaxis.set_visible(False)
    note = ax.text(0.5, 0.02, "Note: log scale — holaprime +1,143.8% reach growth",
                   transform=ax.transAxes, ha='center', va='bottom',
                   color=LIGHT_TXT, fontsize=7, fontstyle='italic', fontfamily='Arial')
    ax.grid(axis='y', color='#111133', linewidth=0.5, zorder=0)
    fig.tight_layout(pad=0.5)
    return fig

def make_pie_chart(brands, values, title, width_in=3.5, height_in=3.5):
    """Pie chart"""
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    pie_colors = [BRAND_COLORS_MAP.get(b, "#888888") for b in brands]
    wedge_props = {'edgecolor': DARK_BG, 'linewidth': 2}
    
    # explode holaprime slightly
    explode = [0.05 if b == 'holaprime' else 0 for b in brands]
    
    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=pie_colors,
        autopct='%1.1f%%', pctdistance=0.75,
        explode=explode, wedgeprops=wedge_props,
        startangle=90
    )
    for at in autotexts:
        at.set_color(DARK_BG)
        at.set_fontsize(8)
        at.set_fontweight('bold')

    ax.set_title(title, color=ORANGE, fontsize=10, fontweight='bold',
                 fontfamily='Arial', pad=8)
    
    # legend
    legend_patches = [mpatches.Patch(color=pie_colors[i], label=f"{brands[i]} ({values[i]:.1f}%)")
                      for i in range(len(brands))]
    ax.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.15),
              ncol=2, facecolor='#050D3E', edgecolor='#333355',
              labelcolor=WHITE, fontsize=7, framealpha=0.9)
    fig.tight_layout(pad=0.3)
    return fig

# ─── CUSTOM FLOWABLES ─────────────────────────────────────────────────────────

class ColoredBackground(Flowable):
    """Full-width colored background block"""
    def __init__(self, width, height, bg_color):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.bg_color = bg_color

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.rect(-10*mm, 0, self.width + 20*mm, self.height, fill=1, stroke=0)

def make_section_badge(text, bg=ORANGE, fg=DARK_BG):
    """Create a colored badge label using a Table"""
    p = Paragraph(f'<font name="Helvetica-Bold" size="8" color="{fg}">&nbsp;{text}&nbsp;</font>', 
                  ParagraphStyle('badge_inner', fontName='Helvetica-Bold', fontSize=8,
                                 textColor=hx(fg), spaceAfter=0, leading=10))
    t = Table([[p]], colWidths=[None])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), hx(bg)),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

class HorizontalLine(Flowable):
    def __init__(self, width, color, thickness=0.5):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = thickness + 2

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


# ─── PARAGRAPH STYLES ─────────────────────────────────────────────────────────
def make_styles():
    s = getSampleStyleSheet()
    
    base = dict(fontName='Helvetica', textColor=hx(WHITE))
    
    styles = {
        'cover_eyebrow': ParagraphStyle('cover_eyebrow',
            fontName='Helvetica', fontSize=9, textColor=hx(ORANGE),
            spaceAfter=4, letterSpacing=2),
        'cover_title1': ParagraphStyle('cover_title1',
            fontName='Helvetica-Bold', fontSize=42, textColor=hx(WHITE),
            leading=46, spaceAfter=0),
        'cover_title2': ParagraphStyle('cover_title2',
            fontName='Helvetica-Bold', fontSize=42, textColor=hx(ORANGE),
            leading=46, spaceAfter=16),
        'cover_subtitle': ParagraphStyle('cover_subtitle',
            fontName='Helvetica', fontSize=13, textColor=hx(LIGHT_TXT),
            spaceAfter=6),
        'cover_stat_num': ParagraphStyle('cover_stat_num',
            fontName='Helvetica-Bold', fontSize=28, textColor=hx(ORANGE),
            spaceAfter=2, leading=32),
        'cover_stat_label': ParagraphStyle('cover_stat_label',
            fontName='Helvetica', fontSize=9, textColor=hx(LIGHT_TXT),
            spaceAfter=0),
        'cover_meta_label': ParagraphStyle('cover_meta_label',
            fontName='Helvetica', fontSize=8, textColor=hx(LIGHT_TXT),
            spaceAfter=1),
        'cover_meta_value': ParagraphStyle('cover_meta_value',
            fontName='Helvetica-Bold', fontSize=10, textColor=hx(WHITE),
            spaceAfter=4),
        'section_badge': ParagraphStyle('section_badge',
            fontName='Helvetica-Bold', fontSize=8, textColor=hx(DARK_BG),
            backColor=hx(ORANGE), spaceAfter=4, spaceBefore=0,
            borderPad=3),
        'section_title': ParagraphStyle('section_title',
            fontName='Helvetica-Bold', fontSize=18, textColor=hx(WHITE),
            spaceAfter=8, spaceBefore=4),
        'subsection_num': ParagraphStyle('subsection_num',
            fontName='Helvetica-Bold', fontSize=20, textColor=hx(ORANGE),
            spaceAfter=0, leading=22),
        'subsection_title': ParagraphStyle('subsection_title',
            fontName='Helvetica-Bold', fontSize=14, textColor=hx(WHITE),
            spaceAfter=6, spaceBefore=2),
        'body': ParagraphStyle('body',
            fontName='Helvetica', fontSize=9.5, textColor=hx(LIGHT_TXT),
            spaceAfter=8, leading=14),
        'body_white': ParagraphStyle('body_white',
            fontName='Helvetica', fontSize=9.5, textColor=hx(WHITE),
            spaceAfter=6, leading=14),
        'highlight_box_title': ParagraphStyle('highlight_box_title',
            fontName='Helvetica-Bold', fontSize=10, textColor=hx(ORANGE),
            spaceAfter=4),
        'highlight_body': ParagraphStyle('highlight_body',
            fontName='Helvetica', fontSize=9, textColor=hx(WHITE),
            spaceAfter=3, leading=13),
        'bullet': ParagraphStyle('bullet',
            fontName='Helvetica', fontSize=9, textColor=hx(LIGHT_TXT),
            spaceAfter=3, leading=13, leftIndent=12, bulletIndent=0),
        'kpi_num': ParagraphStyle('kpi_num',
            fontName='Helvetica-Bold', fontSize=22, textColor=hx(ORANGE),
            spaceAfter=2, leading=26),
        'kpi_label': ParagraphStyle('kpi_label',
            fontName='Helvetica', fontSize=8, textColor=hx(LIGHT_TXT)),
        'insight_num': ParagraphStyle('insight_num',
            fontName='Helvetica-Bold', fontSize=11, textColor=hx(ORANGE),
            spaceAfter=1),
        'insight_title': ParagraphStyle('insight_title',
            fontName='Helvetica-Bold', fontSize=11, textColor=hx(WHITE),
            spaceAfter=3),
        'insight_body': ParagraphStyle('insight_body',
            fontName='Helvetica', fontSize=9, textColor=hx(LIGHT_TXT),
            spaceAfter=10, leading=13),
        'footer_txt': ParagraphStyle('footer_txt',
            fontName='Helvetica', fontSize=7.5, textColor=hx(LIGHT_TXT),
            spaceAfter=0),
        'tag': ParagraphStyle('tag',
            fontName='Helvetica-Bold', fontSize=8, textColor=hx(DARK_BG),
            spaceAfter=0, backColor=hx(ORANGE), borderPad=3),
        'closing_tag': ParagraphStyle('closing_tag',
            fontName='Helvetica-Bold', fontSize=36, textColor=hx(WHITE),
            spaceAfter=8, leading=44),
        'closing_tag2': ParagraphStyle('closing_tag2',
            fontName='Helvetica-BoldOblique', fontSize=36, textColor=hx(ORANGE),
            spaceAfter=16, leading=44),
    }
    return styles

# ─── TABLE STYLE ──────────────────────────────────────────────────────────────
def data_table_style(n_rows, highlight_row=None):
    """Build a TableStyle for data tables"""
    ts = TableStyle([
        # header
        ('BACKGROUND', (0,0), (-1,0), hx(ORANGE)),
        ('TEXTCOLOR',  (0,0), (-1,0), hx(DARK_BG)),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 9),
        ('ALIGN',      (0,0), (-1,0), 'CENTER'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [hx(DARK_ROW), hx(LIGHT_ROW)]),
        ('TEXTCOLOR',  (0,1), (-1,-1), hx(WHITE)),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,1), (-1,-1), 8.5),
        ('GRID',       (0,0), (-1,-1), 0.3, hx("#1A2A6A")),
        ('LINEABOVE',  (0,0), (-1,0), 0.5, hx(ORANGE)),
        ('LINEBELOW',  (0,-1), (-1,-1), 0.5, hx("#1A2A6A")),
    ])
    # highlight holaprime row (last row)
    ts.add('BACKGROUND', (0, n_rows), (-1, n_rows), hx("#0D1F44"))
    ts.add('FONTNAME',   (0, n_rows), (-1, n_rows), 'Helvetica-Bold')
    ts.add('TEXTCOLOR',  (0, n_rows), (0, n_rows), hx(GOLD))
    return ts

# ─── PAGE TEMPLATES ───────────────────────────────────────────────────────────
class PDFDoc:
    def __init__(self, output_path):
        self.output_path = output_path
        self.logo_path = download_logo()
        self.styles = make_styles()

    def header_footer(self, canvas_obj, doc):
        """Draw header and footer on every page (except cover/closing)"""
        canvas_obj.saveState()
        page_num = doc.page

        # Header bar
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.rect(0, PH - 35, PW, 35, fill=1, stroke=0)

        # Orange accent line under header
        canvas_obj.setStrokeColor(hx(ORANGE))
        canvas_obj.setLineWidth(1.5)
        canvas_obj.line(0, PH - 35, PW, PH - 35)

        # Logo in header
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                canvas_obj.drawImage(self.logo_path, 18, PH - 28, width=80, height=18,
                                     preserveAspectRatio=True, mask='auto')
            except:
                canvas_obj.setFillColor(hx(WHITE))
                canvas_obj.setFont('Helvetica-Bold', 10)
                canvas_obj.drawString(18, PH - 24, "growth-onomics")

        # Report title in header center
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 7.5)
        canvas_obj.drawCentredString(PW/2, PH - 22, "Share of Voice Analysis · holaprime")

        # Page number in header right
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.setFont('Helvetica-Bold', 11)
        canvas_obj.drawRightString(PW - 18, PH - 22, f"{page_num:02d}")

        # Footer
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.rect(0, 0, PW, 28, fill=1, stroke=0)
        canvas_obj.setStrokeColor(hx("#1A2A6A"))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(0, 28, PW, 28)

        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 7)
        canvas_obj.drawString(18, 10, "CY: +357 7000 1372 · mg@growth-onomics.com · www.growth-onomics.com")
        canvas_obj.drawRightString(PW - 18, 10, "Confidential")

        canvas_obj.restoreState()

    def cover_page_draw(self, canvas_obj, doc):
        """Draw the cover page (no standard header/footer)"""
        canvas_obj.saveState()

        # Full dark background
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.rect(0, 0, PW, PH, fill=1, stroke=0)

        # Decorative top accent bar
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.rect(0, PH - 6, PW, 6, fill=1, stroke=0)

        # Decorative side accent
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.rect(0, 0, 4, PH, fill=1, stroke=0)

        # Subtle grid pattern in background
        canvas_obj.setStrokeColor(hx("#0A1550"))
        canvas_obj.setLineWidth(0.3)
        for i in range(0, int(PW), 40):
            canvas_obj.line(i, 0, i, PH)
        for j in range(0, int(PH), 40):
            canvas_obj.line(0, j, PW, j)

        # Logo top left
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                canvas_obj.drawImage(self.logo_path, 30, PH - 60, width=110, height=30,
                                     preserveAspectRatio=True, mask='auto')
            except:
                canvas_obj.setFillColor(hx(WHITE))
                canvas_obj.setFont('Helvetica-Bold', 14)
                canvas_obj.drawString(30, PH - 50, "growth-onomics")

        # "Strategic Intelligence Division" label
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawString(30, PH - 68, "Strategic Intelligence Division")

        # CONFIDENTIAL badge
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.roundRect(PW - 115, PH - 62, 85, 18, 3, fill=1, stroke=0)
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.setFont('Helvetica-Bold', 8)
        canvas_obj.drawCentredString(PW - 72, PH - 51, "CONFIDENTIAL")

        # Eyebrow text
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawString(30, PH - 115, "Competitive Intelligence Report  ·  February 2026")

        # Accent line
        canvas_obj.setStrokeColor(hx(ORANGE))
        canvas_obj.setLineWidth(2)
        canvas_obj.line(30, PH - 120, 30 + 280, PH - 120)

        # Main Title
        canvas_obj.setFillColor(hx(WHITE))
        canvas_obj.setFont('Helvetica-Bold', 44)
        canvas_obj.drawString(30, PH - 175, "Share of Voice")
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.setFont('Helvetica-Bold', 44)
        canvas_obj.drawString(30, PH - 225, "Analysis Report")

        # Subtitle
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 13)
        canvas_obj.drawString(30, PH - 255, "holaprime vs Competitor Prop Firms")
        canvas_obj.setFont('Helvetica', 11)
        canvas_obj.drawString(30, PH - 272, "Analysis Period: January 18 – February 18, 2026")

        # ─ Stats row ─────────────────────────────────
        # Dark card backgrounds
        card_y = PH - 355
        card_h = 70
        stats = [
            ("20,194", "Total Market Mentions", 30),
            ("38.4M", "Total Market Reach", 185),
            ("32", "Days Analysed", 340),
        ]
        for num, label, x in stats:
            canvas_obj.setFillColor(hx(DARK_ROW))
            canvas_obj.roundRect(x, card_y, 140, card_h, 5, fill=1, stroke=0)
            canvas_obj.setFillColor(hx(ORANGE))
            canvas_obj.setFont('Helvetica-Bold', 24)
            canvas_obj.drawString(x + 12, card_y + 38, num)
            canvas_obj.setFillColor(hx(LIGHT_TXT))
            canvas_obj.setFont('Helvetica', 8)
            canvas_obj.drawString(x + 12, card_y + 20, label)

        # ─ Metadata grid ─────────────────────────────
        meta_y = PH - 440
        meta_items = [
            ("Analysis Period", "Jan 18 – Feb 18, 2026"),
            ("Report Date", "February 2026"),
            ("Client Brand", "HolaPrime"),
            ("Prepared by", "Growth-onomics"),
        ]
        for i, (k, v) in enumerate(meta_items):
            col = i % 2
            row = i // 2
            x = 30 + col * 245
            y = meta_y - row * 45
            canvas_obj.setFillColor(hx(LIGHT_TXT))
            canvas_obj.setFont('Helvetica', 7.5)
            canvas_obj.drawString(x, y + 14, k)
            canvas_obj.setFillColor(hx(WHITE))
            canvas_obj.setFont('Helvetica-Bold', 10)
            canvas_obj.drawString(x, y, v)

        # ─ Competitive set ────────────────────────────
        cs_y = PH - 555
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawString(30, cs_y + 20, "Competitive Set")
        brands_cs = ["holaprime", "FTMO", "Topstep", "fundednext", "E8 Markets"]
        x_cursor = 30
        for brand in brands_cs:
            bw = canvas_obj.stringWidth(brand, 'Helvetica-Bold', 9) + 16
            bg = hx(GOLD) if brand == "holaprime" else hx(DARK_ROW)
            fc = hx(DARK_BG) if brand == "holaprime" else hx(WHITE)
            canvas_obj.setFillColor(bg)
            canvas_obj.roundRect(x_cursor, cs_y - 5, bw, 20, 3, fill=1, stroke=0)
            canvas_obj.setFillColor(fc)
            canvas_obj.setFont('Helvetica-Bold', 9)
            canvas_obj.drawString(x_cursor + 8, cs_y + 2, brand)
            x_cursor += bw + 8

        # ─ Bottom contact footer ──────────────────────
        canvas_obj.setStrokeColor(hx("#1A2A6A"))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(30, 45, PW - 30, 45)
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 7.5)
        canvas_obj.drawString(30, 28, "CY: +357 7000 1372 · mg@growth-onomics.com · www.growth-onomics.com")
        canvas_obj.drawRightString(PW - 30, 28, "Confidential")

        # Orange bottom accent
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.rect(0, 0, PW, 4, fill=1, stroke=0)

        canvas_obj.restoreState()

    def closing_page_draw(self, canvas_obj, doc):
        """Draw the closing page"""
        canvas_obj.saveState()

        # Full dark background
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.rect(0, 0, PW, PH, fill=1, stroke=0)

        # Accents
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.rect(0, PH - 6, PW, 6, fill=1, stroke=0)
        canvas_obj.rect(0, 0, PW, 4, fill=1, stroke=0)
        canvas_obj.rect(0, 0, 4, PH, fill=1, stroke=0)

        # Grid pattern
        canvas_obj.setStrokeColor(hx("#0A1550"))
        canvas_obj.setLineWidth(0.3)
        for i in range(0, int(PW), 40):
            canvas_obj.line(i, 0, i, PH)
        for j in range(0, int(PH), 40):
            canvas_obj.line(0, j, PW, j)

        # Logo centered
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo_w = 130
                canvas_obj.drawImage(self.logo_path, (PW - logo_w)/2, PH/2 + 40,
                                     width=logo_w, height=36,
                                     preserveAspectRatio=True, mask='auto')
            except:
                pass

        canvas_obj.setFillColor(hx(WHITE))
        canvas_obj.setFont('Helvetica-Bold', 30)
        canvas_obj.drawCentredString(PW/2, PH/2 - 10, "With Data as Our Compass,")
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.setFont('Helvetica-BoldOblique', 30)
        canvas_obj.drawCentredString(PW/2, PH/2 - 50, "We Solve Growth.")

        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 10)
        canvas_obj.drawCentredString(PW/2, PH/2 - 80,
            "This report was prepared by Growth-onomics Strategic Intelligence Division")

        # Contact grid
        contacts = [
            ("Phone", "+357 7000 1372"),
            ("Email", "mg@growth-onomics.com"),
            ("Website", "growth-onomics.com"),
        ]
        cx_start = 60
        for i, (label, value) in enumerate(contacts):
            x = cx_start + i * 160
            y = PH/2 - 130
            canvas_obj.setFillColor(hx(DARK_ROW))
            canvas_obj.roundRect(x, y, 140, 50, 5, fill=1, stroke=0)
            canvas_obj.setFillColor(hx(ORANGE))
            canvas_obj.setFont('Helvetica', 7.5)
            canvas_obj.drawString(x + 10, y + 34, label)
            canvas_obj.setFillColor(hx(WHITE))
            canvas_obj.setFont('Helvetica-Bold', 9)
            canvas_obj.drawString(x + 10, y + 18, value)

        # Bottom attribution
        canvas_obj.setStrokeColor(hx("#1A2A6A"))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(30, 55, PW - 30, 55)
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 7.5)
        canvas_obj.drawCentredString(PW/2, 38,
            "Report prepared by Growth-onomics · Solonos 48, Nicosia, Cyprus · February 2026 · Confidential")

        # Header
        canvas_obj.setFillColor(hx(DARK_BG))
        canvas_obj.rect(0, PH - 35, PW, 35, fill=1, stroke=0)
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                canvas_obj.drawImage(self.logo_path, 18, PH - 28, width=80, height=18,
                                     preserveAspectRatio=True, mask='auto')
            except:
                pass
        canvas_obj.setFillColor(hx(LIGHT_TXT))
        canvas_obj.setFont('Helvetica', 7.5)
        canvas_obj.drawCentredString(PW/2, PH - 22, "Strategic Intelligence Division")
        canvas_obj.setFillColor(hx(ORANGE))
        canvas_obj.setFont('Helvetica-Bold', 11)
        canvas_obj.drawRightString(PW - 18, PH - 22, "06")
        canvas_obj.setStrokeColor(hx(ORANGE))
        canvas_obj.setLineWidth(1.5)
        canvas_obj.line(0, PH - 35, PW, PH - 35)

        canvas_obj.restoreState()

    # ─── BUILD STORY ──────────────────────────────────────────────────────────
    def build(self):
        S = self.styles
        story = []
        
        # Margin = 18mm top/bottom (but we draw header/footer manually),
        # so add spacers at top/bottom of each content page
        TOP_PAD = 40   # points after header
        BOT_PAD = 32   # points before footer

        # ══════════════════════════════════════════════════════════════════════
        # PAGE 2 — Section 1.1: Share of Voice by Mention Volume
        # ══════════════════════════════════════════════════════════════════════
        story.append(Spacer(1, TOP_PAD))

        # Section badge
        story.append(make_section_badge("Section 1"))
        story.append(Spacer(1, 4))
        story.append(Paragraph("Market Share Analysis: Volume &amp; Visibility", S['section_title']))
        story.append(HorizontalLine(PW - 36*mm, hx(ORANGE), 0.8))
        story.append(Spacer(1, 8))

        # 1.1 subsection
        row1 = Table([[Paragraph("1.1", S['subsection_num']),
                       Paragraph("Share of Voice by Mention Volume", S['subsection_title'])]],
                     colWidths=[28, None])
        row1.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(row1)
        story.append(Spacer(1, 4))

        story.append(Paragraph(
            "Out of <b>20,194 total mentions</b> captured across all digital channels during the "
            "32-day analysis period, the distribution reveals a highly competitive but uneven playing field.",
            S['body']))
        story.append(Spacer(1, 6))

        # Table 1.1
        t1_headers = ["Brand", "Mentions", "Share of Voice", "Position", "Gap to Leader", "MoM Trend"]
        t1_data = [t1_headers] + [
            ["FTMO",       "7,149", "35.4%", "Market Leader", "—",              "+8.8%"],
            ["Topstep",    "5,001", "24.8%", "Strong #2",     "−2,148 (−30%)",  "+94.1%"],
            ["fundednext", "4,861", "24.1%", "Close #3",      "−2,288 (−32%)",  "+28.6%"],
            ["E8 Markets", "2,561", "12.7%", "4th – Mid-tier","−4,588 (−64%)",  "+141.9%"],
            ["holaprime",  "334",   "1.7%",  "5th – Emerging","−6,815 (−95%)",  "+115.1%"],
        ]
        t1 = Table(t1_data, colWidths=[70, 52, 68, 90, 90, 65])
        t1.setStyle(data_table_style(5))
        # green MoM for holaprime
        t1.setStyle(TableStyle([('TEXTCOLOR', (5, 5), (5, 5), hx(GREEN))]))
        story.append(t1)
        story.append(Spacer(1, 10))

        # Bar chart — SoV by Mention Volume
        brands_sov = ["holaprime", "E8 Markets", "fundednext", "Topstep", "FTMO"]
        vals_sov = [1.7, 12.7, 24.1, 24.8, 35.4]
        fig_sov = make_horiz_bar_chart(brands_sov, vals_sov,
                                       "Share of Voice by Mention Volume (%)")
        buf_sov = fig_to_bytes(fig_sov)
        story.append(chart_to_image(buf_sov, PW - 36*mm, 160))
        story.append(Spacer(1, 8))

        # Highlight box
        hbox_data = [[
            Paragraph("▲ Market Concentration", S['highlight_box_title']),
            ""
        ],[
            Paragraph(
                "The top 3 players (FTMO, Topstep, fundednext) collectively command "
                "<b>84.3% of all online conversations</b>, leaving only 15.7% of the discussion space "
                "for emerging and mid-tier competitors. <b>holaprime is the fastest-growing brand</b> in this window.",
                S['highlight_body']),
            ""
        ]]
        hbox = Table(hbox_data, colWidths=[PW - 36*mm, 0])
        hbox.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), hx("#0A1550")),
            ('BOX', (0,0), (-1,-1), 1, hx(ORANGE)),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(hbox)
        story.append(Spacer(1, 8))

        # Challenges & Opportunities
        co_data = [[
            [Paragraph("⚠ Challenges", S['highlight_box_title']),
             Paragraph("• High barrier to entry in brand awareness", S['bullet']),
             Paragraph("• Established competitors have loyal communities", S['bullet']),
             Paragraph("• Significant investment required to compete on volume", S['bullet'])],
            [Paragraph("✦ Opportunities", S['highlight_box_title']),
             Paragraph("• Topstep shows 26.1% negative sentiment — audience is up for grabs", S['bullet']),
             Paragraph("• Fragmented 15.7% market share is contestable", S['bullet']),
             Paragraph("• Quality-over-quantity approach differentiates holaprime", S['bullet'])],
        ]]
        co_tbl = Table(co_data, colWidths=[(PW - 36*mm)/2 - 4, (PW - 36*mm)/2 - 4])
        co_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), hx("#0D1020")),
            ('BACKGROUND', (1,0), (1,-1), hx("#051A20")),
            ('BOX',      (0,0), (0,-1), 0.5, hx("#FF3928")),
            ('BOX',      (1,0), (1,-1), 0.5, hx(TEAL)),
            ('VALIGN',   (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ]))
        story.append(co_tbl)
        story.append(Spacer(1, BOT_PAD))
        story.append(PageBreak())

        # ══════════════════════════════════════════════════════════════════════
        # PAGE 3 — Section 1.2: Share of Voice by Reach & Amplification
        # ══════════════════════════════════════════════════════════════════════
        story.append(Spacer(1, TOP_PAD))

        row2 = Table([[Paragraph("1.2", S['subsection_num']),
                       Paragraph("Share of Voice by Reach &amp; Amplification", S['subsection_title'])]],
                     colWidths=[28, None])
        row2.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(row2)
        story.append(Spacer(1, 4))

        story.append(Paragraph(
            "While mention volume provides one dimension of market presence, reach metrics reveal the true "
            "amplification and audience impact of each brand's content. Total combined reach across all "
            "analysed prop firms reached <b>38,426,000 impressions</b> during the study period.",
            S['body']))
        story.append(Spacer(1, 6))

        # Table 1.2
        t2_headers = ["Brand", "Total Reach", "Reach SoV", "Reach / Mention", "Efficiency Rank", "Reach Growth MoM"]
        t2_data = [t2_headers] + [
            ["FTMO",       "15.9M", "41.4%", "2,225", "3rd", "+27.1%"],
            ["Topstep",    "11.4M", "29.7%", "2,280", "2nd", "+193.1%"],
            ["fundednext",  "9.4M", "24.5%", "1,934", "4th", "+18.6%"],
            ["E8 Markets",  "1.4M",  "3.7%",   "562", "5th", "+140.4%"],
            ["holaprime",   "0.9M",  "2.2%", "2,583", "■ 1st", "+1,143.8%"],
        ]
        t2 = Table(t2_data, colWidths=[70, 55, 55, 65, 70, 75])
        t2.setStyle(data_table_style(5))
        # highlight rank 1 efficiency
        t2.setStyle(TableStyle([
            ('TEXTCOLOR', (4, 5), (4, 5), hx(GOLD)),
            ('FONTNAME',  (4, 5), (4, 5), 'Helvetica-Bold'),
            ('TEXTCOLOR', (5, 5), (5, 5), hx(GREEN)),
        ]))
        story.append(t2)
        story.append(Spacer(1, 10))

        # Bar chart — Reach SoV
        brands_reach = ["holaprime", "E8 Markets", "fundednext", "Topstep", "FTMO"]
        vals_reach = [2.2, 3.7, 24.5, 29.7, 41.4]
        fig_reach = make_horiz_bar_chart(brands_reach, vals_reach,
                                         "Reach Share of Voice (%)")
        buf_reach = fig_to_bytes(fig_reach)
        story.append(chart_to_image(buf_reach, PW - 36*mm, 160))
        story.append(Spacer(1, 8))

        # Critical Discovery highlight box
        cd_data = [[
            Paragraph("★ Critical Discovery — The Reach Efficiency Advantage", S['highlight_box_title']),
        ],[
            Paragraph(
                "Despite ranking last in absolute mention volume, "
                "<b>holaprime achieves the highest reach efficiency in the entire competitive set "
                "at 2,583 impressions per mention</b> — outperforming even market leader FTMO by 16.1%.",
                S['highlight_body']),
        ]]
        cd_tbl = Table(cd_data, colWidths=[PW - 36*mm])
        cd_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), hx("#0A1550")),
            ('LINEABOVE', (0,0), (-1,0), 2, hx(GOLD)),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(cd_tbl)
        story.append(Spacer(1, 10))

        # Efficiency comparison bullets
        eff_data = [
            [Paragraph("<b>+16.5%</b> more efficient than Topstep (2,583 vs 2,280)", S['highlight_body'])],
            [Paragraph("<b>+33.6%</b> more efficient than fundednext (2,583 vs 1,934)", S['highlight_body'])],
            [Paragraph("<b>+359.6%</b> more efficient than E8 Markets (2,583 vs 562)", S['highlight_body'])],
            [Paragraph("<b>+16.1%</b> more efficient than FTMO (2,583 vs 2,225)", S['highlight_body'])],
        ]
        eff_tbl = Table(eff_data, colWidths=[PW - 36*mm])
        eff_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), hx(DARK_ROW)),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [hx(DARK_ROW), hx(LIGHT_ROW)]),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('LINEAFTER', (0,0), (0,-1), 2, hx(GOLD)),
        ]))
        story.append(eff_tbl)
        story.append(Spacer(1, BOT_PAD))
        story.append(PageBreak())

        # ══════════════════════════════════════════════════════════════════════
        # PAGE 4 — Section 2: Month-over-Month Growth Analysis
        # ══════════════════════════════════════════════════════════════════════
        story.append(Spacer(1, TOP_PAD))

        story.append(make_section_badge("Section 2"))
        story.append(Spacer(1, 4))
        story.append(Paragraph("Month-over-Month Growth Analysis", S['section_title']))
        story.append(HorizontalLine(PW - 36*mm, hx(ORANGE), 0.8))
        story.append(Spacer(1, 6))

        story.append(Paragraph(
            "Tracking growth momentum across the 32-day period reveals a clear divergence: while "
            "established players show steady or moderate growth, holaprime and E8 Markets are the breakout "
            "stories. The two charts below separate mention volume growth from reach growth to give each "
            "metric appropriate scale.",
            S['body']))
        story.append(Paragraph(
            "<i>Note: Reach Growth chart uses a logarithmic scale. holaprime's +1,143.8% reach growth "
            "would make all other bars invisible on a linear scale.</i>",
            S['bullet']))
        story.append(Spacer(1, 8))

        # Growth Summary Table
        story.append(Paragraph("Growth Summary Table", S['subsection_title']))
        story.append(Spacer(1, 4))

        t3_headers = ["Brand", "Jan Mentions", "Feb Mentions", "Volume Growth", "Jan Reach", "Feb Reach", "Reach Growth"]
        t3_data = [t3_headers] + [
            ["FTMO",       "6,570", "579",   "+8.8%",    "12.51M", "3.39M", "+27.1%"],
            ["Topstep",    "2,576", "2,425", "+94.1%",   "3.89M",  "7.51M", "+193.1%"],
            ["fundednext", "3,779", "1,082", "+28.6%",   "7.93M",  "1.47M", "+18.6%"],
            ["E8 Markets", "1,058", "1,503", "+141.9%",  "0.60M",  "0.84M", "+140.4%"],
            ["holaprime",  "155",   "179",   "+115.1%",  "0.07M",  "0.79M", "+1,143.8%"],
        ]
        t3 = Table(t3_data, colWidths=[70, 52, 52, 55, 52, 52, 57])
        t3.setStyle(data_table_style(5))
        t3.setStyle(TableStyle([
            ('TEXTCOLOR', (3, 5), (3, 5), hx(GREEN)),
            ('TEXTCOLOR', (6, 5), (6, 5), hx(GOLD)),
            ('FONTNAME',  (6, 5), (6, 5), 'Helvetica-Bold'),
        ]))
        story.append(t3)
        story.append(Spacer(1, 10))

        # Two charts side by side: Volume Growth & Reach Growth (log)
        brands_g = ["FTMO", "Topstep", "fundednext", "E8 Markets", "holaprime"]
        vol_growth = [8.8, 94.1, 28.6, 141.9, 115.1]
        reach_growth = [27.1, 193.1, 18.6, 140.4, 1143.8]

        fig_vg = make_growth_bar_chart(brands_g, vol_growth, "Volume Growth MoM (%)", width_in=3.5, height_in=2.8)
        buf_vg = fig_to_bytes(fig_vg)

        fig_rg = make_reach_growth_log_chart(brands_g, reach_growth, "Reach Growth MoM (log scale)", width_in=3.5, height_in=2.8)
        buf_rg = fig_to_bytes(fig_rg)

        half_w = (PW - 36*mm) / 2 - 4
        charts_tbl = Table([[
            chart_to_image(buf_vg, half_w, 170),
            chart_to_image(buf_rg, half_w, 170),
        ]], colWidths=[half_w + 4, half_w + 4])
        charts_tbl.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
        story.append(charts_tbl)
        story.append(Spacer(1, 8))

        # Key Takeaway box
        kt_data = [[
            Paragraph("▲ Key Takeaway", S['highlight_box_title']),
        ],[
            Paragraph(
                "<b>holaprime's reach growth of +1,143.8% MoM</b> is the standout metric of the analysis "
                "period. Combined with +115.1% volume growth, this represents asymmetric momentum — a clear "
                "signal of accelerating brand awareness heading into Q1 2026.",
                S['highlight_body']),
        ]]
        kt_tbl = Table(kt_data, colWidths=[PW - 36*mm])
        kt_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), hx("#051A20")),
            ('LINEABOVE', (0,0), (-1,0), 2, hx(TEAL)),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(kt_tbl)
        story.append(Spacer(1, BOT_PAD))
        story.append(PageBreak())

        # ══════════════════════════════════════════════════════════════════════
        # PAGE 5 — Section 3: Market Share Distribution + Section 4: Key Insights
        # ══════════════════════════════════════════════════════════════════════
        story.append(Spacer(1, TOP_PAD))

        story.append(make_section_badge("Section 3"))
        story.append(Spacer(1, 4))
        story.append(Paragraph("Market Share Distribution Overview", S['section_title']))
        story.append(HorizontalLine(PW - 36*mm, hx(ORANGE), 0.8))
        story.append(Spacer(1, 5))

        story.append(Paragraph(
            "The charts below visualize the competitive landscape from a proportional perspective — comparing "
            "each brand's slice of total mentions against its slice of total reach. The gap between "
            "holaprime's mention share (1.7%) and reach share (2.2%) highlights its above-average content amplification.",
            S['body']))
        story.append(Spacer(1, 6))

        # Distribution table
        t4_headers = ["Brand", "Mention Share", "Reach Share", "Reach vs Mention Gap", "Interpretation"]
        t4_data = [t4_headers] + [
            ["FTMO",       "35.4%", "41.4%", "+6.0pp",  "Above-avg amplification"],
            ["Topstep",    "24.8%", "29.7%", "+4.9pp",  "Above-avg amplification"],
            ["fundednext", "24.1%", "24.5%", "+0.4pp",  "Average amplification"],
            ["E8 Markets", "12.7%",  "3.7%", "−9.0pp",  "Below-avg amplification"],
            ["holaprime",   "1.7%",  "2.2%", "+0.5pp",  "Punching above weight ✓"],
        ]
        t4 = Table(t4_data, colWidths=[70, 62, 58, 80, 120])
        t4.setStyle(data_table_style(5))
        t4.setStyle(TableStyle([
            ('TEXTCOLOR', (4, 5), (4, 5), hx(GOLD)),
            ('FONTNAME',  (4, 5), (4, 5), 'Helvetica-Bold'),
        ]))
        story.append(t4)
        story.append(Spacer(1, 10))

        # Two pie charts side by side
        brands_pie = ["FTMO", "Topstep", "fundednext", "E8 Markets", "holaprime"]
        mention_vals = [35.4, 24.8, 24.1, 12.7, 1.7]  # → sums to ~98.7, close enough
        # normalize
        mt = sum(mention_vals)
        mention_pct = [v/mt*100 for v in mention_vals]

        reach_vals = [41.4, 29.7, 24.5, 3.7, 2.2]
        rt = sum(reach_vals)
        reach_pct = [v/rt*100 for v in reach_vals]

        fig_pie1 = make_pie_chart(brands_pie, mention_pct, "Mention Share of Voice", 3.3, 3.3)
        buf_pie1 = fig_to_bytes(fig_pie1)
        fig_pie2 = make_pie_chart(brands_pie, reach_pct, "Reach Share of Voice", 3.3, 3.3)
        buf_pie2 = fig_to_bytes(fig_pie2)

        pie_w = (PW - 36*mm) / 2 - 4
        pies_tbl = Table([[
            chart_to_image(buf_pie1, pie_w, 185),
            chart_to_image(buf_pie2, pie_w, 185),
        ]], colWidths=[pie_w + 4, pie_w + 4])
        pies_tbl.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(pies_tbl)
        story.append(Spacer(1, 10))

        # ─── Section 4 header ────────────────────────────────────────────────
        story.append(make_section_badge("Section 4"))
        story.append(Spacer(1, 4))
        story.append(Paragraph("Key Insights &amp; Strategic Implications", S['section_title']))
        story.append(HorizontalLine(PW - 36*mm, hx(ORANGE), 0.8))
        story.append(Spacer(1, 6))

        # 4 insights in 2x2 grid
        insights = [
            ("4.1", "Market Concentration Risk",
             "The top 3 players control <b>84.3% of conversations</b> — a high barrier to entry for brand "
             "awareness. However, this also means the fragmented 15.7% tail is highly contestable, and "
             "holaprime's superior content efficiency gives it a structural edge in capturing quality "
             "impressions at scale."),
            ("4.2", "holaprime's Growth Trajectory",
             "With <b>+115.1% MoM volume growth</b> and <b>+1,143.8% MoM reach growth</b>, holaprime is "
             "the fastest-growing brand in the competitive set on both dimensions. This asymmetric growth "
             "is a leading indicator of accelerating brand awareness heading into Q1 2026."),
            ("4.3", "Quality-Over-Quantity Strategy",
             "holaprime's reach efficiency (<b>#1 at 2,583 impressions/mention</b>) indicates high-quality "
             "content placements in high-authority channels. Scaling content output while maintaining this "
             "quality standard will compound the reach advantage rapidly as volume increases."),
            ("4.4", "Competitive Vulnerability Windows",
             "<b>Topstep shows 26.1% negative sentiment</b> in community discussions — a clear opportunity "
             "for holaprime to capture dissatisfied audiences. E8 Markets' volume surge (+141.9% MoM) "
             "signals an emerging near-term competitor that should be monitored closely."),
        ]

        insight_cells = []
        for num, title, body in insights:
            cell = [
                Paragraph(num, S['insight_num']),
                Paragraph(title, S['insight_title']),
                Paragraph(body, S['insight_body']),
            ]
            insight_cells.append(cell)

        half_c = (PW - 36*mm) / 2 - 4
        ins_tbl = Table([
            [insight_cells[0], insight_cells[1]],
            [insight_cells[2], insight_cells[3]],
        ], colWidths=[half_c + 4, half_c + 4])
        ins_tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), hx(DARK_ROW)),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [hx(DARK_ROW), hx(LIGHT_ROW)]),
                ('VALIGN',        (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('RIGHTPADDING',  (0,0), (-1,-1), 10),
            ('LINEBEFORE',    (0,0), (0,-1), 2, hx(ORANGE)),
            ('LINEBEFORE',    (1,0), (1,-1), 2, hx(TEAL)),
            ('GRID',          (0,0), (-1,-1), 0.3, hx("#1A2A6A")),
        ]))
        story.append(ins_tbl)
        story.append(Spacer(1, BOT_PAD))
        story.append(PageBreak())

        return story

    def generate(self):
        # Use a multi-page template with different first-page behavior
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            leftMargin=18*mm,
            rightMargin=18*mm,
            topMargin=38,   # below header
            bottomMargin=30, # above footer
            title="Share of Voice Analysis Report — holaprime",
            author="Growth-onomics Strategic Intelligence Division",
            subject="Competitive Intelligence",
            creator="Growth-onomics",
        )

        story = self.build()

        # Build with cover page as page 1 (drawn in onFirstPage),
        # and header/footer on subsequent pages
        # We insert a cover page by using a "page template" switch.
        # Simpler: draw it manually via onFirstPage.

        page_count = [0]

        def on_page(canvas_obj, doc_obj):
            page_count[0] = doc_obj.page
            if doc_obj.page == 1:
                self.cover_page_draw(canvas_obj, doc_obj)
            else:
                # Dark background on content pages (drawn before content)
                canvas_obj.saveState()
                canvas_obj.setFillColor(hx(DARK_BG))
                canvas_obj.rect(0, 0, PW, PH, fill=1, stroke=0)
                canvas_obj.restoreState()
                self.header_footer(canvas_obj, doc_obj)

        def on_later_pages(canvas_obj, doc_obj):
            # Check if last page (closing page)
            pass

        # Insert cover spacer to push content to page 2
        # Cover page is drawn entirely via onFirstPage callback.
        # We just need a tiny placeholder + PageBreak to advance past page 1.
        full_story = [Spacer(1, 1), PageBreak()] + story

        doc.build(full_story, onFirstPage=on_page, onLaterPages=on_page)

        # Post-process: add closing page
        self._add_closing_page()

        print(f"PDF generated: {self.output_path}")

    def _add_closing_page(self):
        """Append a closing page to the existing PDF"""
        from reportlab.pdfgen import canvas as pdfgen_canvas
        from pypdf import PdfWriter, PdfReader
        import tempfile

        # Create closing page
        tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        tmp_path = tmp.name
        tmp.close()

        c = pdfgen_canvas.Canvas(tmp_path, pagesize=A4)
        # Create a temporary doc object with page=6
        class FakeDoc:
            page = 6
        self.closing_page_draw(c, FakeDoc())
        c.save()

        # Merge
        writer = PdfWriter()
        reader_main = PdfReader(self.output_path)
        reader_closing = PdfReader(tmp_path)

        for page in reader_main.pages:
            writer.add_page(page)
        for page in reader_closing.pages:
            writer.add_page(page)

        with open(self.output_path, 'wb') as f:
            writer.write(f)

        os.unlink(tmp_path)
        print(f"Closing page appended. Final PDF: {self.output_path}")


if __name__ == '__main__':
    output = '/Users/milton/clawd/holaprime-sov-growthonomics.pdf'
    doc = PDFDoc(output)
    doc.generate()
    print(f"\nDone! Output: {output}")
