import streamlit as st
import os
import pytesseract
from PIL import Image
import re

# ---------- CONFIG ----------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OUTPUT_DIR = "data/outputs"
RAW_TEXT_DIR = os.path.join(OUTPUT_DIR, "raw_text")
EXTRACTED_FIELDS_DIR = os.path.join(OUTPUT_DIR, "extracted_fields")
os.makedirs(RAW_TEXT_DIR, exist_ok=True)
os.makedirs(EXTRACTED_FIELDS_DIR, exist_ok=True)

# ---------- HELPER FUNCTIONS ----------
def extract_text_from_image(image):
    """Perform OCR on an uploaded image"""
    text = pytesseract.image_to_string(image)
    return text

def extract_invoice_fields(text):
    """Simple regex-based extraction for demo"""
    fields = {}
    fields["Invoice Number"] = re.search(r"Invoice\s*#?:?\s*(\w+)", text, re.IGNORECASE)
    fields["Date"] = re.search(r"Date[:\s]*([\w\/\-]+)", text, re.IGNORECASE)
    fields["Total Amount"] = re.search(r"Total[:\s]*\$?([\d\.,]+)", text, re.IGNORECASE)

    clean_fields = {}
    for key, val in fields.items():
        clean_fields[key] = val.group(1) if val else "Not found"
    return clean_fields

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Invoice OCR System", page_icon="🧾", layout="wide")

st.title("🧾 Intelligent Invoice Reader")
st.write("Upload an invoice image (JPG, PNG, JPEG) to extract text and key fields.")

uploaded_file = st.file_uploader("📤 Upload your invoice image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Invoice", use_column_width=True)

    if st.button("🔍 Process Invoice"):
        with st.spinner("Extracting text..."):
            image = Image.open(uploaded_file)
            text = extract_text_from_image(image)

            # Save raw text
            raw_path = os.path.join(RAW_TEXT_DIR, f"{uploaded_file.name}_raw.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(text)

            st.success("✅ Text extracted successfully!")
            st.subheader("📜 Extracted Text")
            st.text_area("Raw OCR Output:", text, height=200)

            # Field Extraction
            st.subheader("🧠 Extracted Invoice Fields")
            fields = extract_invoice_fields(text)
            st.json(fields)

            # Save fields
            field_path = os.path.join(EXTRACTED_FIELDS_DIR, f"{uploaded_file.name}_fields.txt")
            with open(field_path, "w", encoding="utf-8") as f:
                for k, v in fields.items():
                    f.write(f"{k}: {v}\n")

            st.success(f"Results saved to:\n📂 {RAW_TEXT_DIR}\n📂 {EXTRACTED_FIELDS_DIR}")
