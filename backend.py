import pandas as pd
import sqlite3
import pytesseract
from PIL import Image
import pdfplumber

# Path to Tesseract (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# Load MRP Reference Database
# -----------------------------
def get_mrp_reference():
    conn = sqlite3.connect("fraud_detection.db")
    df = pd.read_sql("SELECT * FROM mrp_reference", conn)
    conn.close()
    return df

# -----------------------------
# Fraud Detection Logic
# -----------------------------
def check_fraud(bill_df):
    if bill_df.empty:
        return pd.DataFrame(columns=["item","quantity","billed_mrp","mrp_price","expected_price","extra_amount","status"])
    
    mrp_df = get_mrp_reference()
    # normalize item names
    bill_df["item"] = bill_df["item"].str.strip().str.lower()
    mrp_df["item"] = mrp_df["item"].str.strip().str.lower()
    
    merged = pd.merge(bill_df, mrp_df, on="item", how="left")
    
    # expected price = mrp_price × quantity
    merged["expected_price"] = merged["mrp_price"] * merged["quantity"]
    
    # extra amount charged = billed - expected
    merged["extra_amount"] = merged["billed_mrp"] - merged["expected_price"]
    
    # fraud detection
    merged["status"] = merged.apply(
        lambda row: "Fraud Detected" if pd.notnull(row["mrp_price"]) and row["extra_amount"] > 0 else "Valid",
        axis=1
    )
    
    return merged

# -----------------------------
# OCR for Images (JPG/PNG)
# -----------------------------
def ocr_to_dataframe(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        data = []
        for line in text.splitlines():
            parts = [p.strip() for p in line.replace(",", " ").replace("\t", " ").split()]
            if len(parts) >= 3:
                try:
                    # join everything except last two tokens as item name
                    item = " ".join(parts[:-2]).strip()
                    qty = int(parts[-2])
                    price = float(parts[-1])
                    data.append({"item": item, "quantity": qty, "billed_mrp": price})
                except ValueError:
                    continue
        return pd.DataFrame(data)
    except Exception as e:
        print("OCR error:", e)
        return pd.DataFrame(columns=["item", "quantity", "billed_mrp"])

# -----------------------------
# PDF Parsing
# -----------------------------
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
                            # join everything except last two tokens as item name
                            item = " ".join(parts[:-2]).strip()
                            qty = int(parts[-2])
                            price = float(parts[-1])
                            data.append({"item": item, "quantity": qty, "billed_mrp": price})
                        except ValueError:
                            continue
        return pd.DataFrame(data)
    except Exception as e:
        print("PDF parsing error:", e)
        return pd.DataFrame(columns=["item", "quantity", "billed_mrp"])