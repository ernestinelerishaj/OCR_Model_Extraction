**Invoice Data Extraction App**

This Streamlit application extracts and validates data from an invoice image. Users can manually enter invoice details such as Invoice Number, Date, Supplier, Buyer, and Amount, and upload an image of the invoice. The application will extract and validate the fields from the image using Optical Character Recognition (OCR) and compare the extracted data with user inputs.

**Features**

Manual Input: Users can input the invoice number, date, supplier, buyer, amount, supplier state, and buyer state.

Image Upload: Upload an image of an invoice for processing.

Field Validation: The app checks if the manually inputted invoice fields match the data extracted from the invoice image.

OCR Processing: Utilizes the doctrModels and LineChecker modules to extract and verify text from the uploaded invoice image.

**How It Works**

Input Fields: The user enters information such as Invoice Number, Date, Supplier, Buyer, Amount, Supplier State, and Buyer State.

Image Upload: The user uploads an image of the invoice.

Data Validation: Once all fields are entered and the image is uploaded, clicking "Process" extracts data from the invoice image, and the app checks if it matches the manually inputted data.

Word Pooling: The app uses multiple variants of common invoice fields (e.g., "Invoice Number," "Inv #") to improve the accuracy of the validation process.

**Prerequisites**

To run this project, you need to have Python and Streamlit installed.

**Code Breakdown**

invoice.py: This is the main file containing the Streamlit interface and logic.

Fields for manually entering invoice data (Invoice Number, Date, Supplier, Buyer, Amount, etc.).

An image uploader for uploading an invoice image.

A processing function that extracts text from the image using doctrModels and LineChecker, and matches the text with user inputs.

A word-pooling system for matching variants of invoice fields like "Invoice Number" and "Total Amount."

**Modules:**

doctrModels: Used for handling OCR (Optical Character Recognition) from the uploaded invoice image.

LineChecker: Used to validate and extract specific lines from the image text.

**Helper Function:**

check_for_variants(file_path, variants_list, data): This function checks if any variant of the manually entered data matches the extracted text from the image file. It performs number extraction and comparison for numeric fields like Invoice Number and Amount.

**Important Notes**

The application relies on the clarity of the uploaded invoice image. Poor image quality may lead to inaccurate OCR results.

The file temp_image.jpg is used as a temporary file to store the uploaded image for processing.
