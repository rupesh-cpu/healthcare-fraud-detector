import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st

from backend import check_fraud, ocr_to_dataframe, pdf_to_dataframe


st.set_page_config(page_title="ClearBill | Healthcare billing review", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

COPY = {
    "English": {"title": "Know what you are paying for.", "subtitle": "Upload a hospital bill to compare medicine prices with the reference MRP database.", "step": "Step 1 of 2", "upload_title": "Add a bill for review", "upload_help": "Your bill is processed only for this review session.", "pdf": "PDF document", "image": "Image file", "camera": "Camera scan", "select": "Choose a bill file", "scan": "Take a clear photo of the bill", "analyze": "Analyze bill", "review_title": "Review complete", "review_subtitle": "Here is a clear breakdown of the extracted bill items.", "items": "Items analyzed", "flagged": "Items flagged", "rate": "Flag rate", "excess": "Potential excess", "no_items": "We couldn't identify any bill items. Try a clearer image or a text-based PDF.", "details": "Item-by-item review", "summary": "Risk summary", "download": "Download review as CSV", "empty": "Upload a bill, then select Analyze bill to see the review here.", "privacy": "Private session · Reference-price check · No account required", "footer": "ClearBill is a decision-support tool. Confirm concerns with the provider or a qualified authority."},
    "हिन्दी": {"title": "जानें कि आप किसके लिए भुगतान कर रहे हैं।", "subtitle": "दवा की कीमतों को संदर्भ MRP डेटाबेस से मिलाने के लिए अस्पताल का बिल अपलोड करें।", "step": "2 में से चरण 1", "upload_title": "जांच के लिए बिल जोड़ें", "upload_help": "आपका बिल केवल इस समीक्षा सत्र के लिए संसाधित किया जाता है।", "pdf": "PDF दस्तावेज़", "image": "छवि फ़ाइल", "camera": "कैमरा स्कैन", "select": "बिल फ़ाइल चुनें", "scan": "बिल की स्पष्ट तस्वीर लें", "analyze": "बिल जांचें", "review_title": "समीक्षा पूरी हुई", "review_subtitle": "निकाले गए बिल आइटम का स्पष्ट विवरण यहाँ है।", "items": "जांचे गए आइटम", "flagged": "चिह्नित आइटम", "rate": "चिह्नित दर", "excess": "संभावित अतिरिक्त राशि", "no_items": "कोई बिल आइटम नहीं मिला। अधिक स्पष्ट छवि या टेक्स्ट PDF आज़माएं।", "details": "आइटम-वार समीक्षा", "summary": "जोखिम सारांश", "download": "CSV में समीक्षा डाउनलोड करें", "empty": "समीक्षा देखने के लिए बिल अपलोड करें और बिल जांचें चुनें।", "privacy": "निजी सत्र · संदर्भ मूल्य जांच · खाता आवश्यक नहीं", "footer": "ClearBill एक सहायक उपकरण है। चिंता की पुष्टि प्रदाता या योग्य प्राधिकरण से करें।"},
    "मराठी": {"title": "तुम्ही कशासाठी पैसे देता ते जाणून घ्या.", "subtitle": "औषधांच्या किमती संदर्भ MRP डेटाबेसशी पडताळण्यासाठी हॉस्पिटलचे बिल अपलोड करा.", "step": "2 पैकी पायरी 1", "upload_title": "तपासणीसाठी बिल जोडा", "upload_help": "तुमच्या बिलावर फक्त या सत्रात प्रक्रिया केली जाते.", "pdf": "PDF दस्तऐवज", "image": "प्रतिमा फाइल", "camera": "कॅमेरा स्कॅन", "select": "बिल फाइल निवडा", "scan": "बिलचा स्पष्ट फोटो घ्या", "analyze": "बिल तपासा", "review_title": "तपासणी पूर्ण", "review_subtitle": "काढलेल्या बिल आयटमचे स्पष्ट विश्लेषण येथे आहे.", "items": "तपासलेले आयटम", "flagged": "चिन्हांकित आयटम", "rate": "चिन्हांकित दर", "excess": "संभाव्य जास्तीची रक्कम", "no_items": "बिल आयटम सापडले नाहीत. स्पष्ट प्रतिमा किंवा टेक्स्ट PDF वापरून पहा.", "details": "आयटम-निहाय तपासणी", "summary": "जोखीम सारांश", "download": "CSV म्हणून तपासणी डाउनलोड करा", "empty": "तपासणी पाहण्यासाठी बिल अपलोड करा आणि बिल तपासा निवडा.", "privacy": "खासगी सत्र · संदर्भ किंमत तपासणी · खाते आवश्यक नाही", "footer": "ClearBill हे निर्णय-सहाय्यक साधन आहे. प्रदाता किंवा योग्य प्राधिकरणाकडून खात्री करा."},
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
:root { --ink:#13233b; --muted:#68758a; --line:#e4e9f0; --blue:#1769e0; --navy:#0c2444; }
.stApp { background:#f6f8fb; color:var(--ink); } html,body,[class*="css"] { font-family:'DM Sans',sans-serif; } #MainMenu,footer,header { visibility:hidden; }
.block-container { max-width:1180px; padding-top:2.2rem; padding-bottom:2rem; }.brand { display:flex;align-items:center;gap:10px;font-weight:700;color:var(--navy);letter-spacing:-.02em; }.brand-mark { width:35px;height:35px;display:grid;place-items:center;border-radius:11px;background:#e5f0ff;font-size:19px; }
.eyebrow { color:var(--blue);font-size:.77rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;margin:0 0 11px; }.hero { padding:42px 46px;border-radius:24px;background:radial-gradient(circle at 83% 15%,#285d9e 0,#102b4d 34%,#091d36 100%);color:#fff;position:relative;overflow:hidden; }.hero:after { content:'';position:absolute;width:270px;height:270px;border:1px solid rgba(255,255,255,.13);border-radius:50%;right:-65px;bottom:-150px; }.hero h1 { max-width:660px;font-family:'Fraunces',serif;font-size:clamp(2.15rem,4.3vw,3.55rem);line-height:1.08;letter-spacing:-.045em;margin:0 0 14px; }.hero p { max-width:590px;margin:0;color:#c9d9eb;font-size:1.05rem;line-height:1.55; }.trust { display:inline-flex;margin-top:23px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;padding:7px 11px;color:#dceaff;font-size:.79rem; }
.panel { background:#fff;border:1px solid var(--line);box-shadow:0 12px 30px rgba(25,48,82,.05);border-radius:20px;padding:27px; }.panel h2 { font-size:1.2rem;margin:0 0 5px;letter-spacing:-.025em; }.panel p { color:var(--muted);margin:0 0 20px; }.metric { background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;min-height:113px; }.metric-label { color:var(--muted);font-size:.82rem;font-weight:600; }.metric-value { font-size:1.75rem;font-weight:700;letter-spacing:-.05em;margin-top:8px; }.status-note { padding:18px;border:1px dashed #cdd8e7;border-radius:16px;color:var(--muted);text-align:center;background:#fbfcfe; }.section-title { font-size:1.22rem;font-weight:700;letter-spacing:-.03em;margin:30px 0 13px; }.footer-note { text-align:center;color:#7c899a;font-size:.8rem;padding-top:29px; }
.stButton>button { background:var(--blue);color:white;border:0;border-radius:10px;font-weight:700;padding:.62rem 1.2rem; }.stButton>button:hover { background:#0958c4;color:white; }.stDownloadButton>button { border-radius:10px;border:1px solid #c8d4e4;color:var(--navy);font-weight:600; } div[data-baseweb="tab-list"] { gap:8px; } button[data-baseweb="tab"] { border-radius:9px;font-weight:600;padding:8px 14px; } button[data-baseweb="tab"][aria-selected="true"] { background:#e8f1ff;color:#135ec9; } div[data-testid="stFileUploader"] { border:1px dashed #b9c9df;border-radius:13px;padding:7px;background:#fafcff; } @media(max-width:700px) { .block-container { padding:1rem; }.hero { padding:31px 25px;border-radius:18px; }.panel { padding:20px; } }
</style>
""", unsafe_allow_html=True)

if "fraud_results" not in st.session_state: st.session_state.fraud_results = None
if "file_token" not in st.session_state: st.session_state.file_token = None

top_left, top_right = st.columns([5, 1])
with top_left: st.markdown('<div class="brand"><span class="brand-mark">✦</span> ClearBill</div>', unsafe_allow_html=True)
with top_right: language = st.selectbox("Language", list(COPY), label_visibility="collapsed")
t = COPY[language]
st.markdown(f'<div class="hero"><div class="eyebrow" style="color:#80b2ff">Healthcare billing review</div><h1>{t["title"]}</h1><p>{t["subtitle"]}</p><div class="trust">🛡️ {t["privacy"]}</div></div>', unsafe_allow_html=True)
st.write("")

left, right = st.columns([1.18, .82], gap="large")
with left:
    st.markdown(f'<div class="panel"><div class="eyebrow">{t["step"]}</div><h2>{t["upload_title"]}</h2><p>{t["upload_help"]}</p>', unsafe_allow_html=True)
    tabs = st.tabs([f"📄 {t['pdf']}", f"🖼️ {t['image']}", f"📷 {t['camera']}"])
    with tabs[0]: pdf_upload = st.file_uploader(t["select"], type=["pdf"], key="pdf_upload")
    with tabs[1]: image_upload = st.file_uploader(t["select"], type=["jpg", "jpeg", "png"], key="image_upload")
    with tabs[2]: camera_upload = st.camera_input(t["scan"], key="camera_upload")
    uploaded, source = next(
        ((file, kind) for file, kind in ((pdf_upload, "pdf"), (image_upload, "image"), (camera_upload, "camera")) if file),
        (None, ""),
    )
    if uploaded:
        token = hashlib.sha256(uploaded.getvalue()).hexdigest()
        if token != st.session_state.file_token:
            st.session_state.fraud_results, st.session_state.file_token = None, token
        info_col, action_col = st.columns([3, 1])
        with info_col: st.caption(f"Ready to review: {uploaded.name}")
        with action_col: analyze = st.button(t["analyze"], type="primary", use_container_width=True)
        if analyze:
            with st.spinner("Reading bill and checking reference prices…"):
                extracted = pdf_to_dataframe(uploaded) if source == "pdf" else ocr_to_dataframe(uploaded)
                st.session_state.fraud_results = check_fraud(extracted)
    st.markdown("</div>", unsafe_allow_html=True)
with right:
    st.markdown('<div class="panel"><div class="eyebrow">How it works</div><h2>Simple, transparent checks</h2><p>We extract line items, match known medicines, and make possible price differences easy to inspect.</p><hr style="border:0;border-top:1px solid #e7ebf0;margin:18px 0"><p style="font-size:.88rem;margin-bottom:0">Tip: For best results, ensure item name, quantity, and price are visible in the image.</p></div>', unsafe_allow_html=True)

result = st.session_state.fraud_results
if result is None:
    st.markdown(f'<div class="section-title">{t["review_title"]}</div><div class="status-note">{t["empty"]}</div>', unsafe_allow_html=True)
elif result.empty:
    st.warning(t["no_items"])
else:
    display = result.rename(columns={"item":"Item", "quantity":"Quantity", "billed_mrp":"Billed price (₹)", "mrp_price":"Reference MRP (₹)", "expected_price":"Expected total (₹)", "extra_amount":"Potential excess (₹)", "status":"Review status"}).copy()
    total = len(display); flagged = int((display["Review status"] == "Fraud Detected").sum()); missing = int((display["Review status"] == "MRP Not Found").sum()); rate = flagged / total * 100; excess = display.loc[display["Review status"] == "Fraud Detected", "Potential excess (₹)"].sum()
    st.markdown(f'<div class="section-title">{t["review_title"]}</div><p style="color:#68758a;margin-top:-7px">{t["review_subtitle"]}</p>', unsafe_allow_html=True)
    cards = st.columns(4)
    for col, (label, value, color) in zip(cards, [(t["items"],str(total),"#1769e0"),(t["flagged"],str(flagged),"#d94b46"),(t["rate"],f"{rate:.0f}%","#d94b46"),(t["excess"],f"₹{excess:,.2f}","#d94b46")]): col.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value" style="color:{color}">{value}</div></div>', unsafe_allow_html=True)
    chart_col, insight_col = st.columns([1.45, .8], gap="large")
    with chart_col:
        st.markdown(f'<div class="section-title">{t["details"]}</div>', unsafe_allow_html=True)
        chart_data = display.sort_values("Potential excess (₹)", ascending=False)
        figure = px.bar(chart_data, x="Potential excess (₹)", y="Item", orientation="h", color="Review status", color_discrete_map={"Fraud Detected":"#dc5b55", "Valid":"#2a9d78", "MRP Not Found":"#e3a531"})
        figure.update_layout(height=max(270,len(chart_data)*50), margin=dict(l=0,r=10,t=8,b=0), legend_title_text="", plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", xaxis_title=None, yaxis_title=None); figure.update_xaxes(gridcolor="#edf0f4", zerolinecolor="#edf0f4")
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar":False})
    with insight_col:
        st.markdown(f'<div class="section-title">{t["summary"]}</div>', unsafe_allow_html=True)
        status_counts = display["Review status"].value_counts().rename_axis("Status").reset_index(name="Items")
        donut = px.pie(status_counts, names="Status", values="Items", hole=.67, color="Status", color_discrete_map={"Fraud Detected":"#dc5b55", "Valid":"#2a9d78", "MRP Not Found":"#e3a531"}); donut.update_layout(height=225,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(donut, use_container_width=True, config={"displayModeBar":False}); st.caption(f"{missing} item(s) could not be matched to a reference MRP.")
    st.markdown(f'<div class="section-title">{t["details"]}</div>', unsafe_allow_html=True)
    def status_style(value):
        colors = {"Fraud Detected": "#ffe8e6", "Valid": "#e5f6ef", "MRP Not Found": "#fff3d9"}
        return f"background-color: {colors.get(value, '#fff')}; font-weight:600"
    st.dataframe(display.style.map(status_style, subset=["Review status"]).format({"Billed price (₹)":"₹{:.2f}","Reference MRP (₹)":"₹{:.2f}","Expected total (₹)":"₹{:.2f}","Potential excess (₹)":"₹{:.2f}"}, na_rep="—"), use_container_width=True, hide_index=True)
    st.download_button(t["download"], display.to_csv(index=False).encode("utf-8"), "clearbill-review.csv", "text/csv")
st.markdown(f'<div class="footer-note">{t["footer"]}</div>', unsafe_allow_html=True)
