import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, FrameBreak, 
                                NextPageTemplate, KeepInFrame, Paragraph, Spacer, 
                                Table, TableStyle, Image)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import HRFlowable

# Font Tanımlamaları ve Cloud Optimizasyonu (Hata Yakalama)
try:
    pdfmetrics.registerFont(TTFont("Montserrat", "fonts/Montserrat-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Montserrat-Bold", "fonts/Montserrat-Bold.ttf"))
    FONT_NORMAL = "Montserrat"
    FONT_BOLD = "Montserrat-Bold"
except Exception:
    # Eğer fonts klasörü buluta yüklenmezse uygulama çökmesin diye standart fonta döner.
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

def line(spaceBefore=4, spaceAfter=8, color="#2C3E50", thickness=1.0):
    return HRFlowable(
        width="100%",
        thickness=thickness,
        lineCap='round',
        color=colors.HexColor(color),
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter
    )

def icon_text_row(icon_path, text, style, icon_size=12, padding=5):
    if os.path.exists(icon_path):
        try:
            img = Image(icon_path, width=icon_size, height=icon_size)
            table = Table(
                [[img, Paragraph(text, style)]],
                colWidths=[icon_size + padding, None],
                style=TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ])
            )
            return table
        except Exception:
            pass
    return Paragraph(text, style)

def parse_text_to_flowables(text, style_normal, bullet_style):
    if not text:
        return []
    flowables = []
    lines = str(text).split('\n')
    for line_str in lines:
        clean_line = line_str.strip()
        if not clean_line:
            flowables.append(Spacer(1, 4))
            continue
        if clean_line.startswith('- ') or clean_line.startswith('* '):
            content = clean_line[2:]
            flowables.append(Paragraph(f"<bullet>&bull;</bullet> {content}", bullet_style))
        else:
            flowables.append(Paragraph(clean_line, style_normal))
    return flowables

def create_block(title, flowables_list, theme_color, style_bold):
    if not flowables_list:
        return []
    block = []
    block.append(Paragraph(title, style_bold))
    block.append(line(color=theme_color, spaceBefore=2, spaceAfter=8, thickness=1.5))
    block.extend(flowables_list)
    block.append(Spacer(1, 15))
    return block

def format_smart_link(text, link_type):
    if not text: return ""
    text = text.strip()
    color = "#333333" 
    
    if link_type == "email":
        display = text
        if len(display) > 24:
            display = display[:21] + "..."
        return f'<a href="mailto:{text}"><font color="{color}">{display}</font></a>'
        
    elif link_type == "url":
        display = text.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
        if len(display) > 24:
            display = display[:21] + "..."
        url = text if text.startswith("http") else "https://" + text
        return f'<a href="{url}"><font color="{color}">{display}</font></a>'
        
    return text

def create_cv(data):
    buffer = io.BytesIO()
    
    # SAYFA VE FRAME (ÇERÇEVE) MİMARİSİ
    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN = 30
    HEADER_HEIGHT = 150
    LEFT_COL_WIDTH = 175
    
    theme_color = data.get("theme_color", "#000000")
    
    doc = BaseDocTemplate(
        buffer, 
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title=f"{data.get('name', 'CV')}_CV"
    )

    def draw_background(canvas, doc_obj):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor(theme_color))
        
        y_horizontal = PAGE_HEIGHT - MARGIN - HEADER_HEIGHT
        x_vertical = MARGIN + LEFT_COL_WIDTH
        
        if doc_obj.page == 1:
            canvas.setLineWidth(2.5)
            canvas.line(MARGIN, y_horizontal, PAGE_WIDTH - MARGIN, y_horizontal)
        
        canvas.setLineWidth(1.0)
        y_vertical_top = y_horizontal if doc_obj.page == 1 else PAGE_HEIGHT - MARGIN
        canvas.line(x_vertical, y_vertical_top, x_vertical, MARGIN)
        
        canvas.restoreState()

    frame_header = Frame(MARGIN, PAGE_HEIGHT - MARGIN - HEADER_HEIGHT, PAGE_WIDTH - 2*MARGIN, HEADER_HEIGHT, id='header', topPadding=0, bottomPadding=10, leftPadding=0, rightPadding=0)
    frame_left_1 = Frame(MARGIN, MARGIN, LEFT_COL_WIDTH, PAGE_HEIGHT - 2*MARGIN - HEADER_HEIGHT, id='left_1', rightPadding=20, topPadding=15, bottomPadding=0, leftPadding=0)
    frame_right_1 = Frame(MARGIN + LEFT_COL_WIDTH, MARGIN, PAGE_WIDTH - 2*MARGIN - LEFT_COL_WIDTH, PAGE_HEIGHT - 2*MARGIN - HEADER_HEIGHT, id='right_1', leftPadding=20, topPadding=15, bottomPadding=0, rightPadding=0)
    
    frame_right_2 = Frame(MARGIN + LEFT_COL_WIDTH, MARGIN, PAGE_WIDTH - 2*MARGIN - LEFT_COL_WIDTH, PAGE_HEIGHT - 2*MARGIN, id='right_2', leftPadding=20, topPadding=0, bottomPadding=0, rightPadding=0)

    page_1_template = PageTemplate(id='Page1', frames=[frame_header, frame_left_1, frame_right_1], onPage=draw_background)
    page_2_template = PageTemplate(id='Page2', frames=[frame_right_2], onPage=draw_background)
    doc.addPageTemplates([page_1_template, page_2_template])

    # STİLLER (Font Değişkenlerine Bağlandı)
    styles = getSampleStyleSheet()
    
    style_normal = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=10, leading=14, spaceAfter=5)
    style_contact = ParagraphStyle('ContactStyle', parent=style_normal, fontSize=9, leading=14)
    style_bullet = ParagraphStyle('BulletStyle', parent=style_normal, leftIndent=12, bulletIndent=0, spaceAfter=4)
    style_bold = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=13, textColor=colors.HexColor(theme_color), spaceBefore=10, spaceAfter=2, textTransform='uppercase')
    
    style_header_name = ParagraphStyle('HeaderName', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=32, leading=34, spaceAfter=6, textColor=colors.HexColor(theme_color))
    style_header_title = ParagraphStyle('HeaderTitle', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=16, leading=18, textColor=colors.HexColor("#777777"), textTransform='uppercase', spaceAfter=10)

    # İÇERİK OLUŞTURMA
    story = []

    # 1. BAŞLIK (HEADER)
    header_flowables = []
    header_text_items = [
        Paragraph(data.get("name", ""), style_header_name),
        Paragraph(data.get("title", ""), style_header_title)
    ]
    if data.get("photo"):
        try:
            profile_pic = Image(io.BytesIO(data["photo"]), width=100, height=100)
            header_table = Table([[header_text_items, profile_pic]], colWidths=[435, 100], style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ALIGN', (1, 0), (1, 0), 'RIGHT'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)
            ]))
            header_flowables.append(header_table)
        except Exception:
            header_flowables.extend(header_text_items)
    else:
        header_flowables.extend(header_text_items)

    story.extend(header_flowables)
    story.append(FrameBreak()) 

    # 2. SOL KOLON
    left_col_items = []
    contact_flowables = []
    
    val_phone = data.get("telephone")
    if val_phone and val_phone.strip():
        contact_flowables.append(icon_text_row("icons/telefon.png", f"<b>Telefon:</b> {format_smart_link(val_phone, 'text')}", style_contact))

    val_address = data.get("address")
    if val_address and val_address.strip():
        contact_flowables.append(icon_text_row("icons/konum.png", f"<b>Konum:</b> {format_smart_link(val_address, 'text')}", style_contact))

    val_email = data.get("email")
    if val_email and val_email.strip():
        contact_flowables.append(icon_text_row("icons/eposta.png", f"<b>E-posta:</b> {format_smart_link(val_email, 'email')}", style_contact))

    if data.get("socials"):
        for platform, link in data["socials"]:
            if platform and link:
                icon_path = f"icons/{platform.lower().replace(' ', '')}.png"
                contact_flowables.append(icon_text_row(icon_path, f"<b>{platform.capitalize()}:</b> {format_smart_link(link, 'url')}", style_contact))
                
    if contact_flowables:
        left_col_items.extend(create_block("İLETİŞİM", contact_flowables, theme_color, style_bold))

    if data.get("skills") and data["skills"].strip():
        left_col_items.extend(create_block("YETENEKLER", parse_text_to_flowables(data["skills"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("languages") and data["languages"].strip():
        left_col_items.extend(create_block("DİLLER", parse_text_to_flowables(data["languages"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("references") and data["references"].strip():
        left_col_items.extend(create_block("REFERANSLAR", parse_text_to_flowables(data["references"], style_normal, style_bullet), theme_color, style_bold))

    if left_col_items:
        story.append(KeepInFrame(LEFT_COL_WIDTH, PAGE_HEIGHT - 2*MARGIN - HEADER_HEIGHT, left_col_items, mode='shrink'))
    
    story.append(FrameBreak()) 

    # 3. SAĞ KOLON
    story.append(NextPageTemplate('Page2')) 
    
    right_col_items = []
    if data.get("about") and data["about"].strip():
        right_col_items.extend(create_block("HAKKIMDA", parse_text_to_flowables(data["about"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("experience") and data["experience"].strip():
        right_col_items.extend(create_block("DENEYİM", parse_text_to_flowables(data["experience"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("education") and data["education"].strip():
        right_col_items.extend(create_block("EĞİTİM", parse_text_to_flowables(data["education"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("custom_1_text") and data["custom_1_text"].strip():
        right_col_items.extend(create_block(data.get("custom_1_title", "ÖZEL ALAN 1"), parse_text_to_flowables(data["custom_1_text"], style_normal, style_bullet), theme_color, style_bold))
    if data.get("custom_2_text") and data["custom_2_text"].strip():
        right_col_items.extend(create_block(data.get("custom_2_title", "ÖZEL ALAN 2"), parse_text_to_flowables(data["custom_2_text"], style_normal, style_bullet), theme_color, style_bold))

    story.extend(right_col_items)

    doc.build(story)
    buffer.seek(0)
    return buffer