# 🧾 OCR Model Extraction – Intelligent Invoice & Document Text Recognition

This project focuses on extracting structured information from invoices and documents using OCR (Optical Character Recognition) techniques. It compares multiple OCR models such as **Doctr**, **EasyOCR**, **Tesseract**, and **PaddleOCR** to improve text extraction accuracy and layout understanding, specifically in complex domains like healthcare billing and insurance claims.

---

## 🚀 Key Features

- 📄 Extracts and classifies invoice fields (e.g., **Invoice Number**, **Date**, **Buyer GSTIN**, **Supplier GSTIN**, etc.)
- 🔍 Uses **Doctr** for structured data extraction and JSON outputs
- 🔁 Model comparison for OCR performance across diverse formats
- 🧠 Context-aware logic for field mapping using Python
- ✅ Verification module to validate the output against input data

---

## 🧰 Tech Stack

- Python
- EasyOCR
- Doctr (by Mindee)
- PaddleOCR
- Tesseract
- Streamlit (for optional web deployment)
- OpenCV, NumPy, Regex

---

## 🧠 Project Overview

The goal of this project is to **automate document and invoice analysis** using a combination of OCR engines and logic-based field extractors. This is particularly useful in:

- **Healthcare billing**
- **Insurance claims**
- **GST-based invoice validation**

Each model is benchmarked for its ability to extract structured data from noisy or complex documents.

---

## 🖼️ Sample Input/Output

_Example invoice image → JSON output_

```json
{
  "Invoice Number": "INV2024-001",
  "Date": "2024-08-10",
  "Buyer GSTIN": "33AAAAA0000A1Z5",
  "Supplier GSTIN": "29BBBBB1111B2Z6",
  "Total Amount": "₹12,000.00"
}

