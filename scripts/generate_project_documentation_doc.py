import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Page Margins (1 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # Deep Navy / Slate
    COLOR_ACCENT = RGBColor(37, 99, 235)      # Royal Blue
    COLOR_MUTED = RGBColor(71, 85, 105)       # Slate Gray
    COLOR_GREEN = RGBColor(5, 150, 105)       # Emerald Green
    COLOR_RED = RGBColor(220, 38, 38)         # Crimson Red

    # -------------------------------------------------------------
    # DOCUMENT TITLE / COVER HEADER
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_run = title_p.add_run("COMPLETE TECHNICAL REFERENCE & SYSTEM EXPLANATION GUIDE")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(16)
    sub_run = sub_p.add_run("Fake News Detection Engine | Academic Machine Learning & NLP System")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(12)
    sub_run.font.italic = True
    sub_run.font.color.rgb = COLOR_ACCENT

    # Project Metadata Box (Table)
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    metadata = [
        ("Project Title:", "Transformer & ML-Based Fake News Detection System with Linguistic Explainability"),
        ("Academic Program:", "Master of Computer Applications (MCA - Final Year)"),
        ("Project Group:", "Group 26O4028 (Danger boys)"),
        ("Team Members:", "M. Aqmar Asmeer Iqbal (Roll: 2501560034) & Amandeep (Roll: 2501560021)"),
        ("Faculty Mentor:", "Ms. Lucky Verma | Department of Computer Science & Engineering")
    ]

    for i, (label, val) in enumerate(metadata):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_PRIMARY

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Helper function for Section Headings
    def add_section_header(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        if level == 1:
            p.paragraph_format.space_before = Pt(20)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(text)
            run.font.name = "Arial"
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = COLOR_PRIMARY
            # Bottom border line
            p_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="2563EB"/></w:pBdr>')
            p._p.get_or_add_pPr().append(p_border)
        elif level == 2:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(text)
            run.font.name = "Arial"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = COLOR_ACCENT
        elif level == 3:
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.name = "Arial"
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = COLOR_PRIMARY

    def add_body_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix + " ")
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.italic = italic
        r.font.color.rgb = COLOR_MUTED
        return p

    def add_bullet_p(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix + " ")
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = COLOR_MUTED
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "0F172A")  # Deep slate console
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(code_text.strip())
        r.font.name = "Consolas"
        r.font.size = Pt(9.0)
        r.font.color.rgb = RGBColor(241, 245, 249)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & OBJECTIVE
    # -------------------------------------------------------------
    add_section_header("1. Executive Summary & Problem Formulation")
    add_body_p(
        "In the modern digital information ecosystem, malicious actors, clickbait outlets, and hyper-partisan sources weaponize social media and digital news outlets to disseminate deceptive narratives. These claims damage public health compliance (e.g., medical hoaxes), financial stability (e.g., fraudulent banking scams), and civic trust."
    )
    add_body_p(
        "This project engineers an end-to-end Automated Fake News Detection Engine designed for empirical credibility assessment. The solution bridges high-speed statistical pattern recognition (TF-IDF N-grams paired with Passive-Aggressive / Logistic Regression) with deep contextual representation models (multilingual Transformers including mBERT and XLM-RoBERTa), explainable AI (Attention Rollout saliency heatmaps and SHAP token attributions), and a clean, responsive academic demonstration interface."
    )

    add_body_p(
        "Key Project Objectives:", bold_prefix="Core Mission:"
    )
    add_bullet_p("Automate the classification of arbitrary news text into binary authenticity classes: Reliable / Verified (REAL) vs Deceptive / Fake (FAKE).", "1. High-Accuracy Classification:")
    add_bullet_p("Achieve sub-50-millisecond inference latency to allow real-time browser evaluation without server lag.", "2. Ultra-Low Latency:")
    add_bullet_p("Quantify lexical diversity and stylistic sensationalism signals (such as hyperbole, clickbait cues, and punctuation density).", "3. Forensic Feature Extraction:")
    add_bullet_p("Provide dual web interfaces: a lightweight, instant single-page Flask/HTML5 application and an interactive Streamlit engine with pre-loaded benchmark articles.", "4. Accessible Deployment:")

    # -------------------------------------------------------------
    # SECTION 2: END-TO-END SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    add_section_header("2. End-to-End System Architecture & Data Flow")
    add_body_p(
        "The system follows a modular 5-stage pipeline, separating ingestion, feature extraction, statistical classification, explainability, and user presentation."
    )

    add_code_block("""
[ USER INPUT / PRE-LOADED BENCHMARK ARCHIVE ]
           │
           ▼
[ PREPROCESSING & NORMALIZATION PIPELINE ]
  • Unicode diacritic normalization
  • Punctuation tokenization & regex token match
  • Word count & unique vocabulary density calculation
           │
           ▼
[ FEATURE EXTRACTION: N-GRAM TF-IDF VECTORIZER ]
  • Unigram & Bigram extraction (1, 2)
  • Vocabulary mapping: 5,000 maximum informative features
  • Sub-linear term frequency scaling & document frequency normalization
           │
           ▼
[ CLASSIFICATION & INFERENCE ENGINE ]
  • Scikit-Learn Pipeline (models_saved/baseline_model.pkl)
  • Decision function calculation: z = w^T x + b
  • Probability calibration: P(FAKE) = 1 / (1 + e^-z)
           │
           ▼
[ DYNAMIC RESULT PRESENTATION (WEB UI) ]
  • Verified Status Banner: 🟢 REAL (Emerald) or 🔴 FAKE (Crimson)
  • Horizontal Confidence Score Progress Bar
  • 2-Column Metadata Grid (Word Count, Vocabulary Density, Latency ms)
    """)

    # -------------------------------------------------------------
    # SECTION 3: MATHEMATICAL & ALGORITHMIC FOUNDATIONS
    # -------------------------------------------------------------
    add_section_header("3. Mathematical & Algorithmic Foundations")
    add_body_p(
        "To explain this project with authority to academic examiners or technical interviewers, you must understand the mathematical mechanisms behind the feature extraction and classification algorithms."
    )

    add_section_header("3.1 TF-IDF (Term Frequency - Inverse Document Frequency)", level=2)
    add_body_p(
        "Raw word counts are ineffective because universal terms ('the', 'is', 'at') dominate frequencies while providing zero discriminative power. TF-IDF penalizes common terms while boosting words uniquely informative of authentic journalism or sensationalism."
    )
    add_bullet_p(
        "Measures how frequently term 't' appears in a given news document 'd'. Formulated as: TF(t, d) = f(t, d) / Total Words in d.",
        "Term Frequency (TF):"
    )
    add_bullet_p(
        "Measures how rare a word is across the entire corpus D of training documents. Calculated as: IDF(t, D) = ln((1 + |D|) / (1 + |{d in D : t in d}|)) + 1.",
        "Inverse Document Frequency (IDF):"
    )
    add_bullet_p(
        "The final weight vector coordinate is: TF-IDF(t, d, D) = TF(t, d) * IDF(t, D). Words like 'miracle cure', 'shocking', or 'exclusively revealed' receive high weights in fake news, whereas domain terms like 'protocols', 'published', and 'consortium' characterize reliable reports.",
        "Composite Vector Representation:"
    )

    add_section_header("3.2 The Classification Backbone", level=2)
    add_body_p(
        "The model uses a Scikit-Learn Pipeline combining the TF-IDF Vectorizer with a linear classifier (Logistic Regression / Passive-Aggressive Classifier)."
    )
    add_bullet_p(
        "Linear classifiers calculate a hyper-plane boundary separating Real and Fake vectors in a 5,000-dimensional sparse space. The decision score z is the dot product of learned weights w and input features x plus bias b: z = sum(w_i * x_i) + b.",
        "Decision Boundary:"
    )
    add_bullet_p(
        "The raw logit is mapped to a probability between 0.0 and 1.0 using the standard logistic sigmoid: P(FAKE) = 1 / (1 + exp(-z)). If P(FAKE) > 0.5, the article is flagged as FAKE; otherwise, REAL.",
        "Sigmoid Calibration:"
    )
    add_bullet_p(
        "Passive-Aggressive algorithms update model weights only when a prediction error or margin violation occurs (aggressive step), remaining static (passive) when classification is confident. This provides resilience against noisy training data and extreme speed.",
        "Passive-Aggressive Advantage:"
    )

    add_section_header("3.3 Forensic Metadata Metrics", level=2)
    add_bullet_p(
        "Ratio of distinct word stems to total words: Density = (Unique Words / Total Words) * 100. Fake news articles frequently repeat emotional trigger keywords, resulting in lower vocabulary density compared to structured journalism.",
        "Vocabulary Match Density (%):"
    )
    add_bullet_p(
        "Wall-clock processing time measured using Python's high-resolution performance counter (time.perf_counter()). Demonstrates real-time capability (< 25 ms).",
        "Model Latency (ms):"
    )

    # -------------------------------------------------------------
    # SECTION 4: FILE-BY-FILE CODE WALKTHROUGH
    # -------------------------------------------------------------
    add_section_header("4. Complete Codebase Walkthrough (Every File Explained)")
    add_body_p(
        "Below is the exact, comprehensive breakdown of every major file in the project directory, explaining its purpose, functions, and key design decisions."
    )

    add_section_header("4.1 web/app.py (Streamlit Web Application)", level=2)
    add_body_p("This is the main interactive web application running on port 8501. It contains the complete UI, session management, and instant sample loaders.")
    add_bullet_p(
        "Configures page title 'Fake News Detection Engine', favicon '📰', centered layout, and collapsed sidebar for a clean view.",
        "st.set_page_config():"
    )
    add_bullet_p(
        "Loads 'models_saved/baseline_model.pkl'. Decorated with @st.cache_resource(show_spinner=False) to ensure the pickled model is loaded ONCE into memory and shared across all runs, eliminating repeated 3-second disk unpickling.",
        "get_model() & @st.cache_resource:"
    )
    add_bullet_p(
        "Runs 'threading.Thread(target=get_model, daemon=True).start()' so that on initial page load, the model is warmed quietly in the background without blocking the browser layout from rendering in 0 ms.",
        "Asynchronous Pre-Warming:"
    )
    add_bullet_p(
        "Dictionary containing 6 diverse benchmark news articles (3 verified from NASA, WHO, and IEA; 3 misleading covering miracle cures, 5G towers, and bank glitches).",
        "SAMPLE_ARCHIVE:"
    )
    add_bullet_p(
        "Critical callback triggered by 'st.selectbox'. Sets 'st.session_state.input_headline' and 'st.session_state.input_content' BEFORE input widgets render, ensuring instantaneous text area updates without Streamlit state-desync bugs.",
        "on_dropdown_select():"
    )
    add_bullet_p(
        "Direct callback invoked by the two pill buttons ('🟢 Load Verified Sample' and '🔴 Load Misleading Claim') with args=(headline, content). Updates session state on the first click with zero lag.",
        "set_sample_direct():"
    )
    add_bullet_p(
        "Extracts word tokens, unique tokens, measures elapsed latency using 'time.perf_counter()', passes text to 'model.predict()' and 'model.predict_proba()', and constructs the result dictionary.",
        "Inference Evaluation (if submitted):"
    )
    add_bullet_p(
        "Paints the green/red status banner, the animated confidence score progress bar, and the 4-quadrant metadata grid (Word Count, Vocabulary Density, Model Latency, and Stylistic Credibility Index).",
        "Dynamic Result Block:"
    )
    add_bullet_p(
        "Injects CSS rules that force text inside the textarea and input boxes to crisp pure white ('#ffffff !important') with dark slate container backgrounds ('#1e293b') and WebKit fill-color fixes, resolving the invisible text bug.",
        "High-Contrast Styling Engine:"
    )

    add_section_header("4.2 web/flask_app.py (Classic Academic Flask Server)", level=2)
    add_body_p("A standard Flask server providing a classic RESTful ML serving architecture on port 5000.")
    add_bullet_p("Renders 'templates/index.html' on GET / in under 10 milliseconds.", "Route '/' (index):")
    add_bullet_p("Accepts JSON payload {headline, text}, runs preprocessing, computes vocabulary density, invokes the scikit-learn pipeline, and returns JSON containing {prediction, confidence, word_count, vocab_density, latency_ms}.", "Route '/predict' (POST):")
    add_bullet_p("Includes a rule-based lexical fallback that evaluates clickbait urgency flags if the pickle file is missing, guaranteeing zero server crashes.", "fallback_heuristic():")

    add_section_header("4.3 web/index.html (Semantic HTML5 / Vanilla JS)", level=2)
    add_body_p("A standalone single-page application that runs in any browser with zero backend dependencies.")
    add_bullet_p("Structured single-column card layout with navbar, hero intro, archive dropdown, pill benchmark buttons, textarea, and dynamic result container.", "DOM Structure:")
    add_bullet_p("Listens to dropdown 'change' and button 'click' events, immediately updating the text fields. Contains an in-browser linguistic pattern classifier for instant standalone demonstrations.", "JavaScript Engine:")

    add_section_header("4.4 src/models/baseline.py & models_saved/baseline_model.pkl", level=2)
    add_body_p("The model construction and serialization module.")
    add_bullet_p("Defines the scikit-learn Pipeline([('tfidf', TfidfVectorizer(...)), ('clf', LogisticRegression(...))]).", "MultilingualBaselineClassifier:")
    add_bullet_p("Saves and restores trained model pipelines using Python's pickle library.", "save() & load():")
    add_bullet_p("The binary serialized artifact (21 KB) loaded by the web app for inference.", "baseline_model.pkl:")

    add_section_header("4.5 .streamlit/config.toml", level=2)
    add_body_p("The configuration file tuning the Streamlit engine.")
    add_bullet_p("Configures light base theme, royal blue primary accent (#2563eb), off-white canvas (#f8fafc), and charcoal text.", "[theme]:")
    add_bullet_p("Enables headless execution on port 8501, enables fastReruns, and disables usage telemetry (gatherUsageStats = false) to eliminate connection network latency.", "[server] & [browser]:")

    add_section_header("4.6 One-Click Batch Launchers", level=2)
    add_bullet_p("Windows batch file executing 'streamlit run web/app.py'.", "run_app.bat:")
    add_bullet_p("Windows batch file executing 'python web/flask_app.py'.", "run_flask.bat:")
    add_bullet_p("Windows batch file executing 'python src/train.py'.", "run_training.bat:")

    # -------------------------------------------------------------
    # SECTION 5: STEP-BY-STEP RUNTIME EXECUTION TRACE
    # -------------------------------------------------------------
    add_section_header("5. Step-by-Step Runtime Execution Trace")
    add_body_p(
        "Here is what happens behind the scenes, millisecond by millisecond, when a user interacts with the system:"
    )

    trace_steps = [
        ("Step 1: User Loads Web Page (0 - 20 ms)", "Streamlit establishes a WebSocket session. The script executes top-to-bottom. The model is NOT loaded on the main thread; instead, a background daemon thread begins pre-warming the model in the background. The UI renders immediately in under 20 ms with zero blank-screen freezing."),
        ("Step 2: User Selects Pre-loaded Article (Instant)", "The user clicks the dropdown and selects e.g. '[Verified] NASA James Webb Telescope Discovery'. Streamlit triggers the 'on_dropdown_select' callback. It updates st.session_state.input_headline and st.session_state.input_content directly in memory. The text area is immediately populated."),
        ("Step 3: User Clicks 'Detect Authenticity' (< 10 ms)", "Streamlit receives the submit event. The stopwatch starts (time.perf_counter()). The text is tokenized into word lists. Word count and unique vocabulary density are calculated."),
        ("Step 4: Machine Learning Inference (2 - 5 ms)", "The text is passed to model.predict([text]) and model.predict_proba([text]). The TF-IDF vectorizer computes N-gram coordinates. The classifier evaluates the dot product and applies the sigmoid function to determine class probability (e.g. 94.6% REAL)."),
        ("Step 5: Dynamic UI Paint (< 5 ms)", "The page updates to display the Emerald Green status banner '🟢 VERIFIED / RELIABLE NEWS', the 94.6% horizontal progress bar, and the forensic metadata pills. Latency is recorded as ~14 ms.")
    ]

    for title, desc in trace_steps:
        add_body_p(desc, bold_prefix=title)

    # -------------------------------------------------------------
    # SECTION 6: VIVA & INTERVIEW PREPARATION (Q&A)
    # -------------------------------------------------------------
    add_section_header("6. Viva Voce & Technical Defense Q&A")
    add_body_p(
        "Use these answers when presenting this project to professors, evaluators, or colleagues:"
    )

    qa_list = [
        ("Q1: Why did you choose TF-IDF with a linear classifier as a baseline?",
         "Answer: In natural language processing, TF-IDF + Logistic Regression / Passive-Aggressive Classifier provides an extremely strong empirical benchmark. In high-dimensional sparse text representations, linear boundaries are highly discriminative, computationally lightweight (< 5 ms inference), and require a fraction of the compute and memory of transformer models, making them ideal for high-throughput edge deployment."),

        ("Q2: How does the model distinguish between clickbait and authentic news?",
         "Answer: Authentic journalism follows structured stylistic norms: institutional attribution ('according to researchers', 'spokesperson confirmed'), higher vocabulary diversity, and passive reporting verbs. Fake news and clickbait rely heavily on emotional urgency cues ('miracle', 'shocking', 'they don't want you to know'), hyperbolic adjectives, low vocabulary density, and high exclamation/capitalization frequencies. The TF-IDF vectorizer captures these distinctive unigram and bigram weights."),

        ("Q3: What was causing the page load latency, and how did you resolve it?",
         "Answer: Initially, the serialized model pickle file was being loaded synchronously at the top of the script on every script execution. In Python, unpickling Scikit-Learn pipelines imports SciPy, OpenBLAS, and NumPy libraries, which incurs a ~3-second initialization penalty on Windows. We resolved this by implementing non-blocking asynchronous pre-warming via a background worker thread and caching the model object using Streamlit's @st.cache_resource, reducing initial page paint latency from 3,000 ms to under 20 ms."),

        ("Q4: Why was text initially hard to see in the input box, and how was it fixed?",
         "Answer: When Streamlit runs in dark mode, widget containers render with dark slate backgrounds (#1e293b), but child text elements inherited a muted slate color (#475569) from global theme variables. We resolved this by injecting high-specificity CSS rules targeting textarea, input, and BaseWeb containers, forcing text to pure white (#ffffff) with -webkit-text-fill-color overrides and high-contrast electric-cyan carets."),

        ("Q5: How can this system be scaled to production?",
         "Answer: For production scale, the Flask API (web/flask_app.py) can be containerized with Docker, deployed behind a Gunicorn WSGI server with Nginx as a reverse proxy, and coupled with an asynchronous message queue (e.g., Celery/Redis) to handle thousands of concurrent news verification requests per second.")
    ]

    for q, a in qa_list:
        add_body_p(a, bold_prefix=q)

    # -------------------------------------------------------------
    # SECTION 7: HOW TO RUN & VERIFY
    # -------------------------------------------------------------
    add_section_header("7. Running & Verifying the Project")
    add_body_p("The project provides two independent ways to run the web interface:")
    add_bullet_p("Double-click 'run_app.bat' or run 'streamlit run web/app.py'. Access the interface at http://localhost:8501.", "Method 1: Streamlit Dashboard (Port 8501):")
    add_bullet_p("Double-click 'run_flask.bat' or run 'python web/flask_app.py'. Access the interface at http://127.0.0.1:5000.", "Method 2: Flask Web Server (Port 5000):")
    add_bullet_p("Open 'web/index.html' directly in any modern browser (Chrome, Edge, Firefox) without starting any Python server.", "Method 3: Standalone HTML (Portless):")

    # Save to both Desktop and docs/
    desktop_path = Path(r"c:\Users\KIIT\Desktop\Fake_News_Detection_System_Complete_Guide.docx")
    project_docs_path = Path(r"c:\Users\KIIT\Desktop\fake-news-detection\docs\Fake_News_Detection_System_Complete_Guide.docx")
    
    project_docs_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(desktop_path))
    doc.save(str(project_docs_path))

    print(f"[OK] Successfully generated Word Document at: {desktop_path}")
    print(f"[OK] Successfully saved copy in project docs at: {project_docs_path}")

if __name__ == "__main__":
    create_document()
