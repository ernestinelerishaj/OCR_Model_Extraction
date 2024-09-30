import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import json

def convert_bbox_format(bbox, image_width, image_height):
    x_min, y_min = bbox[0]
    x_max, y_max = bbox[1]
    # Convert normalized coordinates to pixel coordinates
    return ((x_min * image_width, y_min * image_height),
            (x_max * image_width, y_max * image_height))

# Function to check if two boxes overlap
def boxes_overlap(box1, box2):
    # box1 and box2 are in the format ((x_min, y_min), (x_max, y_max))
    return not (box1[1][0] < box2[0][0] or  # Right of box1 is left of box2
                box1[0][0] > box2[1][0] or  # Left of box1 is right of box2
                box1[1][1] < box2[0][1] or  # Bottom of box1 is above box2
                box1[0][1] > box2[1][1])    # Top of box1 is below box2

def visualize_bounding_boxes(image_path, data):
    # Load the image
    image = Image.open(image_path)
    image_width, image_height = image.size

    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Iterate over lines
    for line in data["lines"]:
        for word in line["words"]:
            if "date" in word["value"].strip().lower() :
                try:
                    # Convert bounding box for the word "Peaceful"
                    bbox = convert_bbox_format(word["geometry"], image_width, image_height)
                    (x_min, y_min), (x_max, y_max) = bbox

                    # Draw the original bounding box
                    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                             linewidth=1, edgecolor='r', facecolor='none')
                    ax.add_patch(rect)
                    plt.text(x_min, y_min, word["value"], color='red', fontsize=12, weight='bold')

                    # Create two more boxes to the right of the original
                    width = x_max - x_min  # Width of the original bounding box
                    for i in range(1, 3):  # Two boxes to the right
                        new_x_min = x_min + i * width
                        new_x_max = x_max + i * width
                        right_rect = patches.Rectangle((new_x_min, y_min), width, y_max - y_min,
                                                       linewidth=1, edgecolor='g', facecolor='none')
                        ax.add_patch(right_rect)

                        # Check for overlapping words in the right boxes
                        for other_line in data["lines"]:
                            for other_word in other_line["words"]:
                                other_bbox = convert_bbox_format(other_word["geometry"], image_width, image_height)
                                if boxes_overlap(other_bbox, ((new_x_min, y_min), (new_x_max, y_max))):
                                    print(f"Word overlapping right box {i}: {other_word['value']}")

                    # Create two more boxes below the original
                    height = y_max - y_min  # Height of the original bounding box
                    for j in range(1, 3):  # Two boxes below
                        new_y_min = y_min + j * height
                        new_y_max = y_max + j * height
                        below_rect = patches.Rectangle((x_min, new_y_min), x_max - x_min + 30, height,
                                                       linewidth=1, edgecolor='b', facecolor='none')
                        ax.add_patch(below_rect)

                        # Check for overlapping words in the below boxes
                        for other_line in data["lines"]:
                            for other_word in other_line["words"]:
                                other_bbox = convert_bbox_format(other_word["geometry"], image_width, image_height)
                                if boxes_overlap(other_bbox, ((x_min, new_y_min), (x_max - x_min + 30, new_y_max))):
                                    print(f"Word found {j}: {other_word['value']}")

                except ValueError as e:
                    print(e)
    
    plt.show()

#load the data
with open("data.json") as f:
    data = json.load(f)["pages"][0]["blocks"][0]



# Provide the path to your image
image_path = 'document 4.png'
visualize_bounding_boxes(image_path, data)
