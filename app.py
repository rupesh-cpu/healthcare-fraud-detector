import streamlit as st
import pandas as pd
import plotly.express as px
from backend import check_fraud, ocr_to_dataframe, pdf_to_dataframe

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Healthcare Fraud Detector",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Global CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
body { background: linear-gradient(135deg, #F2F6FA, #EAF0F6); }
.app-header { background: linear-gradient(90deg, #0B3C5D, #1A5276); padding: 32px; border-radius: 16px; text-align: center; margin-bottom: 32px; }
.metric-card { background: white; padding: 22px; border-radius: 16px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: transform 0.2s ease; }
.metric-card:hover { transform: translateY(-4px); }
.metric-title { font-size: 14px; font-weight: 600; color: #566573; }
.metric-value { font-size: 30px; font-weight: 700; color: #1C2833; margin-top: 6px; }
footer { text-align: center; color: #7F8C8D; font-size: 14px; margin-top: 40px; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
lang = st.selectbox("🌐 Choose Language / भाषा निवडा", ["English", "हिन्दी", "मराठी"])

translations = {
    "English": {
        "title": "Healthcare Billing Fraud Detector",
        "subtitle": "AI-assisted verification of hospital billing and medicine pricing",
        "input_method": "Choose Input Method",
        "upload_pdf": "Upload Bill PDF",
        "upload_image": "Upload Bill Image",
        "camera": "Scan Bill Using Camera",
        "results": "Fraud Detection Results",
        "total_items": "Items Analyzed",
        "fraud_cases": "Fraud Detected",
        "fraud_percent": "Fraud Rate",
        "extra_charged": "Excess Amount",
        "warning": "No valid bill items detected.",
        "view_bill": "View Bill"
    },
    "हिन्दी": {
        "title": "स्वास्थ्य बिलिंग धोखाधड़ी डिटेक्टर",
        "subtitle": "अस्पताल बिल और दवा मूल्य का एआई आधारित सत्यापन",
        "input_method": "इनपुट विधि चुनें",
        "upload_pdf": "बिल PDF अपलोड करें",
        "upload_image": "बिल इमेज अपलोड करें",
        "camera": "कैमरे से स्कैन करें",
        "results": "जांच परिणाम",
        "total_items": "जांचे गए आइटम",
        "fraud_cases": "धोखाधड़ी",
        "fraud_percent": "धोखाधड़ी दर",
        "extra_charged": "अतिरिक्त शुल्क",
        "warning": "कोई वैध आइटम नहीं मिला।",
        "view_bill": "बिल देखें"
    },
    "मराठी": {
        "title": "आरोग्य बिलिंग फसवणूक शोधक",
        "subtitle": "रुग्णालय बिल व औषध दरांचे एआय आधारित विश्लेषण",
        "input_method": "इनपुट पद्धत निवडा",
        "upload_pdf": "PDF अपलोड करा",
        "upload_image": "इमेज अपलोड करा",
        "camera": "कॅमेऱ्याने स्कॅन करा",
        "results": "तपासणी निकाल",
        "total_items": "तपासलेले आयटम",
        "fraud_cases": "फसवणूक",
        "fraud_percent": "फसवणूक दर",
        "extra_charged": "अतिरिक्त रक्कम",
        "warning": "वैध आयटम आढळले नाहीत.",
        "view_bill": "बिल पहा"
    }
}

# --------------------------------------------------
# Header with Hero Image
# --------------------------------------------------
st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=120)
st.markdown(f"""
<div class="app-header">
    <h1 style="color:white;margin-bottom:8px;">{translations[lang]['title']}</h1>
    <p style="color:#D6EAF8;font-size:17px;">{translations[lang]['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Input Method
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

# --------------------------------------------------
# Upload Handling with View Button + Spinner + Progress
# --------------------------------------------------
if option == translations[lang]["upload_pdf"]:
    pdf = st.file_uploader("", type=["pdf"])
    if pdf:
        if st.button(translations[lang]["view_bill"]):
            st.download_button("📄 Open PDF", data=pdf.read(), file_name=pdf.name, mime="application/pdf")
        with st.spinner("🔍 Analyzing your bill..."):
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            st.session_state["fraud_results"] = check_fraud(pdf_to_dataframe(pdf))

elif option == translations[lang]["upload_image"]:
    img = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if img:
        if st.button(translations[lang]["view_bill"]):
            st.image(img, caption="Uploaded Bill", use_container_width=True)
        with st.spinner("🔍 Analyzing your bill..."):
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            st.session_state["fraud_results"] = check_fraud(ocr_to_dataframe(img))

elif option == translations[lang]["camera"]:
    cam = st.camera_input("")
    if cam:
        if st.button(translations[lang]["view_bill"]):
            st.image(cam, caption="Scanned Bill", use_container_width=True)
        with st.spinner("🔍 Analyzing your bill..."):
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            st.session_state["fraud_results"] = check_fraud(ocr_to_dataframe(cam))

# --------------------------------------------------
# Results Display with Color Coding + Extra Chart
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

    # Pie chart
    st.plotly_chart(
        px.pie(pd.DataFrame({"Status": ["Fraud", "Valid"], "Count": [fraud_count, total_items - fraud_count]}),
               names="Status", values="Count", hole=0.45),
        use_container_width=True
    )

    # Bar chart
    st.plotly_chart(
        px.bar(result, x="item", y="extra_amount", color="status", title="Fraud Distribution by Item"),
        use_container_width=True
    )

    # Color-coded table
    def highlight_fraud(val):
        return 'background-color: #F1948A' if val == "Fraud Detected" else 'background-color: #82E0AA'

    st.dataframe(result.style.map(highlight_fraud, subset=["status"]), use_container_width=True)

# --------------------------------------------------
# Persistent Results
# --------------------------------------------------
def show_results(result):
    if result.empty:
        st.warning(translations[lang]["warning"])
        return

    # ✅ Rename columns for display only
    result_display = result.rename(columns={
        "item": "Item Name",
        "quantity": "Quantity",
        "billed_mrp": "Billed Price (₹)",
        "mrp_price": "MRP Price (₹)",
        "expected_price": "Expected Price (₹)",
        "extra_amount": "Excess Amount (₹)",
        "status": "Fraud Status"
    })

    # Use result_display everywhere in charts and tables
    total_items = len(result_display)
    fraud_count = (result_display["Fraud Status"] == "Fraud Detected").sum()
    fraud_percent = (fraud_count / total_items) * 100
    total_extra = result_display["Excess Amount (₹)"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(translations[lang]["total_items"], total_items)
    col2.metric(translations[lang]["fraud_cases"], fraud_count)
    col3.metric(translations[lang]["fraud_percent"], f"{fraud_percent:.2f}%")
    col4.metric(translations[lang]["extra_charged"], f"₹{total_extra:.2f}")

    st.plotly_chart(
        px.bar(result_display, x="Item Name", y="Excess Amount (₹)", color="Fraud Status",
               title="Fraud Distribution by Item"),
        use_container_width=True
    )

    def highlight_fraud(val):
        return 'background-color: #F1948A' if val == "Fraud Detected" else 'background-color: #82E0AA'

    st.dataframe(result_display.style.map(highlight_fraud, subset=["Fraud Status"]), use_container_width=True)
if "fraud_results" in st.session_state:
    show_results(st.session_state["fraud_results"])

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    "<footer>© 2026 Government of India • Digital Health Intelligence Platform</footer>",
    unsafe_allow_html=True
)