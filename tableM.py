import os
import cv2
from ultralyticsplus import YOLO,render_result
import TableValues as tv 

# load model
model = YOLO('foduucom/table-detection-and-extraction')

# set model parameters
model.overrides['conf'] = 0.1  # NMS confidence threshold
model.overrides['iou'] = 0.3  # NMS IoU threshold
model.overrides['agnostic_nms'] = True  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image
def Table(image_path):
# set image
    
    image = cv2.imread(image_path)

    # perform inference
    results = model.predict(image_path)

    # create output folder if not exists
    output_folder = 'tables'
    os.makedirs(output_folder, exist_ok=True)

    # process each detected table
    for i, result in enumerate(results[0].boxes):
        # get bounding box coordinates (x1, y1, x2, y2)
        x1, y1, x2, y2 = result.xyxy[0].int().numpy()
        
        # crop the table from the image
        cropped_table = image[y1:y2, x1:x2]
        
        # save the cropped table
        output_path = os.path.join(output_folder, f'Table_{i+1}.jpg')
        
        cv2.imwrite(output_path, cropped_table)
        tv.values(output_path,f'Tables\Table_{i+1}.csv')

    print(f"{len(results[0].boxes)} tables saved to {output_folder} folder.")

# set image
image = 'temp_image.jpg'

# perform inference
results = model.predict(image)

# observe results
print(results[0].boxes)
render = render_result(model=model, image=image, result=results[0])
render.show()
