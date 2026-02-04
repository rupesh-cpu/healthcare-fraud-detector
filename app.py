import streamlit as st
import pandas as pd
import plotly.express as px
from backend import check_fraud, ocr_to_dataframe, pdf_to_dataframe

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Healthcare Fraud Detector",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Global CSS
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #F4F6F7;
}
.metric-card {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.metric-title {
    font-size: 15px;
    font-weight: 600;
    color: #34495E;
}
.metric-value {
    font-size: 26px;
    font-weight: 700;
    margin-top: 6px;
}
.section-box {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.alert-box {
    background: #FDEDEC;
    padding: 14px;
    border-left: 5px solid #C0392B;
    border-radius: 6px;
    font-weight: 600;
    color: #922B21;
    margin-top: 16px;
}
footer {
    text-align: center;
    color: #7B7D7D;
    font-size: 14px;
    margin-top: 30px;
}
.suggestion {
    padding: 8px;
    border-bottom: 1px solid #E5E7E9;
    cursor: pointer;
}
.suggestion:hover {
    background-color: #EBF5FB;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
lang = st.selectbox("Choose Language / भाषा चुनें", ["English", "हिन्दी", "मराठी"])

translations = {
    "English": {
        "title": "Healthcare Billing Fraud Detector",
        "subtitle": "Upload hospital bills and verify approved medicine prices.",
        "input_method": "Choose Input Method",
        "upload_pdf": "Upload Bill PDF",
        "upload_image": "Upload Bill Image",
        "camera": "Scan Bill Using Camera",
        "search_title": "Medicine Price Search",
        "search_placeholder": "Type medicine name",
        "results": "Fraud Detection Results",
        "total_items": "Total Items Checked",
        "fraud_cases": "Fraud Cases Detected",
        "fraud_percent": "Fraud Percentage",
        "extra_charged": "Total Extra Charged",
        "download": "Download Results as CSV",
        "warning": "No valid items detected."
    },
    "हिन्दी": {
        "title": "स्वास्थ्य बिलिंग धोखाधड़ी डिटेक्टर",
        "subtitle": "अस्पताल बिल अपलोड करें और दवा मूल्य जांचें।",
        "input_method": "इनपुट विधि चुनें",
        "upload_pdf": "बिल PDF अपलोड करें",
        "upload_image": "बिल इमेज अपलोड करें",
        "camera": "कैमरे से स्कैन करें",
        "search_title": "दवा मूल्य खोज",
        "search_placeholder": "दवा का नाम टाइप करें",
        "results": "जांच परिणाम",
        "total_items": "कुल आइटम",
        "fraud_cases": "धोखाधड़ी",
        "fraud_percent": "धोखाधड़ी प्रतिशत",
        "extra_charged": "अतिरिक्त शुल्क",
        "download": "CSV डाउनलोड करें",
        "warning": "कोई वैध आइटम नहीं मिला।"
    },
    "मराठी": {
        "title": "आरोग्य बिलिंग फसवणूक शोधक",
        "subtitle": "रुग्णालय बिल अपलोड करा व औषध दर तपासा.",
        "input_method": "इनपुट पद्धत निवडा",
        "upload_pdf": "PDF अपलोड करा",
        "upload_image": "इमेज अपलोड करा",
        "camera": "कॅमेऱ्याने स्कॅन करा",
        "search_title": "औषध दर शोध",
        "search_placeholder": "औषध नाव टाइप करा",
        "results": "तपासणी निकाल",
        "total_items": "एकूण आयटम",
        "fraud_cases": "फसवणूक",
        "fraud_percent": "टक्केवारी",
        "extra_charged": "अतिरिक्त रक्कम",
        "download": "CSV डाउनलोड करा",
        "warning": "वैध आयटम आढळले नाहीत."
    }
}

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(f"""
<div style="background:#1A5276;padding:26px;border-radius:12px;text-align:center;margin-bottom:30px;">
    <h1 style="color:white;">{translations[lang]['title']}</h1>
    <p style="color:#ECF0F1;">{translations[lang]['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Input Method (Upload Section)
# --------------------------------------------------
option = st.radio(
    translations[lang]["input_method"],
    [
        translations[lang]["upload_pdf"],
        translations[lang]["upload_image"],
        translations[lang]["camera"]
    ],
    horizontal=True
)

uploaded = False

if option == translations[lang]["upload_pdf"]:
    pdf = st.file_uploader("", type=["pdf"])
    if pdf:
        uploaded = True
        show_df = check_fraud(pdf_to_dataframe(pdf))

elif option == translations[lang]["upload_image"]:
    img = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if img:
        uploaded = True
        show_df = check_fraud(ocr_to_dataframe(img))

elif option == translations[lang]["camera"]:
    cam = st.camera_input("")
    if cam:
        uploaded = True
        show_df = check_fraud(ocr_to_dataframe(cam))

# --------------------------------------------------
# Medicine MRP Database (Replace later with CSV/DB)
# --------------------------------------------------
medicine_db = pd.DataFrame({
    "medicine_name": [
        "Paracetamol", "Amoxicillin", "Azithromycin",
        "Cetirizine", "Ibuprofen", "Metformin",
        "Pantoprazole", "Dolo 650", "Crocin"
    ],
    "mrp_price": [25, 110, 120, 18, 30, 45, 70, 30, 28],
    "category": [
        "Pain Relief", "Antibiotic", "Antibiotic",
        "Antihistamine", "Pain Relief", "Diabetes",
        "Gastric", "Pain Relief", "Pain Relief"
    ]
})

# --------------------------------------------------
# Medicine Smart Search (BELOW Upload Section)
# --------------------------------------------------
st.markdown(f"<div class='section-box'><h3>{translations[lang]['search_title']}</h3>", unsafe_allow_html=True)

query = st.text_input(translations[lang]["search_placeholder"])

if query:
    matches = medicine_db[
        medicine_db["medicine_name"].str.contains(query, case=False)
    ].head(5)

    for _, row in matches.iterrows():
        if st.button(row["medicine_name"]):
            st.success(
                f"Medicine: {row['medicine_name']} | "
                f"MRP: ₹{row['mrp_price']} | "
                f"Category: {row['category']}"
            )

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Fraud Results
# --------------------------------------------------
def show_results(result):
    if result.empty:
        st.warning(translations[lang]["warning"])
        return

    total_items = len(result)
    fraud_count = (result["status"] == "Fraud Detected").sum()
    fraud_percent = (fraud_count / total_items) * 100
    total_extra = result["extra_amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='metric-card'><div class='metric-title'>{translations[lang]['total_items']}</div><div class='metric-value'>{total_items}</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'><div class='metric-title'>{translations[lang]['fraud_cases']}</div><div class='metric-value'>{fraud_count}</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-card'><div class='metric-title'>{translations[lang]['fraud_percent']}</div><div class='metric-value'>{fraud_percent:.2f}%</div></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric-card'><div class='metric-title'>{translations[lang]['extra_charged']}</div><div class='metric-value'>₹{total_extra:.2f}</div></div>", unsafe_allow_html=True)

    chart_df = pd.DataFrame({
        "Status": ["Fraud", "Valid"],
        "Count": [fraud_count, total_items - fraud_count]
    })

    st.plotly_chart(px.pie(chart_df, names="Status", values="Count", hole=0.4), use_container_width=True)

# Show fraud results if uploaded
if uploaded:
    show_results(show_df)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("<footer>© 2026 Government of India – Healthcare Fraud Detection Initiative</footer>", unsafe_allow_html=True)
