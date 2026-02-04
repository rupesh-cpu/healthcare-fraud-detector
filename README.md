Healthcare Fraud Detector
A Streamlit app to detect fraudulent billing in healthcare invoices.
It compares hospital bills (PDF, image, or camera input) against an official MRP database and highlights discrepancies.
Supports English, Hindi, and Marathi with interactive dashboards.

📂 Structure
healthcare-fraud-detector/
├── app.py              # Streamlit frontend
├── backend.py          # Fraud detection, OCR, PDF parsing
├── init_db.py          # Initialize SQLite DB from mrp_master.csv
├── fraud_detection.db  # Auto-created SQLite database
├── mrp_master.csv      # MRP reference dataset
├── sample_bills/       # Demo bills (PDF, image, camera)
├── requirements.txt    # Dependencies
└── README.md           # Documentation



🚀 Features
- Upload bills (PDF, image, camera)
- Fraud detection vs MRP database
- Multilingual support (English, Hindi, Marathi)
- Interactive charts (Plotly)
- Export results as CSV
- Medicine price lookup

▶️ Usage
pip install -r requirements.txt
python init_db.py
streamlit run app.py



📌 Notes
- Keep mrp_master.csv updated with latest MRP data.
- fraud_detection.db is auto-generated.
- Use sample_bills/ for testing.
