# 💊 Healthcare Fraud Detector

## 📌 Overview
Healthcare billing fraud is a growing concern where patients are often charged more than the approved medicine or service prices.  
This app provides an **AI-powered fraud detection system** that automatically verifies hospital bills against a trusted MRP reference database.

---

## 🚀 Features
- **Multi-language UI**: English, Hindi, Marathi support for wider accessibility.
- **Bill Upload Options**:
  - PDF upload
  - Image upload (JPG/PNG)
  - Camera capture (mobile-friendly)
- **AI-Powered OCR**: Uses Tesseract OCR to read text from images and scanned bills.
- **Fraud Detection Logic**:
  - Compares billed prices against official MRP database.
  - Flags items as **Valid**, **Fraud Detected**, or **MRP Not Found**.
- **Interactive Dashboard**:
  - Fraud metrics (total items, fraud cases, fraud percentage, extra charged).
  - Pie chart visualization (fraud vs valid).
  - Results table (item, quantity, billed MRP, actual MRP, status).
- **Secure Deployment**: Authentication layer for faculty/admin access.

---

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/) (Python-based UI framework)
- **Backend**: Python modules for OCR, PDF parsing, fraud detection
- **Database**: SQLite (`fraud_detection.db`) with `mrp_reference` table
- **Libraries**:
  - `pandas` → data handling
  - `plotly` → interactive charts
  - `pytesseract` → OCR engine
  - `pdfplumber` → PDF parsing
  - `sqlite3` → database integration

---

## ⚙️ How It Works
1. **Upload Bill** (PDF, image, or camera scan).
2. **OCR/PDF Parsing** extracts items, quantities, and billed prices.
3. **Fraud Detection** compares extracted data with MRP reference database.
4. **Dashboard** displays fraud metrics, pie chart, and detailed results table.

---

## 🧠 AI Component
- **Computer Vision (OCR)**: Reads text from images and scanned bills using Tesseract.
- **Data Intelligence**: Applies fraud detection logic to identify overbilling.
- **Future Scope**:
  - ML models for anomaly detection.
  - NLP for parsing complex bill formats.
  - Trend analysis across hospitals.

---

## 🌐 Impact
- **Patients**: Protects against hidden charges.
- **Hospitals**: Builds trust and compliance.
- **Government/Institutions**: Encourages transparency and accountability.

---

## 📊 Example Output
| Item          | Quantity | Billed MRP | Actual MRP | Status          |
|---------------|----------|------------|------------|-----------------|
| Paracetamol   | 2        | 20         | 10         | Fraud Detected  |
| Amoxicillin   | 1        | 45         | 45         | Valid           |
| Ibuprofen     | 3        | 90         | 30         | Fraud Detected  |
| Blood Test    | 1        | 120        | 120        | Valid           |

---

## 🔮 Future Enhancements
- Role-based dashboards (patients vs faculty vs admin).
- Integration with government health databases.
- Mobile app wrapper with custom manifest (native icon + branding).
- Advanced analytics for fraud trends.

---

## 📜 License
© 2026 Government of India – Healthcare Fraud Detection Initiative  
Developed by **Rupesh Ramnath Patare**  
- Keep mrp_master.csv updated with latest MRP data.
- fraud_detection.db is auto-generated.
- Use sample_bills/ for testing.
