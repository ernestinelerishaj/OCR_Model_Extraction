import streamlit as st
import doctrModels as dm
import LineChecker as lc
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

import os
import re 

st.header("Input")
st.write("{")

# Input fields
no = st.text_input("Invoice Number:")
date = st.text_input("Invoice date:") 
supp= st.text_input("Supplier:")
buyer=st.text_input("Buyer:")
amt= str(st.number_input("Amount:"))
if amt.endswith(".0"):
    amt=amt[:-2]
supplier_state= st.text_input("Supplier State:")
buyer_state= st.text_input("Buyer State:")
pic = st.file_uploader("Image")

st.write("}")
process=False

if no and date and supp and buyer and amt:
    no=no.replace(" ", "")
    date=date.replace(" ", "").replace(",", "")
    supp=supp.replace(" ", "")
    buyer=buyer.replace(" ", "")
    amt=amt.replace(" ", "")
    process=True 

if st.button("Process") and pic and process:
    # Save the uploaded file temporarily
    temp_file_path = "temp_image.jpg"  # You can give it any name with the correct extension
    
    # Write the uploaded image to a temporary file
    with open(temp_file_path, "wb") as f:
        f.write(pic.getbuffer())

    # Process the image using the file path
    dm.ReadImage(temp_file_path)
   #Word pooling 
    invoice_number_variants = ["invoice number", "inv", "inv-no", "invoice no", "inv number", "inv #", "invoice #"]
    date_variants = ["date", "invoice date", "bill date", "inv date", "issued on", "invoice issued", "date of issue", "date issued"]
    buyer_variants = ["buyer", "bill to", "billed to", "customer", "client", "to", "purchaser", "buyer details", "buying party","consignee"]
    supplier_variants = ["supplier", "from", "vendor", "seller", "company", "supplier details", "issued by", "provider", "from company"]
    amount_variants = ["amount", "invoice amount", "total", "total amount", "inv amount", "total due", "amount payable", "amount paid", "total payable", "total inv amount"]
    st.write(lc.LineWords(temp_file_path, "number"))
    # Helper function to check if any variant is in the document
    def check_for_variants(file_path, variants_list,data):
        for variant in variants_list:
            
            if data.strip().lower().isdigit():
                st.write(lc.LineWords(file_path, variant))
                numbers = re.findall(r'\d+\.\d+|\d+', lc.LineWords(file_path, variant))
                # Convert extracted numbers into floats
                if float(data.strip().lower()) in [float(num) for num in numbers]:
                    return True
            elif data.strip().lower() in lc.LineWords(file_path, variant):
                
                return True
        return False

    # Now use the helper function to check for variants
    no = check_for_variants(temp_file_path, invoice_number_variants,no)
    date = check_for_variants(temp_file_path, date_variants,date)
    buyer = check_for_variants(temp_file_path, buyer_variants,buyer)
    supp = check_for_variants(temp_file_path, supplier_variants,supp)
    amt = check_for_variants(temp_file_path, amount_variants,amt)
    supplier_state = check_for_variants(temp_file_path, amount_variants,supplier_state)
    buyer_state=check_for_variants(temp_file_path, amount_variants,buyer_state)

    st.write({
             'invoice_number': f'{no}',
             'invoice_date': f'{date}',
             'supp':f'{supp}',
             'buyer':f'{buyer}',
             'amount':f'{amt}',
             'supplier_state':f'{supplier_state}',
             'buyer_state':f'{buyer_state}',
             })
