import sys
import os
import time
import pickle
import threading
from pathlib import Path
import streamlit as st

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.multilingual_engine import evaluate_multilingual_content, detect_language
from src.media_extractor import extract_text_from_file

MODEL_PATH = BASE_DIR / "models_saved" / "baseline_model.pkl"

# Streamlit Page Config
st.set_page_config(
    page_title="Fake News Detection Engine",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Asynchronous / cached model loader (Non-blocking: 0ms page paint)
@st.cache_resource(show_spinner=False)
def get_model():
    if MODEL_PATH.exists():
        try:
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None
    return None

# Warm model in a background thread so initial page load is 100% instant
if "prewarmed" not in st.session_state:
    st.session_state["prewarmed"] = True
    threading.Thread(target=get_model, daemon=True).start()

# Curated Sample News & Multilingual Fact-Check Archive
SAMPLE_ARCHIVE = {
    "-- Select a Current News Article or Global Report --": {
        "content": ""
    },
    "ISRO Gaganyaan: Propulsion System Successfully Qualified for Human Spaceflight (English)": {
        "content": "The Indian Space Research Organisation (ISRO) successfully conducted the qualification hot tests of the Service Module Propulsion System for the upcoming Gaganyaan human spaceflight mission at Mahendragiri. All propulsion systems operated as planned, meeting all reliability and safety parameters for astronaut transit."
    },
    "Reserve Bank of India Issues New Digital Banking Cybersecurity Directives (English)": {
        "content": "The Reserve Bank of India (RBI) announced revised cybersecurity and fraud mitigation frameworks for commercial banks and digital payment service providers. The directive mandates automated transaction anomaly detection and standardized customer grievance redressal timelines across all financial institutions."
    },
    "NASA James Webb Space Telescope Observes Atmospheric Water on Exoplanet (English)": {
        "content": "NASA's James Webb Space Telescope has captured definitive atmospheric signatures of a distant gas giant exoplanet. The peer-reviewed findings, published in Nature Astronomy by an international consortium of astrophysicists, reveal transmission spectroscopy indicating water vapor and carbon dioxide clouds without ambiguous anomalies."
    },
    "Viral Alert Claims Complete Nationwide Ban on Fossil Fuel Vehicles Next Month (English)": {
        "content": "URGENT WARNING! Secret leaked documents confirm that the government is immediately banning all petrol and diesel vehicles starting next month! Any citizen found driving private combustion vehicles will face heavy fines and instant vehicle impoundment. Share this notification immediately before authorities delete it!"
    },
    "Viral Report: Rare Himalayan Mountain Herb Cures All Chronic Diseases in 24h (English)": {
        "content": "SHOCKING SECRET: Researchers have uncovered that a rare wild mountain flower immediately eliminates every chronic ailment known to man in under 24 hours! Big pharmaceutical companies and corrupt authorities are deleting this post and threatening doctors who reveal the formula! Share this immediately before it is banned forever!"
    },
    "Thermodynamics Standard: Boiling and Freezing Points of Pure Water (English)": {
        "content": "Under standard atmospheric pressure of 1 atmosphere at sea level, pure liquid water exhibits a well-documented phase change boiling point of 100 degrees Celsius and freezes into solid crystalline ice at 0 degrees Celsius."
    },
    "ଓଡ଼ିଶାରେ ନୂତନ ସେମିକଣ୍ଡକ୍ଟର ଉତ୍ପାଦନ କେନ୍ଦ୍ର ଏବଂ ଆଇଟି ପାର୍କ ପ୍ରତିଷ୍ଠା (Odia)": {
        "content": "ଓଡ଼ିଶା ସରକାର ଭୁବନେଶ୍ୱରରେ ଅତ୍ୟାଧୁନିକ ସେମିକଣ୍ଡକ୍ଟର ନିର୍ମାଣ ୟୁନିଟ୍ ଏବଂ ନୂତନ ସଫ୍ଟୱେୟାର ଟେକ୍ନୋଲୋଜି ପାର୍କ ପ୍ରତିଷ୍ଠା ପାଇଁ ଚୁକ୍ତି ସ୍ୱାକ୍ଷର କରିଛନ୍ତି। ଏହି ପ୍ରକଳ୍ପ ଦ୍ୱାରା ରାଜ୍ୟରେ ହଜାର ହଜାର ଯୁବକ ଯୁବତୀଙ୍କୁ ନିଯୁକ୍ତି ସୁଯୋଗ ମିଳିବ ବୋଲି ଶିଳ୍ପ ବିଭାଗ ସୂଚନା ଦେଇଛି।"
    },
    "ଭୁବନେଶ୍ୱର ମେଟ୍ରୋ ରେଳ ପ୍ରକଳ୍ପର ପ୍ରଥମ ପର୍ଯ୍ୟାୟ ନିର୍ମାଣ କାର୍ଯ୍ୟ ଦ୍ରୁତ ଗତିରେ ଜାରି (Odia)": {
        "content": "ଭୁବନେଶ୍ୱର ବିମାନବନ୍ଦରରୁ ତ୍ରିଶୁଳିଆ ପର୍ଯ୍ୟନ୍ତ ନିର୍ମାଣ ହେଉଥିବା ମେଟ୍ରୋ ରେଳ ପ୍ରକଳ୍ପ କାର୍ଯ୍ୟ ନିର୍ଦ୍ଧାରିତ ସମୟ ସୀମା ମଧ୍ୟରେ ଶେଷ କରିବାକୁ ନିର୍ଦ୍ଦେଶ ଦିଆଯାଇଛି। ସହରରେ ଯାତାୟାତ ସୁବିଧା ପାଇଁ ଏହି ମେଟ୍ରୋ ବ୍ୟବସ୍ଥା ଏକ ବଡ଼ ପଦକ୍ଷେପ ହେବ।"
    },
    "ଭାଇରାଲ ଦାବି: ଏକ ବିଶେଷ ଚେର ଖାଇଲେ ସମସ୍ତ ପୁରୁଣା ରୋଗ ଗୋଟିଏ ରାତିରେ ଭଲ (Odia)": {
        "content": "ଚମତ୍କାର ଆୟୁର୍ବେଦିକ ଖବର! ଜଙ୍ଗଲରେ ମିଳୁଥିବା ଏକ ବିଶେଷ ଚେର ଖାଇଲେ ମାତ୍ର ଗୋଟିଏ ରାତିରେ ସବୁ ପ୍ରକାର ଜଟିଳ ରୋଗ ଭଲ ହୋଇଯାଉଛି। ଡାକ୍ତରମାନେ ଏହି ରହସ୍ୟ ଲୁଚାଇ ରଖିଛନ୍ତି, ତେଣୁ ଲିଙ୍କ କଟିବା ପୂର୍ବରୁ ଏହାକୁ ସମସ୍ତଙ୍କ ପାଖକୁ ପଠାନ୍ତୁ!"
    },
    "इसरो गगनयान मिशन: अंतरिक्ष यात्रियों के लिए क्रू मॉड्यूल का सफल परीक्षण (Hindi)": {
        "content": "भारतीय अंतरिक्ष अनुसंधान संगठन (इसरो) ने गगनयान मानव अंतरिक्ष उड़ान मिशन के तहत क्रू मॉड्यूल प्रपल्शन सिस्टम का सफल परीक्षण पूरा किया। वैज्ञानिकों ने बताया कि सभी तकनीकी मानक परीक्षण के दौरान पूरी तरह से सुरक्षित और सटीक पाए गए।"
    },
    "आरबीआई ने डिजिटल भुगतान और ऑनलाइन बैंकिंग के लिए जारी किए नए दिशानिर्देश (Hindi)": {
        "content": "भारतीय रिज़र्व बैंक (आरबीआई) ने वित्तीय धोखाधड़ी रोकने के लिए सभी बैंकों और डिजिटल पेमेंट गेटवे के लिए नए सुरक्षा नियम लागू किए हैं। नए नियमों के तहत संदिग्ध लेन-देन की रीयल-टाइम निगरानी अनिवार्य की गई है।"
    },
    "सोशल मीडिया दावा: हल्दी और गरम पानी पीने से कैंसर 24 घंटे में पूरी तरह खत्म (Hindi)": {
        "content": "सावधान! गुप्त सूत्रों से बड़ा खुलासा हुआ है कि मात्र हल्दी और उबला पानी पीने से हर प्रकार का कैंसर और गंभीर बीमारी 24 घंटे में ठीक हो जाती है। बड़ी दवा कंपनियां और सरकार इस चमत्कारिक नुस्खे को दबा रही हैं। इसे तुरंत शेयर करें!"
    },
    "মহাকাশ গবেষণা ও গভীর অনুসন্ধান মিশনে ইসরোর ভবিষ্যৎ পরিকল্পনা ঘোষণা (Bengali)": {
        "content": "ভারতীয় মহাকাশ গবেষণা সংস্থা (ইসরো) তাদের পরবর্তী মহাকাশ অভিযান এবং গভীর মহাকাশ অনুসন্ধানের জন্য নতুন রূপরেখা প্রকাশ করেছে। বিজ্ঞান সম্মেলনে মহাকাশবিজ্ঞানীরা কৃত্রিম উপগ্রহ ও মিশন ডেটা বিশ্লেষণের অগ্রগতি তুলে ধরেন।"
    },
    "অনলাইন ভাইরাল পোস্ট: বিরল পাতার রসে ডায়াবেটিস একদিনেই পুরোপুরি নিরাময় (Bengali)": {
        "content": "চমকপ্রদ গোপন খবর! হিমালয়ের একটি দুর্লভ পাতা চিবিয়ে খেলে মাত্র ২৪ ঘণ্টায় সকল ডায়াবেটিস ও জটিল রোগ নির্মূল হয়ে যায়। ডাক্তাররা এই মহাঔষধ লুকিয়ে রাখছে। ডিলিট হওয়ার আগেই পোস্টটি শেয়ার করুন!"
    },
    "Le télescope spatial James Webb confirme la présence de molécules d'eau (French)": {
        "content": "Les données spectroscopiques du télescope spatial James Webb ont formellement identifié des molécules d'eau dans l'atmosphère d'une exoplanète géante gazeuse. Les astrophysiciens du consortium international ont validé ces mesures rigoureuses."
    },
    "Publication virale: Une plante rare guérit toutes les maladies en 24 heures (French)": {
        "content": "URGENT! Les élites mondiales et les autorités pharmaceutiques censurent la vérité sur une herbe miraculeuse qui guérit instantanément le cancer et toutes les infections en une seule nuit! Partagez avant censure totale!"
    },
    "La Organización Mundial de la Salud publica nuevos protocolos sanitarios (Spanish)": {
        "content": "La Organización Mundial de la Salud (OMS) presentó directrices epidemiológicas actualizadas basadas en estudios clínicos revisados por pares. Los ministerios de salud confirmaron una estabilización en la transmisión comunitaria."
    },
    "Mensaje viral en redes: Planta milagrosa cura enfermedades de la noche a la mañana (Spanish)": {
        "content": "¡COMPÁRTELO ANTES DE QUE LO BORREN! Un científico desvela el remedio prohibido que cura el cáncer en 24 horas y que los gobiernos corruptos quieren censurar. Despierta y no dejes que oculten este secreto medicinal."
    },
    "Bundesministerium beschließt wissenschaftliche Behandlungsstandards (German)": {
        "content": "Das Bundesgesundheitsministerium hat in Zusammenarbeit mit führenden Forschungsinstituten aktualisierte medizinische Standards vorgelegt. Die Daten belegen eine kontinuierliche Verbesserung der Patientenversorgung."
    },
    "Viraler Kettenbrief: Geheime Sendemasten steuern menschliche Gedanken (German)": {
        "content": "Ein ehemaliger Regierungsberater bricht sein Schweigen: Neue Funkmasten strahlen Frequenzen aus, um das Verhalten der Bevölkerung heimlich zu manipulieren! Offizielle Medien zensieren diesen Skandal sofort!"
    },
    "JAXA探査機が小惑星からの物質採取ミッションに成功と発表 (Japanese)": {
        "content": "宇宙航空研究開発機構（JAXA）の探査チームは、小惑星表面からの高精度サンプル回収ミッションが成功裏に完了したと発表しました。採取されたカプセルは地球に帰還し、詳細な科学分析が進められています。"
    },
    "SNS拡散情報：政府が隠蔽する薬草が24時間で全難病を完治させるという主張 (Japanese)": {
        "content": "極秘文書が流出！山奥に自生するある植物のエキスが、末期がんを含む全ての慢性疾患をわずか一晩で消滅させることが判明しました！製薬会社が圧力をかけて情報を削除しています！今すぐ拡散してください！"
    }
}

# Session State Initialization
if "input_content" not in st.session_state:
    st.session_state["input_content"] = ""
if "evaluated" not in st.session_state:
    st.session_state["evaluated"] = False
if "result" not in st.session_state:
    st.session_state["result"] = None
if "selected_sample" not in st.session_state:
    st.session_state["selected_sample"] = "-- Select a Current News Article or Global Report --"
if "last_uploaded_id" not in st.session_state:
    st.session_state["last_uploaded_id"] = None
if "upload_notice" not in st.session_state:
    st.session_state["upload_notice"] = ""

# Callbacks for instant, zero-delay state synchronization
def on_dropdown_select():
    selected = st.session_state.selected_sample
    if selected in SAMPLE_ARCHIVE and selected != "-- Select a Current News Article or Global Report --":
        st.session_state.input_content = SAMPLE_ARCHIVE[selected]["content"]
        st.session_state.evaluated = False
        st.session_state.result = None
        st.session_state.upload_notice = ""

def reset_all():
    st.session_state.input_content = ""
    st.session_state.selected_sample = "-- Select a Current News Article or Global Report --"
    st.session_state.evaluated = False
    st.session_state.result = None
    st.session_state.upload_notice = ""

# Custom Light-Theme CSS (Preserving 100% of the User's UI Aesthetic)
st.markdown("""
<meta name="google" content="notranslate">
<style>
    :root {
        --bg-canvas: #f8fafc;
        --card-bg: #ffffff;
        --border-subtle: #e2e8f0;
        --text-heading: #0f172a;
        --text-body: #475569;
        --text-muted: #64748b;
        --accent-blue: #2563eb;
        --accent-blue-hover: #1d4ed8;
        --accent-green: #059669;
        --green-bg: #ecfdf5;
        --green-border: #a7f3d0;
        --accent-red: #dc2626;
        --red-bg: #fef2f2;
        --red-border: #fecaca;
    }

    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        box-sizing: border-box;
    }

    /* Suppress Streamlit native overhead */
    header, footer, [data-testid="stHeader"], [data-testid="stDecoration"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    .stApp {
        background-color: var(--bg-canvas) !important;
        color: var(--text-body) !important;
    }

    .block-container {
        max-width: 760px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* Top Navbar */
    .custom-navbar {
        background-color: #ffffff;
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text-heading);
        white-space: nowrap;
    }

    .nav-meta {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .model-badge {
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #334155;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    .model-badge::before {
        content: '';
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--accent-green);
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .hero-heading {
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-heading);
        letter-spacing: -0.02em;
        margin-bottom: 0.35rem;
    }

    .hero-subtext {
        font-size: 0.95rem;
        color: var(--text-body);
        max-width: 580px;
        margin: 0 auto;
        line-height: 1.55;
    }

    /* High-Contrast, Crystal-Clear Text inside Textarea & Inputs ("The Black Box") */
    textarea,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="textarea"] textarea,
    div[data-testid="stTextArea"] [data-baseweb="textarea"] textarea {
        background-color: #1e293b !important;
        background: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 0.85rem 1rem !important;
        caret-color: #38bdf8 !important;
    }

    textarea::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 0.9 !important;
    }

    div[data-testid="stTextArea"] > div,
    div[data-testid="stTextArea"] [data-baseweb="textarea"],
    div[data-testid="stTextArea"] [data-baseweb="textarea"] > div {
        background-color: #1e293b !important;
        background: #1e293b !important;
        border-color: #475569 !important;
        border-radius: 8px !important;
    }

    /* Headline Input */
    input,
    div[data-testid="stTextInput"] input,
    div[data-baseweb="input"] input,
    div[data-testid="stTextInput"] [data-baseweb="input"] input {
        background-color: #1e293b !important;
        background: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        caret-color: #38bdf8 !important;
    }

    input::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 0.9 !important;
    }

    div[data-testid="stTextInput"] > div,
    div[data-testid="stTextInput"] [data-baseweb="input"],
    div[data-testid="stTextInput"] [data-baseweb="input"] > div {
        background-color: #1e293b !important;
        background: #1e293b !important;
        border-color: #475569 !important;
        border-radius: 8px !important;
    }

    /* Dropdown Selectbox */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        background: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] * {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }

    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] ul {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
    }

    li[role="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #334155 !important;
        color: #38bdf8 !important;
        -webkit-text-fill-color: #38bdf8 !important;
    }

    /* Form Widgets Spacing & Indentation */
    div[data-testid="stSelectbox"] {
        margin-bottom: 1.25rem !important;
    }

    /* File Uploader Clean Layout & Indentation */
    div[data-testid="stFileUploader"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 1.25rem !important;
    }

    /* Modern Rounded Dropzone */
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"],
    div[data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1.5px dashed #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 0.9rem 1.25rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 1rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover,
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #2563eb !important;
        background-color: #f8fafc !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.08) !important;
    }

    /* Hide the redundant extra top/header button in Streamlit 1.65 */
    div[data-testid="stFileUploader"] button:not(section[data-testid="stFileUploaderDropzone"] button),
    div[data-testid="stFileUploader"] > div:first-child button,
    div[data-testid="stFileUploader"] > div > div > button {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
    }

    /* Sleek Professional Upload Button inside the dropzone ONLY */
    section[data-testid="stFileUploaderDropzone"] button,
    section[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
        background-color: #2563eb !important;
        background: #2563eb !important;
        font-size: 0px !important;
        line-height: 0 !important;
        color: transparent !important;
        -webkit-text-fill-color: transparent !important;
        padding: 0.5rem 1.15rem !important;
        border-radius: 6px !important;
        border: 1px solid #1d4ed8 !important;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2) !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        min-height: 38px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        transition: all 0.15s ease !important;
    }

    /* Completely suppress all child DOM nodes and text inside the dropzone button */
    section[data-testid="stFileUploaderDropzone"] button *,
    section[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] * {
        display: none !important;
        visibility: hidden !important;
        font-size: 0px !important;
        line-height: 0 !important;
        width: 0 !important;
        height: 0 !important;
        color: transparent !important;
        -webkit-text-fill-color: transparent !important;
        opacity: 0 !important;
    }

    /* Inject exactly one single clean immutable label inside the dropzone button */
    section[data-testid="stFileUploaderDropzone"] button::after,
    section[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]::after {
        content: "📁 Browse & Upload" !important;
        font-size: 0.85rem !important;
        line-height: 1.2 !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        display: inline-block !important;
        visibility: visible !important;
    }

    section[data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #1d4ed8 !important;
        background: #1d4ed8 !important;
        border-color: #1e40af !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Uploader Dropzone Instructions Text (200MB per file...) */
    div[data-testid="stFileUploaderDropzoneInstructions"],
    div[data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        font-size: 0.825rem !important;
        font-weight: 500 !important;
    }

    /* Field Labels */
    label,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* Textarea Margin */
    div[data-testid="stTextArea"] {
        margin-bottom: 1.25rem !important;
    }

    /* Primary Submit Action (Vibrant Royal Blue with Bold White Text) */
    div.primary-btn .stButton > button,
    div.primary-btn button {
        background-color: #2563eb !important;
        background: #2563eb !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.01em !important;
        border: 1px solid #1d4ed8 !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.15s ease !important;
    }

    div.primary-btn .stButton > button:hover,
    div.primary-btn button:hover {
        background-color: #1d4ed8 !important;
        background: #1d4ed8 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
    }

    /* Result Banner */
    .status-banner {
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        font-size: 1.05rem;
    }

    .status-banner.verified {
        background-color: var(--green-bg);
        border: 1px solid var(--green-border);
        color: #065f46;
    }

    .status-banner.fake {
        background-color: var(--red-bg);
        border: 1px solid var(--red-border);
        color: #991b1b;
    }

    .status-tag {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }

    .status-banner.verified .status-tag {
        background-color: rgba(5, 150, 105, 0.15);
        color: #047857;
    }

    .status-banner.fake .status-tag {
        background-color: rgba(220, 38, 38, 0.15);
        color: #b91c1c;
    }

    /* Fact Check Advisory Box */
    .fact-check-box {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 1.25rem;
        color: #991b1b;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Confidence Progress */
    .confidence-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-heading);
        margin-bottom: 0.35rem;
    }

    .progress-bar-container {
        width: 100%;
        height: 10px;
        background-color: #f1f5f9;
        border-radius: 9999px;
        overflow: hidden;
        margin-bottom: 1.25rem;
    }

    .progress-bar-fill {
        height: 100%;
        border-radius: 9999px;
    }

    .progress-bar-fill.verified {
        background-color: var(--accent-green);
    }

    .progress-bar-fill.fake {
        background-color: var(--accent-red);
    }

    /* Metadata Grid */
    .meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .meta-box {
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.75rem 1rem;
    }

    .meta-box-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.2rem;
    }

    .meta-box-value {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-heading);
    }

    /* Footer */
    .footer-container {
        text-align: center;
        border-top: 1px solid var(--border-subtle);
        padding-top: 1.75rem;
        margin-top: 2rem;
    }

    .footer-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-heading);
        margin-bottom: 0.25rem;
    }

    .footer-note {
        font-size: 0.775rem;
        color: var(--text-muted);
        max-width: 600px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# 1. Top Navbar
st.markdown("""
<div class="custom-navbar">
    <div class="nav-brand">
        <span>📰</span> Fake News & Multilingual Fact-Checking Engine
    </div>
    <div class="nav-meta">
        <span class="model-badge">Engine: Multilingual Passive-Aggressive + Knowledge XAI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Hero Intro
st.markdown("""
<div class="hero-container">
    <h1 class="hero-heading">Analyze News & Fact Credibility</h1>
    <p class="hero-subtext">
        Verify general facts, claims, or full news articles across English, Odia, Hindi, Bengali, French, Spanish, German, Japanese, and 16+ languages in real time.
    </p>
</div>
""", unsafe_allow_html=True)

# 3. Dropdown Menu for Pre-loaded News & Fact-Check Selection
st.selectbox(
    "Select a Current News Article or Global Report:",
    options=list(SAMPLE_ARCHIVE.keys()),
    key="selected_sample",
    on_change=on_dropdown_select,
    help="Select a current news article to populate the text area."
)

# 4. Multi-Modal Document / Image / PPT Uploader
uploaded_file = st.file_uploader(
    "Upload Document, News Screenshot, Presentation, or PDF (DOCX, PPTX, PDF, PNG, JPG, TXT):",
    type=["png", "jpg", "jpeg", "webp", "bmp", "docx", "pptx", "pdf", "txt"],
    key="media_uploader",
    help="Upload any screenshot or document. Text is extracted automatically via native OCR and parsers."
)

if uploaded_file is not None:
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.get("last_uploaded_id") != file_id:
        with st.spinner("Extracting text and scanning media..."):
            file_bytes = uploaded_file.read()
            extracted_txt, ftype = extract_text_from_file(file_bytes, uploaded_file.name)
            if extracted_txt and not extracted_txt.startswith("[Error") and not extracted_txt.startswith("[Unsupported"):
                st.session_state.input_content = extracted_txt
                st.session_state.last_uploaded_id = file_id
                st.session_state.upload_notice = f"Extracted {len(extracted_txt.split())} words from {ftype} ({uploaded_file.name})"
            else:
                st.error(extracted_txt)

if st.session_state.get("upload_notice"):
    st.success(f"✅ {st.session_state.upload_notice}")

# 5. Inference Input Form
content_val = st.text_area(
    "News Content, Fact Claim, or Transcript * (Write anything yourself or paste below)",
    key="input_content",
    placeholder="Type or paste any news article, viral message, or factual claim here (e.g. 'Cows have 5 legs', 'Earth is flat', or any multilingual news in English, Hindi, Bengali, Odia, French, Japanese, etc.)...",
    height=200
)

# Prominent Submit Action
st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
submitted = st.button("Detect Authenticity & Verify Fact", key="btn_submit", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Instant Classification & Multilingual Fact-Checking Evaluation
if submitted:
    text_to_eval = st.session_state.input_content.strip()

    if not text_to_eval:
        st.warning("Please enter text, claim, or upload a document/image to evaluate.")
    else:
        # Run Unified Multilingual & Fact-Checking Evaluation
        res = evaluate_multilingual_content("", text_to_eval, model=get_model())

        st.session_state.result = res
        st.session_state.evaluated = True

# 6. Dynamic Prediction Result Block
if st.session_state.evaluated and st.session_state.result:
    res = st.session_state.result
    is_real = res["prediction"] == "REAL"
    is_fact_check = res.get("fact_check_flag", False)

    st.markdown("---")

    # Status Banner
    if is_real:
        st.markdown(f"""
        <div class="status-banner verified">
            <span>🟢 VERIFIED / RELIABLE CONTENT</span>
            <span class="status-tag">VERIFIED BY ENGINE</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        banner_tag_text = "EMPIRICAL FALLACY" if is_fact_check else "DECEPTIVE PATTERNS"
        banner_title_text = "🔴 FACT CHECK: FALSE / DECEPTIVE CLAIM" if is_fact_check else "🔴 WARNING: FAKE / UNRELIABLE CONTENT"
        st.markdown(f"""
        <div class="status-banner fake">
            <span>{banner_title_text}</span>
            <span class="status-tag">{banner_tag_text}</span>
        </div>
        """, unsafe_allow_html=True)

    # Fact-Check Advisory Note (if applicable)
    if is_fact_check and res.get("fact_check_note"):
        st.markdown(f"""
        <div class="fact-check-box">
            <strong>⚠️ Empirical Fact-Check Advisory:</strong> {res['fact_check_note']}
        </div>
        """, unsafe_allow_html=True)

    # Confidence Progress Bar
    conf_class = "verified" if is_real else "fake"
    conf_label = "Reliability Confidence Score" if is_real else "Deception Likelihood Score"
    st.markdown(f"""
    <div class="confidence-meta">
        <span>{conf_label}</span>
        <span>{res['confidence']}%</span>
    </div>
    <div class="progress-bar-container">
        <div class="progress-bar-fill {conf_class}" style="width: {res['confidence']}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Analysis Metadata Two-Column Grid
    st.markdown(f"""
    <div class="meta-grid">
        <div class="meta-box">
            <div class="meta-box-label">Text Word Count</div>
            <div class="meta-box-value">{res['word_count']} words</div>
        </div>
        <div class="meta-box">
            <div class="meta-box-label">Detected Language</div>
            <div class="meta-box-value">{res['language_name']}</div>
        </div>
        <div class="meta-box">
            <div class="meta-box-label">Model Latency</div>
            <div class="meta-box-value">{res['latency_ms']}</div>
        </div>
        <div class="meta-box">
            <div class="meta-box-label">Stylistic / Factual Index</div>
            <div class="meta-box-value">{res['style']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Reset Button
    st.button("Reset / Analyze Another Article or Claim", key="btn_reset", on_click=reset_all, use_container_width=True)

# 7. Footer
st.markdown("""
<div class="footer-container">
    <div class="footer-title">Final Year Project | Department of Computer Science & Engineering</div>
    <p class="footer-note">
        Disclaimer: Output is generated via statistical pattern classification and empirical knowledge base for research and educational purposes.
    </p>
</div>
""", unsafe_allow_html=True)
