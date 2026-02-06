import pandas as pd
import sqlite3
import pytesseract
from PIL import Image
import pdfplumber
import re

# --------------------------------------------------
# Tesseract Path
# --------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --------------------------------------------------
# Utility: Normalize Item Names
# --------------------------------------------------
def normalize_item(text):
    if pd.isna(text):
        return text
    text = text.lower()
    text = re.sub(r"\s+", " ", text)   # collapse multiple spaces
    return text.strip()

# --------------------------------------------------
# Load MRP Reference Database
# --------------------------------------------------
def get_mrp_reference():
    conn = sqlite3.connect("fraud_detection.db")
    df = pd.read_sql("SELECT * FROM mrp_reference", conn)
    conn.close()
    return df

# --------------------------------------------------
# Fraud Detection Logic (NO DISPLAY NAMES HERE)
# --------------------------------------------------
def check_fraud(bill_df):
    if bill_df.empty:
        return pd.DataFrame(columns=[
            "item",
            "quantity",
            "billed_mrp",
            "mrp_price",
            "expected_price",
            "extra_amount",
            "status"
        ])

    mrp_df = get_mrp_reference()

    # Normalize item names
    bill_df["item"] = bill_df["item"].apply(normalize_item)
    mrp_df["item"] = mrp_df["item"].apply(normalize_item)

    # Merge bill with MRP reference
    merged = pd.merge(bill_df, mrp_df, on="item", how="left")

    # Price calculations
    merged["expected_price"] = merged["mrp_price"] * merged["quantity"]
    merged["extra_amount"] = merged["billed_mrp"] - merged["expected_price"]

    # Explicit status logic (NO silent Valid)
    def detect_status(row):
        if pd.isna(row["mrp_price"]):
            return "MRP Not Found"
        elif row["extra_amount"] > 0:
            return "Fraud Detected"
        else:
            return "Valid"

    merged["status"] = merged.apply(detect_status, axis=1)

    return merged

# --------------------------------------------------
# OCR for Images (JPG / PNG)
# --------------------------------------------------
def ocr_to_dataframe(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)

        data = []
        for line in text.splitlines():
            parts = line.replace(",", " ").replace("\t", " ").split()
            if len(parts) >= 3:
                try:
                    item = " ".join(parts[:-2]).strip()
                    qty = int(parts[-2])
                    price = float(parts[-1])
                    data.append({
                        "item": item,
                        "quantity": qty,
                        "billed_mrp": price
                    })
                except ValueError:
                    continue

        return pd.DataFrame(data, columns=["item", "quantity", "billed_mrp"])

    except Exception as e:
        print("OCR error:", e)
        return pd.DataFrame(columns=["item", "quantity", "billed_mrp"])

# --------------------------------------------------
# PDF Parsing
# --------------------------------------------------
def pdf_to_dataframe(pdf_file):
    data = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.splitlines():
                    parts = line.replace(",", " ").replace("\t", " ").split()
                    if len(parts) >= 3:
                        try:
                            item = " ".join(parts[:-2]).strip()
                            qty = int(parts[-2])
                            price = float(parts[-1])
                            data.append({
                                "item": item,
                                "quantity": qty,
                                "billed_mrp": price
                            })
                        except ValueError:
                            continue

        return pd.DataFrame(data, columns=["item", "quantity", "billed_mrp"])

    except Exception as e:
        print("PDF parsing error:", e)
        return pd.DataFrame(columns=["item", "quantity", "billed_mrp"])
