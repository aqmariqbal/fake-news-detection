import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.text.text import _Paragraph

# Patch _Paragraph.add_run to seamlessly support passing text directly
_orig_add_run = _Paragraph.add_run
def _patched_add_run(self, text=None):
    r = _orig_add_run(self)
    if text is not None:
        r.text = str(text)
    return r
_Paragraph.add_run = _patched_add_run

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Palette
    BG_CANVAS = RGBColor(248, 250, 252)       # #F8FAFC Off-white
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # #0F172A Dark Navy
    COLOR_BLUE = RGBColor(37, 99, 235)        # #2563EB Royal / Electric Blue
    COLOR_GREEN = RGBColor(5, 150, 105)       # #059669 Emerald Green
    COLOR_RED = RGBColor(220, 38, 38)         # #DC2626 Crimson Red
    COLOR_MUTED = RGBColor(71, 85, 105)       # #475569 Slate Muted
    COLOR_CARD = RGBColor(255, 255, 255)      # Pure White Card
    COLOR_BORDER = RGBColor(226, 232, 240)    # #E2E8F0
    COLOR_BORDER_BLUE = RGBColor(191, 219, 254)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_CANVAS
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_tag="MCA FINAL YEAR SYNOPSIS DEFENSE", slide_num=None, total_slides=12):
        set_slide_background(slide)
        
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
        p_tag = tf_tag.paragraphs[0]
        r_tag = p_tag.add_run()
        r_tag.text = category_tag.upper()
        r_tag.font.name = "Arial"
        r_tag.font.size = Pt(9.5)
        r_tag.font.bold = True
        r_tag.font.color.rgb = COLOR_BLUE

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.5), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title_text
        r.font.name = "Arial"
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY

        # Decorative bottom rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

        # Slide Number Badge
        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.55), Inches(1.0), Inches(0.4))
            tf_num = num_box.text_frame
            tf_num.margin_top = tf_num.margin_bottom = tf_num.margin_left = tf_num.margin_right = 0
            p_num = tf_num.paragraphs[0]
            p_num.alignment = PP_ALIGN.RIGHT
            r_num = p_num.add_run()
            r_num.text = f"{slide_num:02d} / {total_slides:02d}"
            r_num.font.name = "Arial"
            r_num.font.size = Pt(11)
            r_num.font.bold = True
            r_num.font.color.rgb = COLOR_MUTED

    def add_card(slide, left, top, width, height, border_color=COLOR_BORDER, fill_color=COLOR_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent Top Banner
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_BLUE
    top_bar.line.fill.background()

    # Academic Pill Tag
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.9), Inches(4.5), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(238, 242, 255)
    pill.line.color.rgb = COLOR_BORDER_BLUE
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.alignment = PP_ALIGN.CENTER
    r_pill = p_pill.add_run()
    r_pill.text = "MCA FINAL YEAR PROJECT SYNOPSIS DEFENSE"
    r_pill.font.name = "Arial"
    r_pill.font.size = Pt(10)
    r_pill.font.bold = True
    r_pill.font.color.rgb = COLOR_BLUE

    # Title & Subtitle Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = "Transformer-Based Multilingual Fake News Detection System with Attention-Based Explainability (XAI)"
    r_t.font.name = "Arial"
    r_t.font.size = Pt(26)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    p_t.space_after = Pt(12)

    p_sub = tf_t.add_paragraph()
    r_sub = p_sub.add_run()
    r_sub.text = "Cross-Lingual Deep Contextual Representation, Multi-Head Attention Rollout & Token-Level SHAP Attribution"
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    # Metadata Grid Cards (Bottom Half)
    card_author = add_card(s1, Inches(1.0), Inches(4.1), Inches(3.6), Inches(2.5))
    tf_a = card_author.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = Inches(0.25)
    p = tf_a.paragraphs[0]
    r = p.add_run("SUBMITTED BY (GROUP 26O4028)")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(8)
    
    p = tf_a.add_paragraph()
    r = p.add_run("• M. Aqmar Asmeer Iqbal")
    r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY
    p = tf_a.add_paragraph()
    r = p.add_run("   Roll No: 2501560034 (Lead Researcher)")
    r.font.name = "Calibri"; r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED
    p.space_after = Pt(6)

    p = tf_a.add_paragraph()
    r = p.add_run("• Amandeep")
    r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY
    p = tf_a.add_paragraph()
    r = p.add_run("   Roll No: 2501560021 (Co-Researcher)")
    r.font.name = "Calibri"; r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED

    card_mentor = add_card(s1, Inches(4.85), Inches(4.1), Inches(3.6), Inches(2.5))
    tf_m = card_mentor.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = Inches(0.25)
    p = tf_m.paragraphs[0]
    r = p.add_run("FACULTY MENTORSHIP")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(8)

    p = tf_m.add_paragraph()
    r = p.add_run("Ms. Lucky Verma")
    r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY
    p = tf_m.add_paragraph()
    r = p.add_run("Assistant Professor & Project Guide")
    r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = COLOR_MUTED
    p.space_after = Pt(8)
    p = tf_m.add_paragraph()
    r = p.add_run("Specialization: Natural Language Processing, Machine Learning & Deep Learning Architectures")
    r.font.name = "Calibri"; r.font.size = Pt(9); r.font.italic = True; r.font.color.rgb = COLOR_MUTED

    card_inst = add_card(s1, Inches(8.7), Inches(4.1), Inches(3.6), Inches(2.5))
    tf_i = card_inst.text_frame
    tf_i.word_wrap = True
    tf_i.margin_left = tf_i.margin_right = tf_i.margin_top = Inches(0.25)
    p = tf_i.paragraphs[0]
    r = p.add_run("ACADEMIC INSTITUTION")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(8)

    p = tf_i.add_paragraph()
    r = p.add_run("Department of Computer Science & Engineering")
    r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY
    p = tf_i.add_paragraph()
    r = p.add_run("School of Computer Applications")
    r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = COLOR_MUTED
    p.space_after = Pt(8)
    p = tf_i.add_paragraph()
    r = p.add_run("Master of Computer Applications (MCA)\nAcademic Year: 2025 – 2026")
    r.font.name = "Calibri"; r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Project Overview & Problem Formulation", slide_num=2)

    # 3 Column Cards: Problem, Prior Limitations, Proposed Solution
    c1 = add_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1))
    tf1 = c1.text_frame; tf1.word_wrap = True; tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.25)
    p = tf1.paragraphs[0]; r = p.add_run("🚨 1. Problem Statement"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_RED; p.space_after = Pt(10)
    
    bullets_p1 = [
        ("Information Disorder:", "Coordinated disinformation campaigns exploit regional language ecosystems during public crises, health emergencies, and elections."),
        ("Linguistic Scarcity:", "High-resource languages (English) enjoy mature NLP verification toolchains, while regional Indo-Aryan languages (Hindi, Bengali) suffer from a lack of labeled verification resources."),
        ("Real-World Impact:", "Viral misinformation rapidly erodes democratic institutions and public trust without automated real-time intervention.")
    ]
    for b_title, b_desc in bullets_p1:
        p = tf1.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + b_title + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(b_desc); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    c2 = add_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1))
    tf2 = c2.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)
    p = tf2.paragraphs[0]; r = p.add_run("⚠️ 2. Prior System Limitations"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(10)

    bullets_p2 = [
        ("Monolingual Silos:", "Existing commercial filters operate almost exclusively in English, failing completely on code-mixed and non-Latin scripts."),
        ("Black-Box Opacity:", "Deep neural networks predict binary labels without explaining why a statement was flagged, prompting user skepticism and claims of censorship."),
        ("Superficial Heuristics:", "Traditional keyword blacklists fail to detect subtle contextual hyperbole, satirical deception, and paraphrased claims.")
    ]
    for b_title, b_desc in bullets_p2:
        p = tf2.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + b_title + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(b_desc); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    c3 = add_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1), border_color=COLOR_BORDER_BLUE, fill_color=RGBColor(240, 249, 255))
    tf3 = c3.text_frame; tf3.word_wrap = True; tf3.margin_left = tf3.margin_right = tf3.margin_top = Inches(0.25)
    p = tf3.paragraphs[0]; r = p.add_run("💡 3. Proposed Solution"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(10)

    bullets_p3 = [
        ("Cross-Lingual Transformers:", "Leverages pre-trained mBERT & XLM-RoBERTa for zero-shot cross-lingual transfer across 5 major languages."),
        ("Multi-Head Attention Rollout:", "Recursively computes attention flow across all 12 transformer encoder layers down to subword token spans."),
        ("Token-Level SHAP Attributions:", "Quantifies directional feature importance (+ pushes Fake, - pushes Real) for forensic transparency."),
        ("Interactive Forensic HUD:", "A clean, responsive dashboard displaying verified confidence scores, lexical density, and subword heatmaps.")
    ]
    for b_title, b_desc in bullets_p3:
        p = tf3.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + b_title + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_BLUE
        r2 = p.add_run(b_desc); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 3: SPECIFIC OBJECTIVES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Specific Project Objectives", slide_num=3)

    objectives = [
        ("Objective 1: Multilingual Deep Learning Backbone",
         "Fine-tune pre-trained contextual multilingual transformer models (mBERT and XLM-RoBERTa) on multi-domain benchmark corpora across 5 languages: English, Hindi, Bengali, Spanish, and French, establishing robust cross-lingual feature representations."),
        ("Objective 2: Formulation of Attention Rollout Algorithm",
         "Design and implement an Attention Rollout algorithm that tracks and aggregates self-attention matrices recursively through all 12 encoder layers, directly mapping self-attention flow to subword token spans without layer-collapse."),
        ("Objective 3: Dual-Mode SHAP Attribution Integration",
         "Integrate Kernel and Tree SHAP token-level attribution to quantify the marginal directional contribution of each word (+ pushes Deceptive/Fake, - pushes Authentic/Real), validating self-attention distributions against game-theoretic ground truth."),
        ("Objective 4: Production-Grade Forensic Web Dashboard",
         "Develop a real-time web interface (Streamlit & Flask) featuring instant pre-loaded sample selectors, dynamic risk gauge, subword token heatmaps, vocabulary density calculations, and sub-50ms inference latency.")
    ]

    for idx, (obj_title, obj_desc) in enumerate(objectives):
        top_y = Inches(1.7 + idx * 1.3)
        c = add_card(s3, Inches(0.8), top_y, Inches(11.733), Inches(1.15))
        tf = c.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.15)
        
        p = tf.paragraphs[0]
        r_num = p.add_run(f"0{idx+1}  |  ")
        r_num.font.name = "Arial"; r_num.font.size = Pt(13); r_num.font.bold = True; r_num.font.color.rgb = COLOR_BLUE
        r_head = p.add_run(obj_title)
        r_head.font.name = "Arial"; r_head.font.size = Pt(12); r_head.font.bold = True; r_head.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        r_body = p2.add_run(obj_desc)
        r_body.font.name = "Calibri"; r_body.font.size = Pt(10); r_body.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 4: KEY FEATURES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Key Architectural Features & Innovation", slide_num=4)

    features = [
        ("🌐 Zero-Shot Cross-Lingual Transfer",
         "Transfers rich semantic representations trained on high-resource English datasets directly to Indian regional languages (Hindi, Bengali) without requiring manual re-annotation for each language."),
        ("🔍 Subword-Level Interpretability",
         "Bypasses coarse sentence-level classifications by projecting attention weights directly onto SentencePiece and BPE subword tokens, exposing specific hyperbolic stems and clickbait affixes."),
        ("⚖️ Dual-Mode XAI Validation",
         "Combines intrinsic self-attention matrices (Attention Rollout) with extrinsic marginal feature perturbation (SHAP attributions), preventing misleading attention artifacts and hallucinated rationales."),
        ("⚡ High-Speed Forensic HUD",
         "Features an ultra-responsive interface with non-blocking model pre-warming, instantaneous sample loading from archive, vocabulary match density indicators, and sub-20ms runtime execution.")
    ]

    for i, (f_title, f_desc) in enumerate(features):
        col = i % 2
        row = i // 2
        left_x = Inches(0.8 + col * 5.95)
        top_y = Inches(1.7 + row * 2.65)
        
        c = add_card(s4, left_x, top_y, Inches(5.75), Inches(2.45))
        tf = c.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)
        p = tf.paragraphs[0]
        r = p.add_run(f_title)
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        r2 = p2.add_run(f_desc)
        r2.font.name = "Calibri"; r2.font.size = Pt(10.5); r2.font.color.rgb = COLOR_MUTED; p2.space_after = Pt(6)

    # =========================================================================
    # SLIDE 5: PROJECT USE CASES & SCOPE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Project Use Cases & Operational Scope", slide_num=5)

    # Left: Direct Use Cases (2/3 width)
    c_left = add_card(s5, Inches(0.8), Inches(1.7), Inches(7.5), Inches(5.1))
    tf_l = c_left.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.3)
    p = tf_l.paragraphs[0]; r = p.add_run("🎯 Target Applications & Direct Use Cases"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(10)

    use_cases = [
        ("Automated Social Feed Pre-Moderation:", "Integrates into regional content ingestion pipelines (Twitter/X, WhatsApp forwards, Facebook posts) to flag suspicious viral claims prior to mass diffusion."),
        ("Journalistic Fact-Checking Workbench:", "Provides investigative journalists and intelligence desks with token-level explainability heatmaps, showing exact deceptive phrases triggering suspicion."),
        ("Browser Authentication Plugins:", "Powers client-side web extensions to display real-time credibility scores and vocabulary density warnings directly over news articles as citizens browse."),
        ("Civic & Public Health Advisory Portals:", "Enables government monitoring cells to track emergent health and financial disinformation in Hindi and Bengali across decentralized messaging.")
    ]
    for uc_t, uc_d in use_cases:
        p = tf_l.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + uc_t + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(uc_d); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    # Right: Scope Boundaries (1/3 width)
    c_right = add_card(s5, Inches(8.55), Inches(1.7), Inches(4.0), Inches(5.1), fill_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tf_r = c_right.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.3)
    p = tf_r.paragraphs[0]; r = p.add_run("🛡️ Scope Boundaries & Constraints"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_RED; p.space_after = Pt(10)

    scope_items = [
        ("Within Project Scope:", "Linguistic, contextual, stylistic, and semantic pattern analysis of multilingual textual claims; subword attention rollout and SHAP token ranking."),
        ("Explicit Non-Scope:", "Live automated dynamic web scraping (governed by robots.txt policies) and multi-modal deepfake image/video forensic detection."),
        ("Future Roadmap:", "Multimodal vision-language fusion (CLIP/BLIP-2) and knowledge-graph grounding with Wikidata entities for real-time external fact verification.")
    ]
    for s_t, s_d in scope_items:
        p = tf_r.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + s_t + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_RED
        r2 = p.add_run(s_d); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 6: SYSTEM ARCHITECTURE & FLOW DIAGRAM
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "System Architecture & Processing Pipeline", slide_num=6)

    # Monospace Architecture Box
    c_flow = add_card(s6, Inches(0.8), Inches(1.7), Inches(11.733), Inches(4.1), fill_color=RGBColor(15, 23, 42), border_color=COLOR_PRIMARY)
    tf_flow = c_flow.text_frame; tf_flow.word_wrap = True; tf_flow.margin_left = tf_flow.margin_right = tf_flow.margin_top = Inches(0.3)
    
    ascii_arch = """
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           RAW MULTILINGUAL INPUT (English, Hindi, Bengali, Spanish, French)                      │
└────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                 PREPROCESSING & TOKENIZATION LAYER (Unicode Normalization, Script Regex, BPE/SentencePiece)     │
└────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│             CROSS-LINGUAL TRANSFORMER ENCODER (mBERT / XLM-RoBERTa: 12 Layers, 768 Hidden Dim, 12 Heads)       │
└───────────────────────────────┬─────────────────────────────────────────────────┬───────────────────────────────┘
                                │                                                 │
                                ▼                                                 ▼
┌──────────────────────────────────────────────────────────────┐ ┌────────────────────────────────────────────────┐
│               CLASSIFICATION HEAD (Feed-Forward)             │ │           DUAL EXPLAINABILITY ENGINE (XAI)     │
│   • Logit Calculation: z = W^T h_[CLS] + b                   │ │   • Multi-Head Attention Rollout Algorithm     │
│   • Sigmoid Probability: P(FAKE) vs P(REAL)                  │ │   • Token-Level SHAP Marginal Attributions     │
└───────────────────────────────┬──────────────────────────────┘ └────────────────────────┬───────────────────────┘
                                │                                                 │
                                └────────────────────────┬────────────────────────┘
                                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│               INTERACTIVE FORENSIC USER INTERFACE (Streamlit Dashboard & RESTful Flask API)                     │
│    🟢 VERIFIED / 🔴 FAKE Verdict Banner  │  Confidence Progress Bar  │  Subword Heatmaps  │  Metadata Latency   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    """
    p = tf_flow.paragraphs[0]
    p.space_after = Pt(0)
    r = p.add_run(ascii_arch.strip())
    r.font.name = "Consolas"; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(226, 232, 240)

    # Pipeline summary below
    c_summary = add_card(s6, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.9), fill_color=RGBColor(241, 245, 249))
    tf_s = c_summary.text_frame; tf_s.word_wrap = True; tf_s.margin_left = Inches(0.25); tf_s.margin_top = Inches(0.12)
    p = tf_s.paragraphs[0]
    r = p.add_run("Key Architectural Property: ")
    r.font.bold = True; r.font.color.rgb = COLOR_BLUE; r.font.size = Pt(10.5)
    r2 = p.add_run("Dual-branch execution decouples the low-latency classification head (<5ms) from the post-hoc explainability modules, ensuring the user interface remains responsive and fluid.")
    r2.font.size = Pt(10); r2.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 7: SYSTEM IMPLEMENTATION & LIVE WEB INTERFACE DEMONSTRATION
    # =========================================================================
    s_demo = prs.slides.add_slide(blank_layout)
    add_header(s_demo, "System Implementation & Interactive Web Application Demonstration", slide_num=7, total_slides=12)

    # Left: Webpage Screenshot Card with Drop Shadow & Browser Mockup
    c_img_card = add_card(s_demo, Inches(0.8), Inches(1.68), Inches(6.8), Inches(5.2), border_color=COLOR_BORDER_BLUE, fill_color=RGBColor(255, 255, 255))
    
    screenshot_path = Path(r"c:\Users\KIIT\Desktop\fake-news-detection\docs\webpage_presentation_mockup.png")
    if screenshot_path.exists():
        s_demo.shapes.add_picture(str(screenshot_path), Inches(0.92), Inches(1.8), Inches(6.56), Inches(4.96))

    # Right: Technical System Capabilities Cards
    c_feat1 = add_card(s_demo, Inches(7.8), Inches(1.68), Inches(4.733), Inches(2.7))
    tf_f1 = c_feat1.text_frame; tf_f1.word_wrap = True; tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = Inches(0.22)
    p = tf_f1.paragraphs[0]; r = p.add_run("🖥️ Forensic Full-Stack Architecture"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(6)
    
    f1_items = [
        ("Streamlit & Flask Microservices:", "Interactive browser UI backed by an asynchronous Python RESTful API (/predict, /upload_media)."),
        ("Multi-Modal Document Parsing:", "Automated OCR and native parsers supporting PDF, DOCX, PPTX, and image screenshots (.png, .jpg)."),
        ("16+ Multilingual Support:", "Real-time fact & news verification across English, Hindi, Bengali, Odia, French, Spanish, German, Japanese, etc.")
    ]
    for ft, fd in f1_items:
        p = tf_f1.add_paragraph(); p.space_after = Pt(4)
        r = p.add_run("• " + ft + " "); r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(fd); r2.font.size = Pt(9); r2.font.color.rgb = COLOR_MUTED

    c_feat2 = add_card(s_demo, Inches(7.8), Inches(4.5), Inches(4.733), Inches(2.38), fill_color=RGBColor(240, 253, 250), border_color=RGBColor(167, 243, 208))
    tf_f2 = c_feat2.text_frame; tf_f2.word_wrap = True; tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = Inches(0.22)
    p = tf_f2.paragraphs[0]; r = p.add_run("⚡ Real-Time Diagnostic Dashboard"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_GREEN; p.space_after = Pt(6)

    f2_items = [
        ("Instant Credibility Verdict:", "High-contrast dynamic banner displaying VERIFIED (Green) vs. FAKE (Red) with calibrated probability score."),
        ("Subword Stylometric Diagnostics:", "Live calculation of token count, vocabulary density (TTR), language code, and stylistic markers."),
        ("Sub-10ms Inference Latency:", "Non-blocking background pre-warming guarantees instantaneous response on consumer hardware.")
    ]
    for ft, fd in f2_items:
        p = tf_f2.add_paragraph(); p.space_after = Pt(4)
        r = p.add_run("• " + ft + " "); r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(fd); r2.font.size = Pt(9); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 8: DATA & RESOURCES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Datasets, Resources & Computational Environment", slide_num=8, total_slides=12)

    # 3 Cards: Datasets, Software, Hardware
    c_data = add_card(s8, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.1))
    tf_d = c_data.text_frame; tf_d.word_wrap = True; tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = Inches(0.25)
    p = tf_d.paragraphs[0]; r = p.add_run("📊 Benchmark Datasets"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(10)

    d_items = [
        ("Multilingual Corpora:", "Curated datasets including LIAR (political claims), FakeNewsNet, and cross-lingual Indo-Aryan fake news datasets."),
        ("Language Distribution:", "Balanced sampling across English (40%), Hindi (25%), Bengali (20%), Spanish (10%), and French (5%)."),
        ("Splitting Strategy:", "Rigorous stratified split: 70% Training, 15% Validation, and 15% Holdout Testing."),
        ("Label Balance:", "50:50 distribution of verified authentic news versus confirmed deceptive/clickbait claims.")
    ]
    for dt, dd in d_items:
        p = tf_d.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + dt + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(dd); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    c_soft = add_card(s8, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.1))
    tf_so = c_soft.text_frame; tf_so.word_wrap = True; tf_so.margin_left = tf_so.margin_right = tf_so.margin_top = Inches(0.25)
    p = tf_so.paragraphs[0]; r = p.add_run("💻 Software & Frameworks"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(10)

    s_items = [
        ("Deep Learning Core:", "PyTorch 2.2+ with CUDA acceleration for model tensor operations and backward pass."),
        ("Hugging Face Suite:", "Transformers library for pretrained mBERT & XLM-RoBERTa weights and tokenizers."),
        ("Explainability Tooling:", "SHAP (KernelSHAP & TreeSHAP), Captum for PyTorch gradient attribution."),
        ("Serving & UI:", "Streamlit, Flask 2.2+, Plotly for interactive waterfall charts, Scikit-Learn for baseline benchmarking.")
    ]
    for st, sd in s_items:
        p = tf_so.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + st + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_BLUE
        r2 = p.add_run(sd); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    c_hard = add_card(s8, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.1))
    tf_h = c_hard.text_frame; tf_h.word_wrap = True; tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = Inches(0.25)
    p = tf_h.paragraphs[0]; r = p.add_run("⚡ Hardware Infrastructure"); r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_GREEN; p.space_after = Pt(10)

    h_items = [
        ("GPU Compute:", "NVIDIA RTX 40-Series / Cloud-hosted Tesla T4 with 16 GB VRAM and Mixed Precision (FP16)."),
        ("CPU Environment:", "Intel Core i7 / AMD Ryzen 8-core CPU with 16 GB System RAM for asynchronous preprocessing."),
        ("Storage Subsystem:", "High-speed NVMe SSD storage for low-latency serialization of checkpoints and pickled pipelines."),
        ("Edge Deployability:", "Optimized inference pipeline tested on standard consumer laptops (<25ms CPU latency).")
    ]
    for ht, hd in h_items:
        p = tf_h.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("• " + ht + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_GREEN
        r2 = p.add_run(hd); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 9: METHODOLOGY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Mathematical Methodology & Fine-Tuning Pipeline", slide_num=9, total_slides=12)

    # Top: Preprocessing & Fine-tuning Cards
    c_m1 = add_card(s9, Inches(0.8), Inches(1.7), Inches(5.75), Inches(2.4))
    tf_m1 = c_m1.text_frame; tf_m1.word_wrap = True; tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = Inches(0.25)
    p = tf_m1.paragraphs[0]; r = p.add_run("1. Preprocessing & Script Normalization"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(6)
    bullets_m1 = [
        "Unicode Normalization: NFKC normalization resolving Devanagari (Hindi) and Bengali conjunct characters and zero-width joiners.",
        "Subword Tokenization: Byte-Pair Encoding (BPE) & SentencePiece preserving cross-lingual morphological affixes.",
        "Sequence Window: Truncation and dynamic padding capped at max_seq_length = 512 tokens."
    ]
    for b in bullets_m1:
        p = tf_m1.add_paragraph(); r = p.add_run("• " + b); r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED; p.space_after = Pt(3)

    c_m2 = add_card(s9, Inches(6.78), Inches(1.7), Inches(5.75), Inches(2.4))
    tf_m2 = c_m2.text_frame; tf_m2.word_wrap = True; tf_m2.margin_left = tf_m2.margin_right = tf_m2.margin_top = Inches(0.25)
    p = tf_m2.paragraphs[0]; r = p.add_run("2. Transformer Fine-Tuning Hyperparameters"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(6)
    bullets_m2 = [
        "Loss Objective: Binary Cross-Entropy Loss over pooled [CLS] representations.",
        "Optimization: AdamW with weight decay (0.01) to regularize transformer weights.",
        "Learning Rate: 2e-5 with a linear warmup schedule over the first 10% of total training steps.",
        "Batch Size & Epochs: Batch size of 16 (gradient accumulation = 2) trained across 3-5 epochs."
    ]
    for b in bullets_m2:
        p = tf_m2.add_paragraph(); r = p.add_run("• " + b); r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED; p.space_after = Pt(3)

    # Bottom: Explainability Mathematics Box
    c_m3 = add_card(s9, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.5), fill_color=RGBColor(240, 249, 255), border_color=COLOR_BORDER_BLUE)
    tf_m3 = c_m3.text_frame; tf_m3.word_wrap = True; tf_m3.margin_left = tf_m3.margin_right = tf_m3.margin_top = Inches(0.25)
    p = tf_m3.paragraphs[0]; r = p.add_run("3. Explainability Mathematics: Attention Rollout & SHAP Attribution"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(6)

    m_details = [
        ("Attention Rollout Equation:", "A_rollout = ∏ [0.5 · W_l + 0.5 · I]  for l = 1 ... L  (Recursively accounts for residual connections and inter-layer information mixing across multi-head self-attention matrices)."),
        ("Token SHAP Formulation:", "ϕ_i = ∑ [ |S|!(|F| - |S| - 1)! / |F|! ] · [ f(S ∪ {i}) - f(S) ]  (Measures marginal contribution of token i across all subset coalitions S against an uninformative baseline token)."),
        ("Directional Sign Interpretation:", "Positive (+) SHAP values indicate tokens driving the decision toward FAKE; negative (-) values indicate tokens defending CREDIBILITY / REAL.")
    ]
    for mt, md in m_details:
        p = tf_m3.add_paragraph(); p.space_after = Pt(4)
        r = p.add_run("• " + mt + " "); r.font.bold = True; r.font.size = Pt(10); r.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(md); r2.font.name = "Consolas"; r2.font.size = Pt(9); r2.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 10: EXPECTED RESULTS & IMPACT
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Target Performance Benchmarks & Societal Impact", slide_num=10, total_slides=12)

    # Table of Target Metrics
    tbl_shape = s10.shapes.add_table(rows=4, cols=4, left=Inches(0.8), top=Inches(1.7), width=Inches(11.733), height=Inches(2.0))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(2.8)
    tbl.columns[2].width = Inches(2.8)
    tbl.columns[3].width = Inches(2.933)

    headers = ["Evaluation Metric", "Baseline (TF-IDF + PA)", "mBERT Fine-Tuned", "XLM-RoBERTa (Target)"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(h_text); r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

    data_rows = [
        ("Macro-F1 Score (English)", "88.4%", "91.2%", "93.6% (Target >92%)"),
        ("Macro-F1 (Hindi / Bengali)", "78.2%", "84.5%", "88.1% (Target >87%)"),
        ("XAI Correlation (Spearman ρ)", "N/A (Heuristic)", "0.68", "0.74 (Target >0.70)")
    ]
    for r_idx, row in enumerate(data_rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 0 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            if c_idx > 0: p.alignment = PP_ALIGN.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"; r.font.size = Pt(10)
            if c_idx == 3:
                r.font.bold = True
                r.font.color.rgb = COLOR_GREEN
            elif c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_MUTED

    # Impact Cards below table
    c_imp1 = add_card(s10, Inches(0.8), Inches(4.0), Inches(5.75), Inches(2.8))
    tf_i1 = c_imp1.text_frame; tf_i1.word_wrap = True; tf_i1.margin_left = tf_i1.margin_right = tf_i1.margin_top = Inches(0.25)
    p = tf_i1.paragraphs[0]; r = p.add_run("🌟 Scientific & Technical Contribution"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(8)
    imp_sci = [
        "Proves empirical viability of zero-shot cross-lingual transfer for low-resource Indian languages in combating adversarial fake news.",
        "Demonstrates that multi-head attention rollout strongly aligns with post-hoc SHAP token attribution, validating attention as explanation.",
        "Establishes a unified forensic baseline combining statistical latency (<10ms) with deep transformer representations."
    ]
    for b in imp_sci:
        p = tf_i1.add_paragraph(); r = p.add_run("• " + b); r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED; p.space_after = Pt(4)

    c_imp2 = add_card(s10, Inches(6.78), Inches(4.0), Inches(5.75), Inches(2.8))
    tf_i2 = c_imp2.text_frame; tf_i2.word_wrap = True; tf_i2.margin_left = tf_i2.margin_right = tf_i2.margin_top = Inches(0.25)
    p = tf_i2.paragraphs[0]; r = p.add_run("🌍 Societal Impact & Algorithmic Trust"); r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_GREEN; p.space_after = Pt(8)
    imp_soc = [
        "Democratizes algorithmic transparency: citizens see exactly which phrases triggered deception flags, eliminating perceptions of censorship.",
        "Protects non-English-speaking regional demographics against dangerous health disinformation and viral financial fraud.",
        "Provides human-in-the-loop capability: fact-checkers can audit model reasoning directly in real-time."
    ]
    for b in imp_soc:
        p = tf_i2.add_paragraph(); r = p.add_run("• " + b); r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED; p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 11: PROJECT TIMELINE (GANTT SCHEDULE)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Project Timeline & Execution Milestones (16-Week Schedule)", slide_num=11, total_slides=12)

    phases = [
        ("Phase 1: Research & Preprocessing", "Weeks 1 – 3", "Literature survey on cross-lingual NLP; compilation of multilingual corpora; Unicode script cleaning & diacritic normalization pipelines.", COLOR_PRIMARY),
        ("Phase 2: Transformer Fine-Tuning", "Weeks 4 – 7", "Implementation of baseline classifiers (TF-IDF + PA); fine-tuning mBERT and XLM-RoBERTa; learning rate optimization and loss tracking.", COLOR_BLUE),
        ("Phase 3: Explainability Engineering", "Weeks 8 – 11", "Mathematical formulation of Attention Rollout; integration of Kernel and Tree SHAP token-level attribution modules; correlation validation.", COLOR_PRIMARY),
        ("Phase 4: Full-Stack Interface & Benchmarking", "Weeks 12 – 14", "Development of responsive Streamlit & Flask interfaces; non-blocking background pre-warming; latency profiling; user testing.", COLOR_GREEN),
        ("Phase 5: Documentation & Synopsis Defense", "Weeks 15 – 16", "Comprehensive thesis documentation; ablation analysis; research paper draft preparation for indexed conference submission.", COLOR_PRIMARY)
    ]

    for idx, (p_name, p_weeks, p_desc, p_color) in enumerate(phases):
        top_y = Inches(1.7 + idx * 1.05)
        c = add_card(s11, Inches(0.8), top_y, Inches(11.733), Inches(0.92))
        tf = c.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.25); tf.margin_top = Inches(0.1)
        
        p = tf.paragraphs[0]
        r1 = p.add_run(p_name)
        r1.font.name = "Arial"; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = p_color
        r2 = p.add_run("   |   " + p_weeks)
        r2.font.name = "Arial"; r2.font.size = Pt(10.5); r2.font.bold = True; r2.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        r3 = p2.add_run(p_desc)
        r3.font.name = "Calibri"; r3.font.size = Pt(9.5); r3.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 12: CONCLUSION & Q&A
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Summary, Conclusion & Technical Discussion", slide_num=12, total_slides=12)

    # Left: Conclusion Takeaways
    c_c1 = add_card(s11, Inches(0.8), Inches(1.7), Inches(6.8), Inches(5.1))
    tf_c1 = c_c1.text_frame; tf_c1.word_wrap = True; tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = Inches(0.3)
    p = tf_c1.paragraphs[0]; r = p.add_run("📌 Core Project Takeaways"); r.font.name = "Arial"; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(10)

    concl_points = [
        ("Bridging the Multilingual Divide:", "Demonstrates that state-of-the-art cross-lingual transformers effectively transfer contextual deception patterns from English to low-resource regional languages."),
        ("Demystifying the Deep Learning Black-Box:", "Replaces opaque confidence scores with dual-layer interpretability: Attention Rollout heatmaps and SHAP directional token polarities."),
        ("Practical Production Usability:", "Eliminates server startup stalls via asynchronous background pre-warming, delivering real-time inferences in under 20 milliseconds."),
        ("Academic & Practical Readiness:", "Delivers a robust, documented codebase with one-click launchers, test suites, and empirical benchmarks.")
    ]
    for cp_t, cp_d in concl_points:
        p = tf_c1.add_paragraph(); p.space_after = Pt(8)
        r = p.add_run("✓ " + cp_t + " "); r.font.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = COLOR_GREEN
        r2 = p.add_run(cp_d); r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_MUTED

    # Right: Open for Questions Card
    c_c2 = add_card(s11, Inches(7.85), Inches(1.7), Inches(4.68), Inches(5.1), fill_color=RGBColor(238, 242, 255), border_color=COLOR_BORDER_BLUE)
    tf_c2 = c_c2.text_frame; tf_c2.word_wrap = True; tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = Inches(0.3)
    p = tf_c2.paragraphs[0]; r = p.add_run("💬 Open for Technical Discussion"); r.font.name = "Arial"; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = COLOR_BLUE; p.space_after = Pt(12)

    p = tf_c2.add_paragraph()
    r = p.add_run("Key Topics for Defense Examination:")
    r.font.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

    topics = [
        "Cross-lingual representation transfer across non-Latin scripts.",
        "Mathematical divergence between raw attention and SHAP values.",
        "Handling adversarial vocabulary perturbations and cloaked text.",
        "Latency vs. accuracy trade-offs between TF-IDF and Transformers.",
        "Strategies for edge deployment and quantization (INT8/ONNX)."
    ]
    for top in topics:
        p = tf_c2.add_paragraph(); p.space_after = Pt(4)
        r = p.add_run("• " + top); r.font.size = Pt(9.5); r.font.color.rgb = COLOR_MUTED

    p_end = tf_c2.add_paragraph(); p_end.space_before = Pt(18); p_end.alignment = PP_ALIGN.CENTER
    r_end = p_end.add_run("THANK YOU\nQuestions & Feedback Welcome")
    r_end.font.name = "Arial"; r_end.font.size = Pt(13); r_end.font.bold = True; r_end.font.color.rgb = COLOR_BLUE

    # Save Presentation to Desktop and docs/
    desktop_pptx = Path(r"c:\Users\KIIT\Desktop\Fake_News_Detection_Synopsis_Presentation.pptx")
    project_docs_pptx = Path(r"c:\Users\KIIT\Desktop\fake-news-detection\docs\Fake_News_Detection_Synopsis_Presentation.pptx")

    project_docs_pptx.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(desktop_pptx))
    prs.save(str(project_docs_pptx))

    print(f"[OK] Successfully generated Presentation at: {desktop_pptx}")
    print(f"[OK] Successfully saved copy in project docs at: {project_docs_pptx}")

if __name__ == "__main__":
    create_presentation()
