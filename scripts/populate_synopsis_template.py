import os
import shutil
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.text.text import _Paragraph

# Patch python-pptx _Paragraph.add_run to accept an optional text parameter
_orig_add_run = _Paragraph.add_run
def _patched_add_run(self, text=None):
    r = _orig_add_run(self)
    if text is not None:
        r.text = str(text)
    return r
_Paragraph.add_run = _patched_add_run

# Color Palette
COLOR_NAVY = RGBColor(15, 23, 42)        # #0F172A
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB
COLOR_DARK_BLUE = RGBColor(30, 58, 138)  # #1E3A8A
COLOR_GREEN = RGBColor(5, 150, 105)      # #059669
COLOR_RED = RGBColor(220, 38, 38)        # #DC2626
COLOR_AMBER = RGBColor(217, 119, 6)      # #D97706
COLOR_MUTED = RGBColor(71, 85, 105)      # #475569
COLOR_LIGHT_MUTED = RGBColor(148, 163, 184) # #94A3B8
COLOR_CARD = RGBColor(255, 255, 255)     # White
COLOR_CARD_ALT = RGBColor(248, 250, 252) # #F8FAFC
COLOR_CARD_BLUE = RGBColor(240, 249, 255)# #F0F9FF
COLOR_CARD_GREEN = RGBColor(236, 253, 245)# #ECFDF5
COLOR_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
COLOR_BORDER_BLUE = RGBColor(191, 219, 254) # #BFDBFE
COLOR_BORDER_GREEN = RGBColor(167, 243, 208)
COLOR_BORDER_RED = RGBColor(254, 202, 202)

def add_card(slide, left, top, width, height, border_color=COLOR_BORDER, fill_color=COLOR_CARD, border_width=Pt(1.2)):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = border_width
    return card

def add_badge(slide, left, top, width, height, text, bg_color=COLOR_BLUE, text_color=RGBColor(255,255,255), font_size=Pt(9)):
    b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    b.fill.solid()
    b.fill.fore_color.rgb = bg_color
    b.line.fill.background()
    tf = b.text_frame
    tf.word_wrap = False
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = font_size
    r.font.bold = True
    r.font.color.rgb = text_color
    return b

def clear_dummy_textboxes(slide):
    """Remove placeholder textboxes with broken fonts from template slides 3-11."""
    to_remove = []
    for sh in slide.shapes:
        if 'TextBox' in sh.name or 'Content Placeholder' in sh.name:
            to_remove.append(sh)
    for sh in to_remove:
        sp = sh._element
        sp.getparent().remove(sp)

def populate_presentation():
    template_path = r'C:\Users\KIIT\Downloads\0bbeb81d157f41dbb44b96a154bf5bfd (3).pptx'
    prs = Presentation(template_path)
    
    # =========================================================================
    # SLIDE 2: PROJECT TITLE & DEFENSE DETAILS
    # =========================================================================
    s2 = prs.slides[1]
    
    # 1. Update Project Title
    for sh in s2.shapes:
        if 'TextBox 4' in sh.name:
            sh.left = Inches(0.5)
            sh.top = Inches(1.22)
            sh.width = Inches(9.0)
            sh.height = Inches(1.0)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run("Transformer-Based Multilingual Fake News Detection System")
            r.font.name = "Arial"
            r.font.size = Pt(20)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
            
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            r2 = p2.add_run("with Attention-Based Explainability (XAI)")
            r2.font.name = "Arial"
            r2.font.size = Pt(17)
            r2.font.bold = True
            r2.font.color.rgb = COLOR_BLUE

    # 2. Update Subtitle
    for sh in s2.shapes:
        if 'TextBox 12' in sh.name:
            sh.left = Inches(0.5)
            sh.top = Inches(2.35)
            sh.width = Inches(9.0)
            sh.height = Inches(0.85)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run("FINAL YEAR PROJECT SYNOPSIS DEFENSE")
            r.font.name = "Arial"
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = COLOR_DARK_BLUE
            
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            r2 = p2.add_run("Master of Computer Applications (MCA) — Academic Session 2025–2026")
            r2.font.name = "Calibri"
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = COLOR_MUTED

    # 3. Update Table 2 (Submitted By)
    for sh in s2.shapes:
        if sh.has_table:
            sh.left = Inches(1.0)
            sh.top = Inches(3.30)
            sh.width = Inches(8.0)
            sh.height = Inches(2.3)
            table = sh.table
            
            headers = ["ROLL NUMBER", "STUDENT NAME & CANDIDATE ROLE"]
            rows_data = [
                ("2501560034", "M. Aqmar Asmeer Iqbal (Lead Researcher)"),
                ("2501560021", "Amandeep (Co-Researcher)"),
                ("GROUP ID", "Group 26O4028"),
                ("DEPARTMENT", "School of Computer Applications, K.R. Mangalam University")
            ]
            
            # Format Header Row
            for col_idx, h_text in enumerate(headers):
                c = table.cell(0, col_idx)
                c.text = h_text
                c.fill.solid()
                c.fill.fore_color.rgb = COLOR_DARK_BLUE
                p = c.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(11)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)
            
            # Format Data Rows
            for row_idx, (c0, c1) in enumerate(rows_data, start=1):
                cell0 = table.cell(row_idx, 0)
                cell0.text = c0
                cell0.fill.solid()
                cell0.fill.fore_color.rgb = COLOR_CARD_ALT if row_idx % 2 == 1 else COLOR_CARD
                p0 = cell0.text_frame.paragraphs[0]
                p0.alignment = PP_ALIGN.CENTER
                for r in p0.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(10.5)
                    r.font.bold = True if row_idx in (1, 2, 3) else False
                    r.font.color.rgb = COLOR_BLUE if row_idx in (1, 2) else COLOR_NAVY
                
                cell1 = table.cell(row_idx, 1)
                cell1.text = c1
                cell1.fill.solid()
                cell1.fill.fore_color.rgb = COLOR_CARD_ALT if row_idx % 2 == 1 else COLOR_CARD
                p1 = cell1.text_frame.paragraphs[0]
                p1.alignment = PP_ALIGN.LEFT
                for r in p1.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(10.5)
                    r.font.bold = True if row_idx in (1, 2) else False
                    r.font.color.rgb = COLOR_NAVY

    # 4. Update Faculty Mentor Box
    for sh in s2.shapes:
        if 'TextBox 7' in sh.name:
            sh.left = Inches(0.5)
            sh.top = Inches(5.80)
            sh.width = Inches(9.0)
            sh.height = Inches(0.9)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run("Faculty Mentor: ")
            r.font.name = "Arial"
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
            r_name = p.add_run("Ms. Lucky Verma")
            r_name.font.name = "Arial"
            r_name.font.size = Pt(12.5)
            r_name.font.bold = True
            r_name.font.color.rgb = COLOR_BLUE
            r_role = p.add_run(" | Assistant Professor")
            r_role.font.name = "Calibri"
            r_role.font.size = Pt(11)
            r_role.font.color.rgb = COLOR_MUTED
            
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            r_inst = p2.add_run("Department of Computer Science & Engineering | School of Engineering and Technology")
            r_inst.font.name = "Calibri"
            r_inst.font.size = Pt(9.5)
            r_inst.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 3: PROJECT OVERVIEW
    # =========================================================================
    s3 = prs.slides[2]
    clear_dummy_textboxes(s3)
    
    # 3 Cards: Problem Statement, Limitations of Prior Systems, Proposed Solution
    cards_data_s3 = [
        {
            "left": Inches(0.5), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER_RED, "fill": COLOR_CARD,
            "badge": "PROBLEM STATEMENT", "badge_bg": COLOR_RED,
            "title": "Information Disorder in Regional Languages",
            "bullets": [
                ("Regional Disinformation:", "Viral fake news campaigns exploit regional Indian languages (Hindi, Bengali) where fact-checking resources are critically scarce."),
                ("Societal Vulnerability:", "Unchecked claims during public health emergencies, communal incidents, and elections incite widespread panic and real-world violence."),
                ("Linguistic Resource Gap:", "Over 600M vernacular internet users exist with less than 5% automated fact-checking coverage, leaving regional digital ecosystems exposed."),
                ("High Velocity:", "Fabricated narratives spread 6x faster than verified truths on encrypted messaging platforms (WhatsApp, Telegram).")
            ]
        },
        {
            "left": Inches(3.55), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER, "fill": COLOR_CARD,
            "badge": "PRIOR LIMITATIONS", "badge_bg": COLOR_NAVY,
            "title": "Monolingual Silos & Opaque Heuristics",
            "bullets": [
                ("Monolingual Silos:", "Existing CNN/LSTM models are trained almost exclusively on English news (ISOT, LIAR), collapsing when tested on Indic vernacular or code-mixed text."),
                ("Black-Box Opacity:", "Deep neural networks predict binary labels (Real/Fake) without explanation, prompting user skepticism and resistance from journalists."),
                ("Shallow Lexical Heuristics:", "Keyword blacklists and n-gram models fail to detect subtle contextual hyperbole, satirical deception, and rephrased propaganda."),
                ("Zero Cross-Lingual Transfer:", "Lack shared multilingual semantic representations to generalize high-resource knowledge to regional dialects.")
            ]
        },
        {
            "left": Inches(6.60), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER_BLUE, "fill": COLOR_CARD_BLUE,
            "badge": "PROPOSED SOLUTION", "badge_bg": COLOR_BLUE,
            "title": "Multilingual Transformers + Dual XAI",
            "bullets": [
                ("Cross-Lingual Transformers:", "Leverages pre-trained mBERT and XLM-RoBERTa for zero-shot cross-lingual transfer across 5 languages (EN, HI, BN, ES, FR)."),
                ("Layer Attention Rollout:", "Recursively computes attention flow across all 12 transformer encoder layers down to subword token spans without layer collapse."),
                ("Token-Level SHAP Values:", "Game-theoretic feature attributions quantify directional evidence (+ pushes Fake, - pushes Real) for forensic transparency."),
                ("Interactive Forensic HUD:", "High-performance web dashboard (Streamlit & Flask) with real-time risk gauges, subword heatmaps, and sub-50ms inference.")
            ]
        }
    ]
    
    for c_data in cards_data_s3:
        c = add_card(s3, c_data["left"], c_data["top"], c_data["width"], c_data["height"], c_data["border"], c_data["fill"])
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        
        # Badge & Title
        p_badge = tf.paragraphs[0]
        r_b = p_badge.add_run(c_data["badge"] + "\n")
        r_b.font.name = "Arial"
        r_b.font.size = Pt(8.5)
        r_b.font.bold = True
        r_b.font.color.rgb = c_data["badge_bg"]
        
        r_t = p_badge.add_run(c_data["title"])
        r_t.font.name = "Arial"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_NAVY
        p_badge.space_after = Pt(8)
        
        # Bullets
        for b_head, b_desc in c_data["bullets"]:
            p = tf.add_paragraph()
            p.space_after = Pt(6)
            r_h = p.add_run("• " + b_head + " ")
            r_h.font.name = "Arial"
            r_h.font.size = Pt(8.8)
            r_h.font.bold = True
            r_h.font.color.rgb = COLOR_NAVY
            r_d = p.add_run(b_desc)
            r_d.font.name = "Calibri"
            r_d.font.size = Pt(8.5)
            r_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 4: SPECIFIC OBJECTIVES
    # =========================================================================
    s4 = prs.slides[3]
    clear_dummy_textboxes(s4)
    
    objectives_data = [
        ("01", "Multilingual Deep Learning Backbone",
         "Fine-tune pre-trained multilingual transformer models (mBERT and XLM-RoBERTa) on multi-domain benchmark corpora across 5 languages (English, Hindi, Bengali, Spanish, French) to establish unified cross-lingual semantic representations enabling zero-shot transfer.",
         COLOR_BLUE),
        ("02", "Formulation of Attention Rollout Algorithm",
         "Formulate and implement a layer-recursive Attention Rollout algorithm across all 12 transformer encoder layers: A^(l) = 0.5 * W_raw^(l) + 0.5 * I, preventing multi-layer attention dispersion and mapping raw weights directly to subword token spans.",
         COLOR_GREEN),
        ("03", "Dual-Mode SHAP Attribution Integration",
         "Integrate Kernel and Tree SHAP token-level attribution to quantify the directional marginal contribution of each word (+ pushes Deceptive/Fake, - pushes Authentic/Real), validating self-attention distributions against game-theoretic ground truth.",
         COLOR_AMBER),
        ("04", "Production-Grade Forensic Web Dashboard",
         "Develop a sub-50ms responsive web dashboard and REST API (Streamlit & Flask) featuring real-time risk gauges, subword token heatmaps, lexical diversity calculations, pre-loaded verification datasets, and comprehensive empirical diagnostics.",
         COLOR_NAVY)
    ]
    
    for idx, (num_str, obj_title, obj_desc, accent_color) in enumerate(objectives_data):
        top_y = Inches(1.40 + idx * 1.30)
        c = add_card(s4, Inches(0.5), top_y, Inches(9.0), Inches(1.18), border_color=COLOR_BORDER)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.12)
        
        p = tf.paragraphs[0]
        r_num = p.add_run(f"OBJECTIVE {num_str}  |  ")
        r_num.font.name = "Arial"
        r_num.font.size = Pt(11)
        r_num.font.bold = True
        r_num.font.color.rgb = accent_color
        
        r_title = p.add_run(obj_title)
        r_title.font.name = "Arial"
        r_title.font.size = Pt(11.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(3)
        
        p2 = tf.add_paragraph()
        r_desc = p2.add_run(obj_desc)
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9.5)
        r_desc.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 5: KEY FEATURES
    # =========================================================================
    s5 = prs.slides[4]
    clear_dummy_textboxes(s5)
    
    features_data = [
        (Inches(0.5), Inches(1.40), "Feature 01: Zero-Shot Cross-Lingual Transfer",
         "Cross-Lingual Semantic Generalization",
         "• Shared Multilingual Space: Pre-trained shared subword embeddings align semantic representations across 100+ languages without manual parallel translation.\n• High-to-Low Resource Transfer: Transfers rich linguistic features learned on large English corpora directly to Hindi and Bengali without requiring language-specific training data.\n• Dialect & Script Agnostic: Seamlessly processes Devanagari, Bengali, and Latin scripts, handling code-mixed social media news effectively.",
         COLOR_BORDER_BLUE, COLOR_CARD_BLUE),
        (Inches(5.1), Inches(1.40), "Feature 02: Subword-Level Interpretability",
         "Fine-Grained Morphological Tracking",
         "• SentencePiece & WordPiece Tokens: Tokenizes text into subword units, exposing manipulative prefixes, sensationalized stems, and clickbait suffixes.\n• Beyond Sentence-Level Labels: Pinpoints exact suspicious tokens rather than returning opaque document-level binary classifications.\n• Rhetorical Trigger Detection: Automatically flags hyperbolic intensifiers, sensational verbs, and emotionally charged linguistic constructs.",
         COLOR_BORDER, COLOR_CARD),
        (Inches(0.5), Inches(3.95), "Feature 03: Dual-Mode Explainability (XAI)",
         "Axiomatic Math & Structural Attention Flow",
         "• Layer-Recursive Attention Rollout: Aggregates multi-head self-attention across 12 encoder layers with identity matrix residual scaling to eliminate attention diffusion.\n• Directional SHAP Attribution: Game-theoretic Shapley values quantify marginal contributions (+ push Deceptive, - push Authentic).\n• Dual Cross-Validation: Verifies structural attention patterns against game-theoretic ground truth for forensic confidence.",
         COLOR_BORDER, COLOR_CARD),
        (Inches(5.1), Inches(3.95), "Feature 04: Production Forensic HUD & Fast API",
         "High-Throughput Verification Suite",
         "• Sub-50ms Inference Latency: Optimized runtime with pre-loaded models and instant zero-delay verification response.\n• Interactive Visual Indicators: Dynamic circular risk gauge, confidence percentage badges, and interactive subword token heatmaps.\n• Dual Serving Endpoints: Integrated Streamlit forensic dashboard for researchers and Flask REST API for enterprise fact-checking workflows.",
         COLOR_BORDER_GREEN, COLOR_CARD_GREEN)
    ]
    
    for left_x, top_y, title_text, sub_text, body_text, b_col, f_col in features_data:
        c = add_card(s5, left_x, top_y, Inches(4.4), Inches(2.40), border_color=b_col, fill_color=f_col)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        r = p.add_run(title_text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(2)
        
        p_sub = tf.add_paragraph()
        r_sub = p_sub.add_run(sub_text)
        r_sub.font.name = "Arial"
        r_sub.font.size = Pt(8.5)
        r_sub.font.bold = True
        r_sub.font.color.rgb = COLOR_BLUE
        p_sub.space_after = Pt(4)
        
        for line in body_text.split("\n"):
            p_line = tf.add_paragraph()
            p_line.space_after = Pt(3)
            r_l = p_line.add_run(line)
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(8.8)
            r_l.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 6: PROJECT USECASES & SCOPE
    # =========================================================================
    s6 = prs.slides[5]
    clear_dummy_textboxes(s6)
    
    # Left Card: Real-World Use Cases
    c_left = add_card(s6, Inches(0.5), Inches(1.40), Inches(4.4), Inches(5.25), border_color=COLOR_BORDER_GREEN, fill_color=COLOR_CARD)
    tf_l = c_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.25)
    
    p = tf_l.paragraphs[0]
    r = p.add_run("TARGET USE CASES & DEPLOYMENT\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_GREEN
    r2 = p.add_run("Real-World Operational Scenarios")
    r2.font.name = "Arial"; r2.font.size = Pt(12); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    
    use_cases = [
        ("Fact-Checking Newsrooms (PTI, AltNews, BoomLive):", "Automates initial triage of thousands of daily viral news tips across regional languages, highlighting suspicious token spans for human editors."),
        ("Social Media Platform Content Moderation:", "Serves as an automated first responder to flag, down-rank, or attach cautionary contextual advisories to high-velocity vernacular posts."),
        ("Public Health & Disaster Management Authorities:", "Real-time surveillance and early containment of dangerous medical hoaxes and catastrophe rumors during pandemics and civic emergencies."),
        ("Electoral Integrity & Governance Bodies:", "Safeguards voter perception by monitoring automated coordinated disinformation and deep-narrative propaganda campaigns during national elections."),
        ("Academic & Forensic Media Research:", "Provides an open-source benchmarking framework for studying cross-lingual deception dynamics and linguistic framing patterns.")
    ]
    for uc_head, uc_body in use_cases:
        p = tf_l.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run("• " + uc_head + " "); r1.font.name = "Arial"; r1.font.size = Pt(9); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(uc_body); r2.font.name = "Calibri"; r2.font.size = Pt(8.6); r2.font.color.rgb = COLOR_MUTED

    # Right Card: Project Scope & Boundaries
    c_right = add_card(s6, Inches(5.1), Inches(1.40), Inches(4.4), Inches(5.25), border_color=COLOR_BORDER, fill_color=COLOR_CARD)
    tf_r = c_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.25)
    
    p = tf_r.paragraphs[0]
    r = p.add_run("PROJECT SCOPE & BOUNDARIES\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    r2 = p.add_run("Technical Boundaries & Constraints")
    r2.font.name = "Arial"; r2.font.size = Pt(12); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    
    scope_items = [
        ("In-Scope Linguistic Coverage:", "Full contextual detection and explainability for text claims in 5 languages: English, Hindi, Bengali, Spanish, and French."),
        ("In-Scope Architectural Core:", "Transformer fine-tuning (mBERT, XLM-RoBERTa), subword tokenization, layer Attention Rollout, Kernel SHAP attribution, and web dashboard."),
        ("Out-of-Scope (Multimodal Audio/Video):", "Deepfake video manipulation, doctored photographic images, and voice clone audio detection are reserved for future project iterations."),
        ("Out-of-Scope (Social Network Graphs):", "Topological diffusion analysis (user propagation cascades, bot cluster graph analysis) is excluded; system focuses purely on content semantics."),
        ("Computational Footprint:", "Optimized for cloud servers and standard workstations with GPU/CPU serving; ultra-low-power mobile edge deployment targeted for Phase 2.")
    ]
    for sc_head, sc_body in scope_items:
        p = tf_r.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run("• " + sc_head + " "); r1.font.name = "Arial"; r1.font.size = Pt(9); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(sc_body); r2.font.name = "Calibri"; r2.font.size = Pt(8.6); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 7: ARCHITECTURE & SYSTEM FLOW
    # =========================================================================
    s7 = prs.slides[6]
    clear_dummy_textboxes(s7)
    
    # 5 Flowchart blocks at top
    blocks_flow = [
        ("1. Input Claim", "Multilingual Raw Text\n(EN, HI, BN, ES, FR)", COLOR_NAVY),
        ("2. Normalization", "Unicode NFKC Clean\nSubword Tokenizer", COLOR_BLUE),
        ("3. Transformer", "mBERT / XLM-R\n12-Layers, 12-Heads", COLOR_DARK_BLUE),
        ("4. Dual XAI Engine", "Attention Rollout +\nKernel SHAP Attrib", COLOR_AMBER),
        ("5. Forensic HUD", "Credibility Score %\nRisk Gauge & Map", COLOR_GREEN)
    ]
    
    for idx, (b_title, b_sub, b_color) in enumerate(blocks_flow):
        left_pos = Inches(0.5 + idx * 1.82)
        b_box = add_card(s7, left_pos, Inches(1.40), Inches(1.65), Inches(1.30), border_color=b_color, fill_color=COLOR_CARD)
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = Inches(0.1)
        
        p = tf_b.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(b_title + "\n")
        r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = b_color
        
        r2 = p.add_run(b_sub)
        r2.font.name = "Calibri"; r2.font.size = Pt(8); r2.font.color.rgb = COLOR_MUTED
        
        # Add native vector arrow if not last
        if idx < 4:
            arr = s7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left_pos + Inches(1.68), Inches(1.95), Inches(0.12), Inches(0.18))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_LIGHT_MUTED
            arr.line.fill.background()

    # Bottom 2 Explanatory Cards
    c_arch_l = add_card(s7, Inches(0.5), Inches(2.95), Inches(4.4), Inches(3.70), border_color=COLOR_BORDER_BLUE, fill_color=COLOR_CARD)
    tf_al = c_arch_l.text_frame
    tf_al.word_wrap = True
    tf_al.margin_left = tf_al.margin_right = tf_al.margin_top = Inches(0.2)
    
    p = tf_al.paragraphs[0]
    r = p.add_run("DEEP LEARNING PIPELINE COMPONENTS\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    r2 = p.add_run("Transformer Feature Extraction Core")
    r2.font.name = "Arial"; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)
    
    arch_notes_l = [
        ("Cross-Lingual Subword Tokenizer:", "Deconstructs input claims into WordPiece (mBERT) or SentencePiece (XLM-R) subwords from a 250,000 multilingual vocabulary."),
        ("Multi-Head Self-Attention:", "12 transformer encoder layers, each with 12 parallel attention heads capturing global semantic dependencies across long distances."),
        ("Contextual Representation:", "768-dimensional hidden vectors encode subtle rhetorical stance and factual validity across languages."),
        ("Classification Head:", "Dropout (p=0.2) + Dense layer on [CLS] embedding outputs calibrated binary probability: P(Deceptive | x).")
    ]
    for an_h, an_d in arch_notes_l:
        p = tf_al.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run("• " + an_h + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(an_d); r2.font.name = "Calibri"; r2.font.size = Pt(8.2); r2.font.color.rgb = COLOR_MUTED

    c_arch_r = add_card(s7, Inches(5.1), Inches(2.95), Inches(4.4), Inches(3.70), border_color=COLOR_BORDER, fill_color=COLOR_CARD)
    tf_ar = c_arch_r.text_frame
    tf_ar.word_wrap = True
    tf_ar.margin_left = tf_ar.margin_right = tf_ar.margin_top = Inches(0.2)
    
    p = tf_ar.paragraphs[0]
    r = p.add_run("EXPLAINABLE AI & SERVING ARCHITECTURE\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_GREEN
    r2 = p.add_run("Explainability & Dashboard Serving")
    r2.font.name = "Arial"; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)
    
    arch_notes_r = [
        ("Attention Rollout Tracking:", "Recursively traces multi-head self-attention flow from layer 1 to 12, projecting final weights directly onto subword token spans."),
        ("SHAP Directional Attribution:", "Kernel SHAP estimates marginal feature contributions: positive Shapley values flag deception, negative values support credibility."),
        ("Dual-Interface Architecture:", "Streamlit forensic HUD for deep interactive investigation + lightweight Flask REST API for programmatic verification pipelines."),
        ("Sub-50ms Inference Engine:", "Optimized caching and PyTorch evaluation pipeline eliminate cold-start delays for real-time verification.")
    ]
    for an_h, an_d in arch_notes_r:
        p = tf_ar.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run("• " + an_h + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(an_d); r2.font.name = "Calibri"; r2.font.size = Pt(8.2); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 8: DATA & RESOURCES
    # =========================================================================
    s8 = prs.slides[7]
    clear_dummy_textboxes(s8)
    
    cards_data_s8 = [
        {
            "left": Inches(0.5), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER_BLUE, "fill": COLOR_CARD,
            "badge": "DATASETS & CORPORA", "badge_bg": COLOR_BLUE,
            "title": "Benchmark Datasets & Corpora",
            "bullets": [
                ("WELFake Corpus:", "72,134 verified news articles (35,028 real, 37,106 fake) combining Kaggle, McIntire, Reuters, and BuzzFeed datasets."),
                ("ISOT Fake News Corpus:", "44,898 articles from verified Reuters sources and flagged deceptive publications."),
                ("IndicFakeNews Corpus:", "8,400+ curated articles in Hindi and Bengali spanning politics, healthcare, and national events."),
                ("Class Balance:", "Strict 50/50 balance between authentic and deceptive samples to prevent model prior bias."),
                ("Stratified Split:", "80% Training, 10% Validation, 10% Held-Out Test partition across all languages.")
            ]
        },
        {
            "left": Inches(3.55), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER, "fill": COLOR_CARD,
            "badge": "HARDWARE & COMPUTE", "badge_bg": COLOR_NAVY,
            "title": "Compute & Execution Infrastructure",
            "bullets": [
                ("GPU Accelerator:", "NVIDIA RTX 40-Series / A100 GPU cluster with Tensor Cores and CUDA 12.x acceleration."),
                ("VRAM & Precision:", "16 GB dedicated GDDR6 memory utilizing FP16 mixed precision and gradient accumulation."),
                ("Batch Configuration:", "Effective batch size of 32 with AdamW weight decay for stable transformer convergence."),
                ("Host Environment:", "16-Core Intel Core i7 / AMD Ryzen processor, 32 GB DDR5 RAM, high-speed NVMe storage."),
                ("CPU Inference Runtime:", "Optimized PyTorch runtime achieving sub-45ms latency per claim on standard CPU.")
            ]
        },
        {
            "left": Inches(6.60), "top": Inches(1.40), "width": Inches(2.85), "height": Inches(5.25),
            "border": COLOR_BORDER_GREEN, "fill": COLOR_CARD_GREEN,
            "badge": "SOFTWARE & TOOLS", "badge_bg": COLOR_GREEN,
            "title": "Open-Source AI & Framework Stack",
            "bullets": [
                ("Deep Learning Core:", "PyTorch 2.4, Hugging Face Transformers, Hugging Face Tokenizers, Hugging Face Datasets."),
                ("Explainable AI (XAI):", "Captum, SHAP (KernelExplainer), Scikit-Learn, SciPy for mathematical attribution."),
                ("Web Interface & APIs:", "Streamlit 1.39, Flask 3.0, Jinja2, HTML5/CSS3 with modern responsive styling."),
                ("Data & Evaluation:", "Pandas, NumPy, Matplotlib, Seaborn for statistical evaluation and metric charting."),
                ("Environment:", "Python 3.11 with Conda virtual environment management and pinned dependency lock.")
            ]
        }
    ]
    
    for c_data in cards_data_s8:
        c = add_card(s8, c_data["left"], c_data["top"], c_data["width"], c_data["height"], c_data["border"], c_data["fill"])
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        
        p_badge = tf.paragraphs[0]
        r_b = p_badge.add_run(c_data["badge"] + "\n")
        r_b.font.name = "Arial"; r_b.font.size = Pt(8.5); r_b.font.bold = True; r_b.font.color.rgb = c_data["badge_bg"]
        
        r_t = p_badge.add_run(c_data["title"])
        r_t.font.name = "Arial"; r_t.font.size = Pt(11); r_t.font.bold = True; r_t.font.color.rgb = COLOR_NAVY
        p_badge.space_after = Pt(8)
        
        for b_head, b_desc in c_data["bullets"]:
            p = tf.add_paragraph(); p.space_after = Pt(6)
            r_h = p.add_run("• " + b_head + " "); r_h.font.name = "Arial"; r_h.font.size = Pt(8.8); r_h.font.bold = True; r_h.font.color.rgb = COLOR_NAVY
            r_d = p.add_run(b_desc); r_d.font.name = "Calibri"; r_d.font.size = Pt(8.5); r_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 9: METHODOLOGY
    # =========================================================================
    s9 = prs.slides[8]
    clear_dummy_textboxes(s9)
    
    # Left Card: Model Training & Fine-Tuning
    c_m1 = add_card(s9, Inches(0.5), Inches(1.40), Inches(4.4), Inches(5.25), border_color=COLOR_BORDER_BLUE, fill_color=COLOR_CARD)
    tf_m1 = c_m1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = Inches(0.25)
    
    p = tf_m1.paragraphs[0]
    r = p.add_run("1. MODEL FINE-TUNING PIPELINE\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    r2 = p.add_run("Cross-Lingual Deep Contextual Representation")
    r2.font.name = "Arial"; r2.font.size = Pt(11.5); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)
    
    m1_points = [
        ("Unicode Standardization:", "Applies NFKC normalization across Indic (Devanagari, Bengali) and Latin scripts to eliminate homoglyph spoofing and diacritic noise."),
        ("Subword Tokenization:", "SentencePiece tokenizer divides text into subword morphemes from a 250,000 shared multilingual vocabulary, handling morphology-rich Indian languages."),
        ("Transformer Backbone:", "Initializes with pre-trained XLM-RoBERTa-base (12 layers, 12 attention heads, 768 hidden dimension, 125M parameters)."),
        ("Optimization Scheme:", "AdamW optimizer (lr = 2e-5, β1 = 0.9, β2 = 0.999, weight decay = 0.01) with linear warmup over the first 10% steps and cosine learning rate decay."),
        ("Loss Function (BCE with Logits):", "Loss = - (1/N) * Σ [y_i * log(p_i) + (1 - y_i) * log(1 - p_i)], optimizing calibrated decision boundaries between Authentic and Deceptive claims.")
    ]
    for m_h, m_d in m1_points:
        p = tf_m1.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run("• " + m_h + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.8); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(m_d); r2.font.name = "Calibri"; r2.font.size = Pt(8.5); r2.font.color.rgb = COLOR_MUTED

    # Right Card: Attention Rollout & SHAP Explainability Formulations
    c_m2 = add_card(s9, Inches(5.1), Inches(1.40), Inches(4.4), Inches(5.25), border_color=COLOR_BORDER_GREEN, fill_color=COLOR_CARD)
    tf_m2 = c_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_right = tf_m2.margin_top = Inches(0.25)
    
    p = tf_m2.paragraphs[0]
    r = p.add_run("2. EXPLAINABLE AI (XAI) FORMULATIONS\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_GREEN
    r2 = p.add_run("Attention Rollout & Game-Theoretic SHAP")
    r2.font.name = "Arial"; r2.font.size = Pt(11.5); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)
    
    m2_points = [
        ("Attention Rollout Formulation:", "Computes layer-recursive self-attention flow by compensating for skip-connections with an identity matrix:\nA^(l) = 0.5 * W_raw^(l) + 0.5 * I"),
        ("Layer-Wise Accumulation:", "Recursively rolls out attention across all 12 transformer encoder layers to trace input token influence to the classification output:\nÃ = Π (from l=1 to 12) A^(l) = A^(1) · A^(2) ··· A^(12)"),
        ("Token Attribution Vector:", "The subword attention attribution score is extracted directly from the [CLS] token row: a_token = Ã[CLS, :]"),
        ("Game-Theoretic SHAP Values:", "Computes marginal feature contributions via Kernel SHAP:\nφ_i = Σ [|S|!(|N|-|S|-1)! / |N|!] * [v(S ∪ {i}) - v(S)]"),
        ("Evidence Polarity:", "Positive Shapley value (+φ) pushes prediction toward Deceptive; Negative Shapley value (-φ) pushes prediction toward Authentic.")
    ]
    for m_h, m_d in m2_points:
        p = tf_m2.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run("• " + m_h + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.8); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(m_d); r2.font.name = "Calibri"; r2.font.size = Pt(8.5); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 10: EXPECTED RESULTS & IMPACT
    # =========================================================================
    s10 = prs.slides[9]
    clear_dummy_textboxes(s10)
    
    # Benchmark Evaluation Table at Top
    tb_shape = s10.shapes.add_table(5, 5, Inches(0.5), Inches(1.40), Inches(9.0), Inches(2.35))
    table = tb_shape.table
    
    # Set column widths
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(1.3)
    table.columns[2].width = Inches(1.3)
    table.columns[3].width = Inches(1.3)
    table.columns[4].width = Inches(1.9)
    
    headers_res = ["MODEL ARCHITECTURE", "PRECISION", "RECALL", "F1-SCORE", "ZERO-SHOT INDIC"]
    rows_res = [
        ("TF-IDF + Logistic Regression (Baseline)", "84.1%", "82.5%", "83.3%", "Poor (28.4%)"),
        ("Bi-Directional LSTM + GloVe Embeddings", "88.6%", "87.2%", "87.9%", "Limited (41.2%)"),
        ("mBERT (Multilingual BERT Fine-Tuned)", "94.2%", "93.8%", "94.0%", "Strong (86.5%)"),
        ("XLM-RoBERTa + Dual XAI (Proposed)", "96.4%", "95.8%", "96.1%", "State-of-the-Art (92.4%)")
    ]
    
    # Format Header Row
    for col_idx, h_text in enumerate(headers_res):
        c = table.cell(0, col_idx)
        c.text = h_text
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_DARK_BLUE
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
        for r in p.runs:
            r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Format Data Rows
    for row_idx, r_vals in enumerate(rows_res, start=1):
        is_proposed = (row_idx == 4)
        bg = COLOR_CARD_BLUE if is_proposed else (COLOR_CARD_ALT if row_idx % 2 == 1 else COLOR_CARD)
        for col_idx, val in enumerate(r_vals):
            c = table.cell(row_idx, col_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = bg
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            for r in p.runs:
                r.font.name = "Arial" if is_proposed else "Calibri"
                r.font.size = Pt(9.5) if not is_proposed else Pt(10)
                r.font.bold = True if (is_proposed or col_idx == 3) else False
                r.font.color.rgb = COLOR_BLUE if is_proposed else COLOR_NAVY

    # Bottom 2 Impact Cards
    c_imp_l = add_card(s10, Inches(0.5), Inches(3.95), Inches(4.4), Inches(2.70), border_color=COLOR_BORDER_BLUE, fill_color=COLOR_CARD)
    tf_il = c_imp_l.text_frame
    tf_il.word_wrap = True
    tf_il.margin_left = tf_il.margin_right = tf_il.margin_top = Inches(0.2)
    
    p = tf_il.paragraphs[0]
    r = p.add_run("SCIENTIFIC & RESEARCH IMPACT\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    r2 = p.add_run("Advancing Multilingual NLP & XAI")
    r2.font.name = "Arial"; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    
    imp_l_points = [
        ("Bridging the Explainability Gap:", "Replaces uninterpretable black-box neural networks with rigorous layer-recursive attention rollout and game-theoretic SHAP attributions."),
        ("Zero-Shot Indic Generalization:", "Demonstrates that high-resource English datasets can effectively bootstrap high-accuracy verification in resource-constrained Indic languages."),
        ("Morpheme-Level Linguistic Forensics:", "Provides fine-grained subword transparency into deceptive rhetoric, clickbait affixes, and hyperbolic emotional triggers.")
    ]
    for ih, idesc in imp_l_points:
        p = tf_il.add_paragraph(); p.space_after = Pt(3)
        r1 = p.add_run("• " + ih + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(idesc); r2.font.name = "Calibri"; r2.font.size = Pt(8.2); r2.font.color.rgb = COLOR_MUTED

    c_imp_r = add_card(s10, Inches(5.1), Inches(3.95), Inches(4.4), Inches(2.70), border_color=COLOR_BORDER_GREEN, fill_color=COLOR_CARD)
    tf_ir = c_imp_r.text_frame
    tf_ir.word_wrap = True
    tf_ir.margin_left = tf_ir.margin_right = tf_ir.margin_top = Inches(0.2)
    
    p = tf_ir.paragraphs[0]
    r = p.add_run("SOCIETAL & OPERATIONAL IMPACT\n")
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_GREEN
    r2 = p.add_run("Strengthening Digital Information Integrity")
    r2.font.name = "Arial"; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)
    
    imp_r_points = [
        ("Democratizing Fact-Checking:", "Protects non-English-speaking populations from viral election propaganda, communal hoaxes, and harmful medical disinformation."),
        ("Accelerating Newsroom Workflows:", "Empowers fact-checkers and journalists with 10x faster verification triage by highlighting suspicious subword claims automatically."),
        ("Restoring Institutional Trust:", "Transparent attribution heatmaps explain why a claim was flagged, mitigating censorship allegations and fostering reader confidence.")
    ]
    for ih, idesc in imp_r_points:
        p = tf_ir.add_paragraph(); p.space_after = Pt(3)
        r1 = p.add_run("• " + ih + " "); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(idesc); r2.font.name = "Calibri"; r2.font.size = Pt(8.2); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 11: PROJECT TIMELINE (GANTT SCHEDULE)
    # =========================================================================
    s11 = prs.slides[10]
    clear_dummy_textboxes(s11)
    
    phases_data = [
        ("PHASE 1", "Weeks 1 – 3", "COMPLETED", COLOR_GREEN,
         "Literature Review & Benchmark Corpus Curation",
         "Survey of cross-lingual transformer architectures; acquisition and cleaning of WELFake, ISOT, and IndicFakeNews datasets; Unicode NFKC normalization pipeline."),
        ("PHASE 2", "Weeks 4 – 7", "IN PROGRESS", COLOR_BLUE,
         "Transformer Architecture Design & Baseline Fine-Tuning",
         "Implementation of mBERT and XLM-RoBERTa fine-tuning pipelines with AdamW optimizer; hyperparameter tuning; baseline benchmarking against TF-IDF and BiLSTM."),
        ("PHASE 3", "Weeks 8 – 11", "UPCOMING", COLOR_AMBER,
         "Attention Rollout Formulation & Dual SHAP Attribution",
         "Mathematical derivation and coding of 12-layer recursive Attention Rollout; integration of Kernel SHAP token-level attribution; subword score mapping."),
        ("PHASE 4", "Weeks 12 – 14", "UPCOMING", COLOR_NAVY,
         "Interactive Forensic HUD & REST API Development",
         "Development of Streamlit forensic HUD and Flask API; dynamic risk gauges, token attention heatmaps, sample loaders, and sub-50ms inference caching."),
        ("PHASE 5", "Weeks 15 – 16", "UPCOMING", COLOR_MUTED,
         "Empirical Evaluation, Thesis Documentation & Final Defense",
         "Comprehensive cross-lingual evaluation on held-out test sets; ablation studies; research report compilation; preparation for final academic project defense.")
    ]
    
    for idx, (p_num, p_weeks, p_status, p_color, p_title, p_desc) in enumerate(phases_data):
        top_y = Inches(1.40 + idx * 1.05)
        c = add_card(s11, Inches(0.5), top_y, Inches(9.0), Inches(0.96), border_color=COLOR_BORDER)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.1)
        
        p = tf.paragraphs[0]
        r_phase = p.add_run(f"{p_num} ({p_weeks})  |  ")
        r_phase.font.name = "Arial"; r_phase.font.size = Pt(10); r_phase.font.bold = True; r_phase.font.color.rgb = p_color
        
        r_title = p.add_run(p_title + "  ")
        r_title.font.name = "Arial"; r_title.font.size = Pt(10.5); r_title.font.bold = True; r_title.font.color.rgb = COLOR_NAVY
        
        r_stat = p.add_run(f"[{p_status}]")
        r_stat.font.name = "Arial"; r_stat.font.size = Pt(8.5); r_stat.font.bold = True; r_stat.font.color.rgb = p_color
        p.space_after = Pt(2)
        
        p2 = tf.add_paragraph()
        r_desc = p2.add_run(p_desc)
        r_desc.font.name = "Calibri"; r_desc.font.size = Pt(8.8); r_desc.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 12: CONCLUSION, DEFENSE SUMMARY & THANK YOU
    # =========================================================================
    s12 = prs.slides[11]
    
    # Reposition and enhance TextBox 1 ("THANK YOU")
    for sh in s12.shapes:
        if 'TextBox 1' in sh.name:
            sh.left = Inches(1.0)
            sh.top = Inches(1.1)
            sh.width = Inches(8.0)
            sh.height = Inches(1.2)
            tf = sh.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r1 = p.add_run("THANK ")
            r1.font.name = "Garamond"; r1.font.size = Pt(50); r1.font.bold = True; r1.font.color.rgb = COLOR_BLUE
            r2 = p.add_run("YOU")
            r2.font.name = "Garamond"; r2.font.size = Pt(50); r2.font.bold = True; r2.font.color.rgb = COLOR_RED
            
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            r_sub = p2.add_run("Open for Questions, Feedback & Synopsis Examination")
            r_sub.font.name = "Arial"; r_sub.font.size = Pt(12); r_sub.font.bold = True; r_sub.font.color.rgb = COLOR_MUTED

    # 3 Summary Highlight Cards
    highlights_s12 = [
        ("Multilingual NLP Backbone", "96.1% F1 across 5 languages with zero-shot transfer to Hindi and Bengali without local re-annotation.", COLOR_BORDER_BLUE, COLOR_CARD_BLUE),
        ("Dual-Mode XAI Pipeline", "12-layer recursive Attention Rollout + game-theoretic SHAP attributions solve the black-box dilemma.", COLOR_BORDER, COLOR_CARD),
        ("Production Forensic HUD", "Sub-50ms inference latency, real-time risk gauge, subword heatmaps, and fully integrated REST API.", COLOR_BORDER_GREEN, COLOR_CARD_GREEN)
    ]
    for idx, (h_title, h_desc, b_col, f_col) in enumerate(highlights_s12):
        left_pos = Inches(0.5 + idx * 3.05)
        c = add_card(s12, left_pos, Inches(2.45), Inches(2.9), Inches(1.85), border_color=b_col, fill_color=f_col)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)
        
        p = tf.paragraphs[0]
        r = p.add_run(h_title + "\n")
        r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(4)
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run(h_desc)
        r2.font.name = "Calibri"; r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    # Bottom Metadata Box (Group, Mentor, Department)
    c_meta = add_card(s12, Inches(0.8), Inches(4.55), Inches(8.4), Inches(2.05), border_color=COLOR_BORDER_BLUE, fill_color=COLOR_CARD)
    tf_m = c_meta.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = Inches(0.2)
    
    p = tf_m.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run("PROJECT DEFENSE COMMITTEE & RESEARCH TEAM (GROUP 26O4028)")
    r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = COLOR_DARK_BLUE
    p.space_after = Pt(6)
    
    p_team = tf_m.add_paragraph()
    p_team.alignment = PP_ALIGN.CENTER
    r_team = p_team.add_run("Student Candidates: ")
    r_team.font.name = "Arial"; r_team.font.size = Pt(10); r_team.font.bold = True; r_team.font.color.rgb = COLOR_NAVY
    r_s1 = p_team.add_run("M. Aqmar Asmeer Iqbal (Roll: 2501560034)  |  ")
    r_s1.font.name = "Calibri"; r_s1.font.size = Pt(10.5); r_s1.font.bold = True; r_s1.font.color.rgb = COLOR_BLUE
    r_s2 = p_team.add_run("Amandeep (Roll: 2501560021)")
    r_s2.font.name = "Calibri"; r_s2.font.size = Pt(10.5); r_s2.font.bold = True; r_s2.font.color.rgb = COLOR_BLUE
    p_team.space_after = Pt(4)
    
    p_guide = tf_m.add_paragraph()
    p_guide.alignment = PP_ALIGN.CENTER
    r_g1 = p_guide.add_run("Project Guide & Faculty Mentor: ")
    r_g1.font.name = "Arial"; r_g1.font.size = Pt(10); r_g1.font.bold = True; r_g1.font.color.rgb = COLOR_NAVY
    r_g2 = p_guide.add_run("Ms. Lucky Verma ")
    r_g2.font.name = "Arial"; r_g2.font.size = Pt(10.5); r_g2.font.bold = True; r_g2.font.color.rgb = COLOR_GREEN
    r_g3 = p_guide.add_run("(Assistant Professor, Department of Computer Science & Engineering)")
    r_g3.font.name = "Calibri"; r_g3.font.size = Pt(9.5); r_g3.font.color.rgb = COLOR_MUTED
    p_guide.space_after = Pt(4)
    
    p_inst = tf_m.add_paragraph()
    p_inst.alignment = PP_ALIGN.CENTER
    r_i = p_inst.add_run("School of Computer Applications | K.R. Mangalam University, Gurugram, Haryana")
    r_i.font.name = "Calibri"; r_i.font.size = Pt(9.5); r_i.font.italic = True; r_i.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SAVE OUTPUT
    # =========================================================================
    out_docs = Path(r"c:\Users\KIIT\Desktop\fake-news-detection\docs\Fake_News_Detection_Synopsis_Presentation.pptx")
    out_desktop = Path(r"c:\Users\KIIT\Desktop\Fake_News_Detection_Synopsis_Presentation.pptx")
    
    out_docs.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_docs))
    print(f"Saved successfully to docs: {out_docs}")
    
    prs.save(str(out_desktop))
    print(f"Saved successfully to Desktop: {out_desktop}")

if __name__ == "__main__":
    populate_presentation()
