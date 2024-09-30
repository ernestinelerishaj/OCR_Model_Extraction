from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json 

model = ocr_predictor(pretrained=True)
def ReadImage(filename):
    single_img_doc = DocumentFile.from_images(filename)
    # Analyze
    result = model(single_img_doc)
    json_output = result.export()
    with open("data.json","w") as f: 
        json.dump(json_output, f)
        