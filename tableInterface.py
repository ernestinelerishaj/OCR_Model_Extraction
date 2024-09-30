import tableM as t 
import os 

def Instance(path):
    t.Table(path)
path="temp_image.jpg"
Instance(path)
if os.path.exists(path):
    os.remove(path)
    
else:
    print("Temporary image file could not be found for deletion.")
