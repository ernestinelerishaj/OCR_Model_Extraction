import doctrModels as dm
import LineChecker as lc
import os
import re
from pdf2image import convert_from_path

# Function to process the file path and perform the desired operations
def process_invoice(file_path, no, date, supp, buyer, amt, supplier_state, buyer_state):
    process = False

    # Check if all inputs are present
    if no and date and supp and buyer and amt:
        no = no.replace(" ", "")
        date = date.replace(" ", "").replace(",", "")
        supp = supp.replace(" ", "")
        buyer = buyer.replace(" ", "")
        amt = amt.replace(" ", "")
        process = True
    
    # If all fields are valid and process is True
    if process:
        temp_file_path = None

        # Check if the file is a PDF
        if file_path.lower().endswith(".pdf"):
            # Convert the PDF into images
            images = convert_from_path(file_path)
            if images:
                # Save the first page as an image (for simplicity, only processing the first page)
                temp_file_path = "temp_page_image.jpg"
                images[0].save(temp_file_path, "JPEG")
        else:
            # Assuming the file is an image
            temp_file_path = file_path

        if temp_file_path:
            # Process the image using doctrModels
            dm.ReadImage(temp_file_path)

            # Word pooling variants
            invoice_number_variants = ["invoice number", "inv", "inv-no", "invoice no", "inv number", "inv #", "invoice #"]
            date_variants = ["date", "invoice date", "bill date", "inv date", "issued on", "invoice issued", "date of issue", "date issued"]
            buyer_variants = ["buyer", "bill to", "billed to", "customer", "client", "to", "purchaser", "buyer details", "buying party", "consignee"]
            supplier_variants = ["supplier", "from", "vendor", "seller", "company", "supplier details", "issued by", "provider", "from company","shipper"]
            amount_variants = ["amount", "invoice amount", "total", "total amount", "inv amount", "total due", "amount payable", "amount paid", "total payable", "total inv amount"]

            # Helper function to check for variants in the image text
            def check_for_variants(file_path, variants_list, data):
                for variant in variants_list:
                    if data.strip().lower().isdigit():
                        text_in_file = lc.LineWords(file_path, variant)
                        numbers = re.findall(r'\d+\.\d+|\d+', text_in_file)
                        if float(data.strip().lower()) in [float(num) for num in numbers]:
                            return True
                    elif data.strip().lower() in lc.LineWords(file_path, variant).lower():
                        return True
                return False

            # Check for invoice details in the document
            no = check_for_variants(temp_file_path, invoice_number_variants, no)
            date = check_for_variants(temp_file_path, date_variants, date)
            buyer = check_for_variants(temp_file_path, buyer_variants, buyer)
            supp = check_for_variants(temp_file_path, supplier_variants, supp)
            amt = check_for_variants(temp_file_path, amount_variants, amt)
            supplier_state = check_for_variants(temp_file_path, amount_variants, supplier_state)
            buyer_state = check_for_variants(temp_file_path, amount_variants, buyer_state)

            # Display results
            result = {
                'invoice_number': f'{no}',
                'invoice_date': f'{date}',
                'supp': f'{supp}',
                'buyer': f'{buyer}',
                'amount': f'{amt}',
                'supplier_state': f'{supplier_state}',
                'buyer_state': f'{buyer_state}',
            }
            print(result)
        else:
            print("Error processing file.")
    else:
        print("Missing or invalid inputs.")


# Example of calling the function with file path and input values
file_path = "RLL159254 BL.pdf"  # Replace with the actual file path
invoice_number = "12345"
invoice_date = "2023-09-01"
supplier = "Supplier Name"
buyer = "Buyer Name"
amount = "4,629.00"
supplier_state = "State1"
buyer_state = "State2"

process_invoice(file_path, invoice_number, invoice_date, supplier, buyer, amount, supplier_state, buyer_state)
