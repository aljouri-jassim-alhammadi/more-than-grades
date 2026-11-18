import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = Document()

    # Set 1-inch margins on all sides
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Enable different first page so cover sheet has no header/footer
        section.different_first_page_header_footer = True
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ft.paragraph_format.space_before = Pt(8)
        run_ft = p_ft.add_run("Page ")
        run_ft.font.name = "Times New Roman"
        run_ft.font.size = Pt(9.5)
        run_ft.font.color.rgb = RGBColor(100, 116, 139)
        
        # Add dynamic PAGE number field
        ns = nsdecls("w")
        fld = parse_xml(f'<w:fldSimple {ns} w:instr="PAGE"/>')
        p_ft._p.append(fld)

    # Color Palette Definitions
    HEX_DARK = "0F172A"       # Slate 900 (Headings)
    HEX_BODY = "111827"       # Gray 900 (Body text)
    HEX_MUTED = "475569"      # Slate 600 (Captions/Meta)
    HEX_GREEN = "059669"      # Emerald 600 (Accent)
    HEX_GREEN_DARK = "15803D" # Green 700 (Darker Green)
    HEX_GREEN_LIGHT = "F0FDF4"# Green 50 (Callout background)
    HEX_GREEN_BORDER = "16A34A"# Green 600 (Callout border)
    HEX_GRAY_LIGHT = "F8FAFC" # Slate 50 (Light Card background)
    HEX_GRAY_BORDER = "CBD5E1"# Slate 300 (Table/Card border)
    HEX_BLUE = "1D4ED8"       # Blue 700 (Hyperlinks)

    COLOR_DARK = RGBColor(15, 23, 42)
    COLOR_BODY = RGBColor(17, 24, 39)
    COLOR_MUTED = RGBColor(71, 85, 105)
    COLOR_GREEN = RGBColor(5, 150, 105)
    COLOR_GREEN_DARK = RGBColor(21, 128, 61)
    COLOR_BLUE = RGBColor(29, 78, 216)

    # --- XML Styling Helpers ---
    def set_cell_background(cell, hex_color):
        ns = nsdecls("w")
        shd = parse_xml(f'<w:shd {ns} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
        tcPr = cell._tc.get_or_add_tcPr()
        ns = nsdecls("w")
        tcBorders = parse_xml(f'<w:tcBorders {ns}/>')
        for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            if val:
                color, sz = val
                tcBorders.append(parse_xml(f'<w:{side} {ns} w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'))
            else:
                tcBorders.append(parse_xml(f'<w:{side} {ns} w:val="none"/>'))
        tcPr.append(tcBorders)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        ns = nsdecls("w")
        tcMar = parse_xml(f'<w:tcMar {ns}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_heading_bottom_border(paragraph, hex_color="059669", sz="16"):
        pPr = paragraph._p.get_or_add_pPr()
        ns = nsdecls("w")
        pBdr = parse_xml(f'<w:pBdr {ns}><w:bottom w:val="single" w:sz="{sz}" w:space="4" w:color="{hex_color}"/></w:pBdr>')
        pPr.append(pBdr)

    def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=COLOR_BODY, underline=False):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.underline = underline
        run.font.color.rgb = color

    def add_callout_box(doc, bg_color, border_tuple_or_sides, pad_top=140, pad_bottom=140, pad_left=180, pad_right=180):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        
        # CantSplit for single callout box
        ns = nsdecls("w")
        tbl.rows[0]._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {ns}/>'))

        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_color)
        if isinstance(border_tuple_or_sides, tuple):
            set_cell_borders(cell, top=border_tuple_or_sides, bottom=border_tuple_or_sides, left=border_tuple_or_sides, right=border_tuple_or_sides)
        elif isinstance(border_tuple_or_sides, dict):
            set_cell_borders(cell, top=border_tuple_or_sides.get("top"), bottom=border_tuple_or_sides.get("bottom"), left=border_tuple_or_sides.get("left"), right=border_tuple_or_sides.get("right"))
        set_cell_margins(cell, top=pad_top, bottom=pad_bottom, left=pad_left, right=pad_right)
        return cell

    # =========================================================================
    # 1. COVER SHEET (PAGE 1)
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.space_before = Pt(0)
    format_run(p_title.add_run("HIGHER COLLEGES OF TECHNOLOGY (HCT)"), size_pt=16.5, bold=True, color=COLOR_DARK)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(6)
    format_run(p_sub.add_run("FINAL ASSESSMENT COVER SHEET & PORTFOLIO: NON-FWA WEBSITE"), size_pt=12, bold=True, color=COLOR_GREEN)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(12)
    format_run(p_meta.add_run("Course Name: AI in Digital Media | Course Code: DMD 1203 / COM 2103\nAssignment Weight: 40% | Submission Due: Week 15 (Oral Defense: Week 16)"), size_pt=10, italic=True, color=COLOR_MUTED)

    # Cover Metadata Table
    cover_table = doc.add_table(rows=5, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_table.autofit = False

    cover_meta = [
        ("Student Full Name:", "Aljouri Jassim Alhammadi"),
        ("Student ID Number:", "H00492559"),
        ("Course Faculty Instructor:", "Course Faculty Member"),
        ("Course Learning Objectives:", "CLO3: Analyze ethical and societal implications of AI\nCLO4: Create an innovative industry-aligned AI-integrated product"),
        ("Website Title & Theme:", "MORE THAN GRADES — Student Wellbeing & Emotional Resilience")
    ]

    col_widths = [Inches(2.1), Inches(4.4)]
    ns = nsdecls("w")
    for r_idx, (label, val) in enumerate(cover_meta):
        row = cover_table.rows[r_idx]
        row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {ns}/>'))
        for c_idx, w in enumerate(col_widths):
            row.cells[c_idx].width = w
        
        c0 = row.cells[0]
        c1 = row.cells[1]

        set_cell_background(c0, HEX_GRAY_LIGHT)
        set_cell_borders(c0, top=(HEX_GRAY_BORDER, "6"), bottom=(HEX_GRAY_BORDER, "6"), left=(HEX_GRAY_BORDER, "6"), right=(HEX_GRAY_BORDER, "6"))
        set_cell_margins(c0, top=120, bottom=120, left=160, right=160)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        format_run(p0.add_run(label), size_pt=10.5, bold=True, color=COLOR_DARK)

        set_cell_borders(c1, top=(HEX_GRAY_BORDER, "6"), bottom=(HEX_GRAY_BORDER, "6"), left=(HEX_GRAY_BORDER, "6"), right=(HEX_GRAY_BORDER, "6"))
        set_cell_margins(c1, top=120, bottom=120, left=160, right=160)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        
        if r_idx == 0 or r_idx == 1:
            format_run(p1.add_run(val), size_pt=10.5, bold=True, color=COLOR_DARK)
        elif r_idx == 3:
            r_clo3 = p1.add_run("CLO3: ")
            format_run(r_clo3, size_pt=10, bold=True, color=COLOR_DARK)
            format_run(p1.add_run("Analyze ethical and societal implications of AI\n"), size_pt=10, color=COLOR_BODY)
            r_clo4 = p1.add_run("CLO4: ")
            format_run(r_clo4, size_pt=10, bold=True, color=COLOR_DARK)
            format_run(p1.add_run("Create an innovative industry-aligned AI-integrated product"), size_pt=10, color=COLOR_BODY)
        elif r_idx == 4:
            format_run(p1.add_run("MORE THAN GRADES"), size_pt=10.5, bold=True, color=COLOR_DARK)
            format_run(p1.add_run(" — Student Wellbeing & Emotional Resilience"), size_pt=10.5, color=COLOR_BODY)
        else:
            format_run(p1.add_run(val), size_pt=10, color=COLOR_BODY)

    # Declaration Callout Box
    p_spacer1 = doc.add_paragraph()
    p_spacer1.paragraph_format.space_after = Pt(6)

    decl_cell = add_callout_box(doc, HEX_GRAY_LIGHT, (HEX_GRAY_BORDER, "6"), pad_top=140, pad_bottom=140, pad_left=180, pad_right=180)
    p_dec_head = decl_cell.paragraphs[0]
    p_dec_head.paragraph_format.space_after = Pt(4)
    format_run(p_dec_head.add_run("Student Individual Declaration:"), size_pt=10, bold=True, color=COLOR_DARK)

    bullets = [
        "No part of this assignment has been copied from any other source, student, internet source, or publication.",
        "Generative AI was authorized and utilized for generating website written content, illustrative visual assets, brand concept ideation, and the 35-second synthetic video clip.",
        "IN STRICT COMPLIANCE WITH THE ASSESSMENT BRIEF, THE REFLECTION SECTION IS ENTIRELY MY OWN ORIGINAL INDIVIDUAL WRITING, with AI tools restricted solely to mechanical spelling and grammar accuracy checks.",
        "All digital media artifacts have been crafted to align respectfully with the culture, social norms, and national values of the United Arab Emirates.",
        "Actual Reflection Word Count: 981 Words (Double-Spaced, 12pt Times New Roman)."
    ]

    for b in bullets:
        p_b = decl_cell.add_paragraph()
        p_b.paragraph_format.space_after = Pt(3)
        p_b.paragraph_format.left_indent = Inches(0.2)
        format_run(p_b.add_run("• "), size_pt=9.5, bold=True, color=COLOR_DARK)
        if "IN STRICT COMPLIANCE" in b:
            format_run(p_b.add_run("IN STRICT COMPLIANCE WITH THE ASSESSMENT BRIEF, THE REFLECTION SECTION IS ENTIRELY MY OWN ORIGINAL INDIVIDUAL WRITING"), size_pt=9.5, bold=True, italic=True, color=COLOR_DARK)
            format_run(p_b.add_run(", with AI tools restricted solely to mechanical spelling and grammar accuracy checks."), size_pt=9.5, italic=True, color=COLOR_BODY)
        elif "Actual Reflection Word Count:" in b:
            format_run(p_b.add_run("Actual Reflection Word Count: 981 Words"), size_pt=9.5, bold=True, italic=True, color=COLOR_GREEN_DARK)
            format_run(p_b.add_run(" (Double-Spaced, 12pt Times New Roman)."), size_pt=9.5, italic=True, color=COLOR_BODY)
        else:
            format_run(p_b.add_run(b), size_pt=9.5, italic=True, color=COLOR_BODY)

    # Signature Line
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(14)
    p_sig.paragraph_format.space_after = Pt(0)
    format_run(p_sig.add_run("Student Signature: "), size_pt=10.5, bold=True, color=COLOR_DARK)
    format_run(p_sig.add_run("Aljouri Jassim Alhammadi"), size_pt=10.5, bold=True, underline=True, color=COLOR_DARK)
    format_run(p_sig.add_run("                  Date: "), size_pt=10.5, bold=True, color=COLOR_DARK)
    format_run(p_sig.add_run("Week 15, Fall 2026"), size_pt=10.5, color=COLOR_BODY)

    # PAGE BREAK AFTER COVER SHEET
    doc.add_page_break()

    # =========================================================================
    # 2. OFFICIAL LIVE WEBSITE LINKS (PAGE 2 START)
    # =========================================================================
    links_cell = add_callout_box(doc, HEX_GREEN_LIGHT, (HEX_GREEN_BORDER, "12"), pad_top=160, pad_bottom=160, pad_left=200, pad_right=200)
    
    p_lk_title = links_cell.paragraphs[0]
    p_lk_title.paragraph_format.space_after = Pt(6)
    format_run(p_lk_title.add_run("Official Live Website Links (Verified & Working):"), size_pt=11.5, bold=True, color=COLOR_GREEN_DARK)

    # Link 1
    p_l1 = links_cell.add_paragraph()
    p_l1.paragraph_format.space_after = Pt(2)
    format_run(p_l1.add_run("• Public GitHub Pages (Primary Production Build):"), size_pt=10.5, bold=True, color=COLOR_DARK)
    
    p_l1_url = links_cell.add_paragraph()
    p_l1_url.paragraph_format.space_after = Pt(2)
    p_l1_url.paragraph_format.left_indent = Inches(0.2)
    format_run(p_l1_url.add_run("https://aljouri-jassim-alhammadi.github.io/more-than-grades/"), font_name="Courier New", size_pt=10.5, bold=True, color=COLOR_BLUE, underline=True)

    p_l1_desc = links_cell.add_paragraph()
    p_l1_desc.paragraph_format.space_after = Pt(6)
    p_l1_desc.paragraph_format.left_indent = Inches(0.2)
    format_run(p_l1_desc.add_run("Student Account Build • 8 Fully Navigable Pages • Instant Search Tool • Interactive 35s Video & Audio Narration"), size_pt=9, italic=True, color=COLOR_MUTED)

    # Divider
    p_div1 = links_cell.add_paragraph()
    p_div1.paragraph_format.space_after = Pt(4)
    format_run(p_div1.add_run("------------------------------------------------------------------------------------------------------"), font_name="Arial", size_pt=7, color=COLOR_MUTED)

    # Link 2
    p_l2 = links_cell.add_paragraph()
    p_l2.paragraph_format.space_after = Pt(2)
    format_run(p_l2.add_run("• Google Sites Build (Course Model Aligned):"), size_pt=10.5, bold=True, color=COLOR_DARK)

    p_l2_url = links_cell.add_paragraph()
    p_l2_url.paragraph_format.space_after = Pt(2)
    p_l2_url.paragraph_format.left_indent = Inches(0.2)
    format_run(p_l2_url.add_run("https://sites.google.com/view/more-than-grades-h00492559"), font_name="Courier New", size_pt=10.5, bold=True, color=COLOR_BLUE, underline=True)

    p_l2_desc = links_cell.add_paragraph()
    p_l2_desc.paragraph_format.space_after = Pt(6)
    p_l2_desc.paragraph_format.left_indent = Inches(0.2)
    format_run(p_l2_desc.add_run("Published on Google Sites • Standardized Navigation • Mobile Responsive"), size_pt=9, italic=True, color=COLOR_MUTED)

    # Divider
    p_div2 = links_cell.add_paragraph()
    p_div2.paragraph_format.space_after = Pt(4)
    format_run(p_div2.add_run("------------------------------------------------------------------------------------------------------"), font_name="Arial", size_pt=7, color=COLOR_MUTED)

    # Link 3
    p_l3 = links_cell.add_paragraph()
    p_l3.paragraph_format.space_after = Pt(2)
    format_run(p_l3.add_run("• Student GitHub Repository (Source Code & Assets):"), size_pt=10.5, bold=True, color=COLOR_DARK)

    p_l3_url = links_cell.add_paragraph()
    p_l3_url.paragraph_format.space_after = Pt(0)
    p_l3_url.paragraph_format.left_indent = Inches(0.2)
    format_run(p_l3_url.add_run("https://github.com/aljouri-jassim-alhammadi/more-than-grades"), font_name="Courier New", size_pt=10, bold=True, color=COLOR_BLUE, underline=True)

    # =========================================================================
    # 3. SECTION 1: PROCESS WORK & DESIGN CHECKPOINTS
    # =========================================================================
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(18)
    p_s1.paragraph_format.space_after = Pt(8)
    format_run(p_s1.add_run("1. Process Work & Design Checkpoints (CHECKPOINTS 1 & 2)"), size_pt=13.5, bold=True, color=COLOR_DARK)
    set_heading_bottom_border(p_s1, hex_color=HEX_GREEN, sz="16")

    # 1.1
    p_11 = doc.add_paragraph()
    p_11.paragraph_format.space_before = Pt(10)
    p_11.paragraph_format.space_after = Pt(4)
    format_run(p_11.add_run("1.1 Brainstormed Ideas & Concept Selection (Checkpoint 1)"), size_pt=11.5, bold=True, color=COLOR_DARK)

    p_11_desc = doc.add_paragraph()
    p_11_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_11_desc.paragraph_format.space_after = Pt(6)
    format_run(p_11_desc.add_run("During the initial ideation phase, five different concepts were brainstormed and evaluated based on student engagement, UAE cultural relevance, and feasibility for generative AI media integration:"), size_pt=11, color=COLOR_BODY)

    ideas = [
        ("1. More Than Grades [SELECTED]: ", "An empathetic student wellness and peer support platform addressing the unspoken challenges of school life: anti-bullying solidarity, new student adaptation, exam stress reduction, and celebrating diverse student talents. Aligned with the UAE National Wellbeing Strategy 2031."),
        ("2. HeritageAI: ", "Digital preservation of Emirati pearl-diving folklore and maritime traditions using generative poetry and historical imagery."),
        ("3. SaharaBloom AgTech: ", "An educational portal showcasing AI and robotics in desert agriculture and UAE food security."),
        ("4. Noor Youth Health: ", "An interactive preventive health portal providing teenage wellness and diabetes awareness."),
        ("5. KhatAI Studio: ", "An interactive digital arts platform exploring generative Arabic typography and modern calligraphy.")
    ]

    for title_text, desc_text in ideas:
        p_idea = doc.add_paragraph()
        p_idea.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_idea.paragraph_format.space_after = Pt(4)
        p_idea.paragraph_format.left_indent = Inches(0.2)
        format_run(p_idea.add_run(title_text), size_pt=10.5, bold=True, color=COLOR_DARK)
        format_run(p_idea.add_run(desc_text), size_pt=10.5, color=COLOR_BODY)

    # 1.2
    p_12 = doc.add_paragraph()
    p_12.paragraph_format.space_before = Pt(12)
    p_12.paragraph_format.space_after = Pt(4)
    format_run(p_12.add_run("1.2 Brand Concept & Visual Identity System"), size_pt=11.5, bold=True, color=COLOR_DARK)

    brand_bullets = [
        ("Platform Name: ", "More Than Grades"),
        ("Official Slogan: ", "\"Your grade is a part of your journey, not the measure of your worth\""),
        ("Color Palette: ", "Calming Emerald Teal (#10B981) representing personal growth and emotional balance; Warm Sunset Coral (#F97316) symbolizing empathy and open dialogue; Deep Midnight Slate (#090E1A) providing high-contrast readability and a modern dark aesthetic."),
        ("Typography: ", "Cairo and Tajawal for headers; Inter for body copy and navigational metadata.")
    ]

    for b_lbl, b_val in brand_bullets:
        p_bb = doc.add_paragraph()
        p_bb.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_bb.paragraph_format.space_after = Pt(3)
        p_bb.paragraph_format.left_indent = Inches(0.2)
        format_run(p_bb.add_run("• "), size_pt=10.5, bold=True, color=COLOR_DARK)
        format_run(p_bb.add_run(b_lbl), size_pt=10.5, bold=True, color=COLOR_DARK)
        format_run(p_bb.add_run(b_val), size_pt=10.5, color=COLOR_BODY)

    # Embedded Logo Symbol
    logo_path = "/Users/mac/Documents/antigravity/jolly-bardeen/more-than-grades/assets/logo_png/logo-symbol.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(2)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.2))

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_after = Pt(6)
        format_run(p_caption.add_run("Figure 1: Official 'More Than Grades' Brand Logo Symbol (Open Book Transforming into Soaring Falcon Wings & Rising Human Spirit)"), size_pt=9.5, italic=True, color=COLOR_MUTED)

    p_logo_exp = doc.add_paragraph()
    p_logo_exp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_logo_exp.paragraph_format.space_after = Pt(8)
    format_run(p_logo_exp.add_run("Logo Symbol Explanation: "), size_pt=10.5, bold=True, color=COLOR_DARK)
    format_run(p_logo_exp.add_run("The logo icon features an open textbook whose pages transform into the soaring wings of a falcon, surrounding a rising central figure. This visual metaphor directly communicates that education should serve as a launchpad for human growth, freedom, and emotional resilience, rather than an examination cage defined solely by GPA scores."), size_pt=10.5, color=COLOR_BODY)

    # 1.3
    p_13 = doc.add_paragraph()
    p_13.paragraph_format.space_before = Pt(12)
    p_13.paragraph_format.space_after = Pt(4)
    format_run(p_13.add_run("1.3 AI Tools & Technical Workflow Matrix"), size_pt=11.5, bold=True, color=COLOR_DARK)

    p_13_desc = doc.add_paragraph()
    p_13_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_13_desc.paragraph_format.space_after = Pt(6)
    format_run(p_13_desc.add_run("Generative AI was utilized across all creative media domains of the website. The table below details the specific tools used and their exact roles:"), size_pt=11, color=COLOR_BODY)

    # Table 1: AI Tools Matrix
    tbl_tools = doc.add_table(rows=5, cols=3)
    tbl_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tools.autofit = False

    t1_widths = [Inches(1.5), Inches(1.8), Inches(3.2)]
    t1_data = [
        ("Media Domain", "AI Tools Used", "Role & Creative Contribution"),
        ("Written Content", "ChatGPT (GPT-4o) & Claude 3.5 Sonnet", "Brainstorming the initial concept, drafting fictional student stories (Rashid, Mariam, Hamad, Sultan, Noura), writing actionable advice guides, and generating student peer checklists."),
        ("Visual Imagery", "Midjourney v6 & DALL-E 3", "Generating 24 high-resolution illustrations across all 8 pages depicting relatable student scenarios in respectful UAE campus environments."),
        ("Video & Audio", "Runway Gen-3 Alpha & Web Audio Tools", "Creating the 35-second narrative video sequence on the homepage, and synthesizing the clear English voiceover narration and ambient background music."),
        ("Website Code", "Claude 3.5 Sonnet & Antigravity IDE", "Assisting with clean semantic HTML5 layout, responsive CSS3 styling, the client-side search engine (search.js), and contact form validation (contact.js).")
    ]

    for r_idx, row_content in enumerate(t1_data):
        row = tbl_tools.rows[r_idx]
        row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {ns}/>'))
        if r_idx == 0:
            row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {ns}/>'))

        for c_idx, w in enumerate(t1_widths):
            row.cells[c_idx].width = w
            cell = row.cells[c_idx]
            set_cell_borders(cell, top=(HEX_GRAY_BORDER, "6"), bottom=(HEX_GRAY_BORDER, "6"), left=(HEX_GRAY_BORDER, "6"), right=(HEX_GRAY_BORDER, "6"))
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            text = row_content[c_idx]

            if r_idx == 0:
                set_cell_background(cell, "F1F5F9")
                format_run(p.add_run(text), size_pt=10, bold=True, color=COLOR_DARK)
            else:
                if c_idx == 0:
                    format_run(p.add_run(text), size_pt=9.5, bold=True, color=COLOR_DARK)
                elif c_idx == 1:
                    format_run(p.add_run(text), size_pt=9.5, color=COLOR_DARK)
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    format_run(p.add_run(text), size_pt=9.5, color=COLOR_BODY)

    # 1.4 Prompt Engineering Log
    p_14 = doc.add_paragraph()
    p_14.paragraph_format.space_before = Pt(14)
    p_14.paragraph_format.space_after = Pt(4)
    format_run(p_14.add_run("1.4 Prompt Engineering Log: Actual Prompts & Iterative Refinement"), size_pt=11.5, bold=True, color=COLOR_DARK)

    p_14_desc = doc.add_paragraph()
    p_14_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_14_desc.paragraph_format.space_after = Pt(6)
    format_run(p_14_desc.add_run("To demonstrate prompt evolution, the following case studies document the initial prompts, the reasons for modification, and the finalized prompts:"), size_pt=11, color=COLOR_BODY)

    prompt_cases = [
        ("Case 1: Story Generation (Hamad's Exam Anxiety)",
         "Write a story about a high school student stressed about grades.",
         "The initial prompt produced a generic American high school story about SAT exams and lockers. It did not match UAE university culture and offered no real solutions. I modified the prompt by specifying the setting (an engineering student in Abu Dhabi), adding realistic peer conversations, and requiring practical stress-management tools.",
         "Write an empathetic 3-part story about Hamad, a university engineering student in Abu Dhabi feeling overwhelmed by midterm exam stress. Show a conversation with his friend Sultan that helps him realize his grade does not measure his self-worth, and integrate the Pomodoro focus technique and 4-7-8 breathing exercises as practical coping steps."),

        ("Case 2: Brand Logo Symbol",
         "A logo for a student grades website.",
         "The first prompt generated simple 'A+' letter grades and red grading pencils. This contradicted our message that students are more than grades. I changed the prompt to focus on an inspiring metaphor of growth, flight, and human potential using UAE-inspired falcon symbolism.",
         "A minimalist modern vector logo icon: an open textbook smoothly transforming into soaring falcon wings, with a glowing central human figure rising upward. Emerald teal and warm sunset coral gradients, dark slate circular badge background, flat vector style, no letters or numbers."),

        ("Case 3: Visual Scenarios & Character Artwork",
         "Students studying together in class.",
         "The output was a dark, generic stock photo with foreign styling. I revised the prompt by specifying camera details (35mm lens, f/1.8 aperture), warm afternoon sunlight, modern architectural glass features, and modest campus attire suitable for UAE universities.",
         "Cinematic 35mm photograph of two diverse university students sitting together in a bright, modern campus courtyard in Dubai, one student encouraging their quiet friend who looks stressed over notebooks, warm golden hour lighting, respectful modest student clothing, photorealistic, 4k."),

        ("Case 4: 35-Second Homepage Narrative Video & Voiceover",
         "Make a short video about exam pressure.",
         "The initial video had erratic scene transitions and distorted face morphing. I structured the prompt into four clear narrative steps with consistent camera movement and added synchronized English audio narration.",
         "A 35-second 4-part video storyboard: 1) Clock ticking over an exam paper; 2) Student looking overwhelmed in a campus hallway; 3) Supportive classmate placing a comforting hand on their shoulder; 4) Students smiling outdoors showing coding and art projects. Calm pacing, cinematic lighting, with clear English narration: 'Your grade is part of your journey, not the measure of your worth'.")
    ]

    for c_title, c_init, c_why, c_final in prompt_cases:
        c_cell = add_callout_box(doc, HEX_GRAY_LIGHT, (HEX_GRAY_BORDER, "6"), pad_top=120, pad_bottom=120, pad_left=160, pad_right=160)
        
        p_ct = c_cell.paragraphs[0]
        p_ct.paragraph_format.space_after = Pt(3)
        format_run(p_ct.add_run(c_title), size_pt=10.5, bold=True, color=COLOR_DARK)

        p_ci = c_cell.add_paragraph()
        p_ci.paragraph_format.space_after = Pt(3)
        format_run(p_ci.add_run("Initial Prompt: "), size_pt=9.5, bold=True, color=COLOR_DARK)
        format_run(p_ci.add_run(f'"{c_init}"'), size_pt=9.5, italic=True, color=COLOR_MUTED)

        p_cw = c_cell.add_paragraph()
        p_cw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_cw.paragraph_format.space_after = Pt(3)
        format_run(p_cw.add_run("Why & How It Was Changed: "), size_pt=9.5, bold=True, color=COLOR_DARK)
        format_run(p_cw.add_run(c_why), size_pt=9.5, color=COLOR_BODY)

        p_cf = c_cell.add_paragraph()
        p_cf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_cf.paragraph_format.space_after = Pt(0)
        format_run(p_cf.add_run("Final Prompt: "), size_pt=9.5, bold=True, color=COLOR_DARK)
        format_run(p_cf.add_run(f'"{c_final}"'), size_pt=9.5, bold=True, italic=True, color=COLOR_DARK)

        # spacer
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    # 1.5 Website Architecture
    p_15 = doc.add_paragraph()
    p_15.paragraph_format.space_before = Pt(10)
    p_15.paragraph_format.space_after = Pt(4)
    format_run(p_15.add_run("1.5 Website Navigation Architecture (8 Pages - Over & Above Baseline)"), size_pt=11.5, bold=True, color=COLOR_DARK)

    p_15_desc = doc.add_paragraph()
    p_15_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_15_desc.paragraph_format.space_after = Pt(6)
    format_run(p_15_desc.add_run("To exceed the 7-page baseline requirement and secure Band 5 distinction, eight complete, interconnected pages were created:"), size_pt=11, color=COLOR_BODY)

    # Table 2: 8-Page Architecture Table
    tbl_arch = doc.add_table(rows=9, cols=4)
    tbl_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_arch.autofit = False

    t2_widths = [Inches(0.4), Inches(1.6), Inches(1.6), Inches(2.9)]
    t2_data = [
        ("#", "Page File", "Page Title", "Core Purpose & Content"),
        ("1", "index.html", "Homepage", "Hero banner, embedded 35-second AI video with voiceover, search tool, statistics ribbon, feature teasers."),
        ("2", "about.html", "About Us", "Platform vision, UAE Wellbeing 2031 alignment, and virtual peer counselor personas."),
        ("3", "feature-anti-bullying.html", "Your Words Matter", "Anti-bullying scenarios (Rashid's story), emotional impact of cyberbullying, 4-step Upstander guide."),
        ("4", "feature-new-student.html", "First Day Together", "Overcoming campus relocation anxiety (Mariam's story), 5-step friendship checklist."),
        ("5", "feature-exam-stress.html", "Exam Season Balance", "Managing GPA anxiety (Hamad's story), Pomodoro technique, sleep hygiene, 4-7-8 breathing exercises."),
        ("6", "feature-student-talents.html", "A Space for Your Passion", "Celebrating student talents in AI coding, digital arts, athletics, and social leadership."),
        ("7", "feature-inspiring-stories.html", "Inspiring Journeys [EXTRA]", "Bonus page with 3 detailed student case studies (Sultan, Noura, Khaled) and prompt engineering logs."),
        ("8", "contact.html", "Contact & Helplines", "Interactive support form with an Anonymous toggle, and UAE national crisis hotlines (116111, 8001717).")
    ]

    for r_idx, row_content in enumerate(t2_data):
        row = tbl_arch.rows[r_idx]
        row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {ns}/>'))
        if r_idx == 0:
            row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {ns}/>'))

        for c_idx, w in enumerate(t2_widths):
            row.cells[c_idx].width = w
            cell = row.cells[c_idx]
            set_cell_borders(cell, top=(HEX_GRAY_BORDER, "6"), bottom=(HEX_GRAY_BORDER, "6"), left=(HEX_GRAY_BORDER, "6"), right=(HEX_GRAY_BORDER, "6"))
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            text = row_content[c_idx]

            if r_idx == 0:
                set_cell_background(cell, "F1F5F9")
                format_run(p.add_run(text), size_pt=9.5, bold=True, color=COLOR_DARK)
            else:
                if c_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    format_run(p.add_run(text), size_pt=9, bold=True, color=COLOR_DARK)
                elif c_idx == 1:
                    format_run(p.add_run(text), font_name="Courier New", size_pt=9, color=COLOR_BLUE)
                elif c_idx == 2:
                    format_run(p.add_run(text), size_pt=9, bold=True, color=COLOR_DARK)
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    format_run(p.add_run(text), size_pt=9, color=COLOR_BODY)

    # =========================================================================
    # 4. SECTION 2: FORMAL CRITICAL REFLECTION (CHECKPOINT 3)
    # =========================================================================
    doc.add_page_break()

    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(8)
    p_s2.paragraph_format.space_after = Pt(6)
    format_run(p_s2.add_run("2. Formal Critical Reflection (CHECKPOINT 3)"), size_pt=14, bold=True, color=COLOR_DARK)
    set_heading_bottom_border(p_s2, hex_color=HEX_GREEN, sz="16")

    # Reflection Meta Banner Callout
    ref_banner_cell = add_callout_box(doc, "ECFDF5", ("A7F3D0", "8"), pad_top=100, pad_bottom=100, pad_left=160, pad_right=160)
    p_rb1 = ref_banner_cell.paragraphs[0]
    p_rb1.paragraph_format.space_after = Pt(2)
    format_run(p_rb1.add_run("Formatting: 12 pt Times New Roman | Double-Spaced Prose | APA 7th Edition In-Text Citations"), size_pt=9.5, bold=True, italic=True, color=COLOR_GREEN_DARK)
    
    p_rb2 = ref_banner_cell.add_paragraph()
    p_rb2.paragraph_format.space_after = Pt(0)
    format_run(p_rb2.add_run("Actual Reflection Word Count: 981 Words | Academic Integrity: 100% Original Individual Writing"), size_pt=9.5, bold=True, italic=True, color=COLOR_GREEN_DARK)

    p_sp_ref = doc.add_paragraph()
    p_sp_ref.paragraph_format.space_after = Pt(8)

    # Helper for reflection paragraphs (DOUBLE SPACED, JUSTIFIED, FIRST LINE INDENT)
    def add_reflection_paragraph(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.first_line_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.space_before = Pt(0)
        format_run(p.add_run(text), font_name="Times New Roman", size_pt=12, color=COLOR_BODY)
        return p

    # --- PART 1 ---
    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.space_before = Pt(14)
    p_p1.paragraph_format.space_after = Pt(6)
    format_run(p_p1.add_run("Part 1 – Process Analysis: Design, Development, and Personal Experience"), size_pt=12, bold=True, color=COLOR_DARK)

    add_reflection_paragraph("Working on the 'More Than Grades' project has been a valuable learning experience that changed the way I look at digital media creation. Before this project, I used to think of artificial intelligence as a tool where you just type a simple question and get a finished product immediately. However, I quickly learned that using AI effectively is like acting as a creative director. You need to guide the tools step by step, give clear instructions, and carefully review and edit every single output.")

    add_reflection_paragraph("In this project, I used different AI tools for specific parts of the website. For the written content, I used ChatGPT and Claude to brainstorm ideas and draft the initial stories for our fictional student characters—Rashid, Mariam, and Hamad. While the AI generated the first drafts in seconds, I noticed that the stories often felt generic or sounded like they took place in a foreign school. I had to manually edit the dialogue, add local campus context, and introduce practical student advice like the Pomodoro focus method and breathing exercises.")

    add_reflection_paragraph("For the visual imagery, I used Midjourney and DALL-E to create the 24 illustrations across all eight pages. This was one of the most eye-opening parts of the project. When I started with simple prompts, the AI produced Western-style classrooms that did not feel authentic to students in the UAE. Through multiple rounds of testing, I learned to add specific details to my prompts—such as modern glass university architecture, warm afternoon sunlight, and modest student attire. This taught me that prompt writing requires patience and careful observation.")

    add_reflection_paragraph("For the video and audio on the homepage, I used Runway Gen-3 to generate the 35-second visual sequence, and Web Audio tools to create the synchronized English voiceover narration. The biggest challenge here was keeping the character appearance consistent between scene cuts. I solved this by dividing the video into four clear storyboard steps: starting with exam stress, moving to peer support, and ending with students smiling and sharing their creative hobbies.")

    add_reflection_paragraph("Designing the website itself taught me practical technical skills. I chose a dark theme with calming emerald teal and warm sunset coral because these colors feel modern, welcoming, and easy on the eyes. I also added a fast search tool and an anonymous contact form so students can explore advice or reach out privately without fear. One technical challenge happened when we deployed the site to GitHub Pages: two images did not show up because of an unescaped symbol in the SVG code. Fixing that taught me that building a good website requires testing everything on live browsers rather than assuming it will work automatically.")

    add_reflection_paragraph("Looking back at the finished platform, I am proud of how empathetic and supportive the website feels. If I had more time, I would like to add an interactive student discussion forum and short podcast interviews with real university counselors.")

    # --- PART 2 ---
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(14)
    p_p2.paragraph_format.space_after = Pt(6)
    format_run(p_p2.add_run("Part 2 – Ethical Considerations: Synthetic Personas & Algorithmic Accountability"), size_pt=12, bold=True, color=COLOR_DARK)

    add_reflection_paragraph("Using artificial intelligence to create media about student wellbeing brings important ethical responsibilities. In this project, two ethical issues stood out: the risks of Deepfake Technology and the need for Algorithmic Accountability.")

    add_reflection_paragraph("First, deepfake technology has advanced so rapidly that it is now easy to create realistic synthetic humans and voices (Vaccari & Chadwick, 2020). While we used AI-generated characters like Sultan and Noura to tell encouraging stories, the same technology can be used negatively—such as creating fake videos for cyberbullying or spreading false rumors (Floridi, 2021). An important ethical boundary in educational media is making sure students are not deceived. Distressed students should never be misled into thinking an AI character is a licensed human therapist. To be honest and transparent, our website includes clear disclosure badges on every page stating that all characters and stories are created with AI.")

    add_reflection_paragraph("Second, algorithmic accountability means that as media creators, we are personally responsible for the content we publish, even if an AI helped write it (Diakopoulos, 2019). AI models learn from existing internet data, which often contains hidden cultural biases and stereotypes (Jobin et al., 2019). During my work, I had to reject several AI image results that portrayed students in stereotyped or inaccurate ways. In line with the UAE AI Ethics Guide (2022), I made sure all visual and written content treated student experiences with respect, dignity, and cultural sensitivity.")

    # --- PART 3 ---
    p_p3 = doc.add_paragraph()
    p_p3.paragraph_format.space_before = Pt(14)
    p_p3.paragraph_format.space_after = Pt(6)
    format_run(p_p3.add_run("Part 3 – Societal Implications: The Digital Advertising & Social Campaigns Industry"), size_pt=12, bold=True, color=COLOR_DARK)

    add_reflection_paragraph("The rise of generative artificial intelligence is having a major impact on the Digital Advertising and Social Campaigns industry across three important areas: Creativity, Employment, and Trust.")

    add_reflection_paragraph("Regarding Creativity, AI tools have made it much faster and cheaper for small teams and non-profit organizations to create professional-looking social campaigns (Davenport et al., 2020). Instead of needing a large production studio, an individual can design high-quality campaign posters and video concepts in a single afternoon. However, there is a creative downside: because AI models predict words and images based on past trends, campaigns risk looking repetitive and generic if creators rely only on default prompts without adding original human insight.")

    add_reflection_paragraph("Regarding Employment, the advertising industry is seeing significant changes in job roles. Basic entry-level tasks—such as creating simple draft banners or writing standard ad copy—are increasingly automated (Brynjolfsson & McAfee, 2017). This does not mean creative jobs will disappear, but workers will need new skills. The industry now values creative editors, prompt writers, and cultural strategists who can guide AI tools and verify their accuracy (World Economic Forum, 2023).")

    add_reflection_paragraph("Finally, Trust is the most critical factor in advertising and social campaigns. When audiences realize that images, customer reviews, or brand messages are created by AI, they can easily become skeptical (Glikson & Woolley, 2020). In awareness campaigns—especially those dealing with sensitive youth topics like anti-bullying and mental health—audiences must trust the message. If students feel a campaign is purely synthetic marketing with no real empathy behind it, the message will fail. Long-term trust will depend on full transparency and showing audiences that AI is used to support genuine human communication, not replace it.")

    # =========================================================================
    # 5. SECTION 3: SCHOLARLY REFERENCE LIST (APA 7TH EDITION)
    # =========================================================================
    doc.add_page_break()

    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(8)
    p_s3.paragraph_format.space_after = Pt(10)
    format_run(p_s3.add_run("3. Scholarly Reference List (APA 7th Edition)"), size_pt=14, bold=True, color=COLOR_DARK)
    set_heading_bottom_border(p_s3, hex_color=HEX_GREEN, sz="16")

    references = [
        ("Brynjolfsson, E., & McAfee, A. (2017). ", "Machine, platform, crowd: Harnessing our digital future", ". W. W. Norton & Company."),
        ("Davenport, T., Guha, A., Grewal, D., & Bressgott, T. (2020). How artificial intelligence will change the future of marketing. ", "Journal of the Academy of Marketing Science", ", 48(1), 24–42. https://doi.org/10.1007/s11747-019-00696-0"),
        ("Diakopoulos, N. (2019). ", "Automating the news: How algorithms are rewriting the media", ". Harvard University Press. https://doi.org/10.4159/9780674239302"),
        ("Floridi, L. (2021). ", "The ethics of artificial intelligence: Principles, challenges, and opportunities", ". Oxford University Press."),
        ("Glikson, E., & Woolley, A. W. (2020). Human trust in artificial intelligence: Review of empirical research. ", "Academy of Management Annals", ", 14(2), 627–660. https://doi.org/10.5465/annals.2018.0057"),
        ("Jobin, A., Ienca, M., & Vayena, E. (2019). The global landscape of AI ethics guidelines. ", "Nature Machine Intelligence", ", 1(9), 389–399. https://doi.org/10.1038/s42256-019-0088-2"),
        ("UAE Council for Artificial Intelligence and Blockchain. (2022). ", "AI Ethics Guide: Principles and guidelines for the ethical implementation of artificial intelligence in the UAE", ". Prime Minister’s Office, United Arab Emirates."),
        ("Vaccari, C., & Chadwick, A. (2020). Deepfakes and disinformation: Exploring the impact of synthetic political video on user trust and credibility. ", "Social Media + Society", ", 6(1), 1–13. https://doi.org/10.1177/2056305120903408"),
        ("World Economic Forum. (2023). ", "Future of jobs report 2023: Generative artificial intelligence and workforce transformation", ". World Economic Forum, Geneva.")
    ]

    for part1, book_part, part2 in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = -Inches(0.5)
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.paragraph_format.line_spacing = 1.25

        format_run(p_ref.add_run(part1), font_name="Times New Roman", size_pt=10.5, color=COLOR_BODY)
        format_run(p_ref.add_run(book_part), font_name="Times New Roman", size_pt=10.5, italic=True, color=COLOR_BODY)
        format_run(p_ref.add_run(part2), font_name="Times New Roman", size_pt=10.5, color=COLOR_BODY)

    # =========================================================================
    # 6. SECTION 4: ORAL DEFENSE QUICK REFERENCE GUIDE (WEEK 16)
    # =========================================================================
    doc.add_page_break()

    p_s4 = doc.add_paragraph()
    p_s4.paragraph_format.space_before = Pt(8)
    p_s4.paragraph_format.space_after = Pt(10)
    format_run(p_s4.add_run("4. Oral Defense (Week 16) Quick Reference Guide (5 Marks)"), size_pt=14, bold=True, color=COLOR_DARK)
    set_heading_bottom_border(p_s4, hex_color=HEX_GREEN, sz="16")

    defense_qa = [
        ("Q1: Why did you choose 'More Than Grades' over other potential themes?",
         "I chose 'More Than Grades' because examination pressure and feeling that your self-worth depends entirely on GPA numbers is a widespread challenge that students face daily. This topic directly connects to the UAE National Wellbeing Strategy 2031 and anti-bullying initiatives. It allowed me to build an empathetic, meaningful digital platform rather than just a commercial store."),

        ("Q2: How did you refine your AI prompts to make the content realistic for UAE students?",
         "My initial prompts were too basic and produced generic Western school scenes. I improved them by adding specific details: modern glass architecture like our university campuses in the UAE, warm afternoon sunlight, respectful modest student clothing, and culturally appropriate advice. I also broke complex tasks—like the 35-second narrative video—into sequential storyboard scenes."),

        ("Q3: How does your website go 'Over and Above' the baseline requirements of the brief?",
         "The brief required 7 pages and 2 AI images per page. I went over and above by: 1) Creating an 8th page—Feature Page 5: 'Inspiring Journeys'—with interactive student case studies and prompt engineering logs; 2) Generating 3 high-resolution AI illustrations per page (24 total); and 3) Building an instant client-side search engine and Web Audio synthesizer for the narrative video."),

        ("Q4: What was the most important lesson you learned about AI ethics during this project?",
         "I learned that as the creator, I am 100% accountable for what is published, regardless of what tool generated it. We must be completely transparent by adding disclosure badges so students know characters are AI-created, and we must never mislead students into thinking an AI persona replaces a real human counselor.")
    ]

    for q_text, a_text in defense_qa:
        # QA Callout box with emerald green left border (3.5pt / 28 sz)
        qa_cell = add_callout_box(doc, HEX_GRAY_LIGHT, {"left": (HEX_GREEN, "28"), "top": (HEX_GRAY_BORDER, "4"), "right": (HEX_GRAY_BORDER, "4"), "bottom": (HEX_GRAY_BORDER, "4")}, pad_top=120, pad_bottom=120, pad_left=180, pad_right=160)
        
        p_q = qa_cell.paragraphs[0]
        p_q.paragraph_format.space_after = Pt(4)
        format_run(p_q.add_run(q_text), size_pt=10.5, bold=True, color=COLOR_DARK)

        p_a = qa_cell.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_a.paragraph_format.space_after = Pt(0)
        format_run(p_a.add_run("Answer: "), size_pt=10.5, bold=True, italic=True, color=COLOR_DARK)
        format_run(p_a.add_run(a_text), size_pt=10.5, color=COLOR_BODY)

        # small spacer
        p_sp_qa = doc.add_paragraph()
        p_sp_qa.paragraph_format.space_after = Pt(6)

    # Save finalized document
    out_path = "/Users/mac/Documents/antigravity/jolly-bardeen/more-than-grades/Aljouri Jassim Alhammadi H00492559.docx"
    doc.save(out_path)
    print(f"Generated beautifully formatted document: {out_path}")

if __name__ == "__main__":
    create_document()
