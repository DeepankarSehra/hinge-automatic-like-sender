import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# Load the images
large_image_path = 'screenshots/masti.png'
template_image_path = 'scripts/like_box.png'

large_image = cv2.imread(large_image_path)
template = cv2.imread(template_image_path)

# Convert images to grayscale
large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get the dimensions of the template
w, h = template_gray.shape[::-1]

# Perform template matching
result = cv2.matchTemplate(large_image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# Set a threshold for matching
threshold = 0.8
loc = np.where(result >= threshold)

# Create a list to store the match locations
match_locations = []

for pt in zip(*loc[::-1]):
    match_locations.append(pt)

# Function to perform non-maximum suppression
def non_max_suppression(boxes, overlapThresh):
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []

    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")

# Prepare bounding boxes for non-maximum suppression
boxes = []
for pt in match_locations:
    x, y = pt
    boxes.append([x, y, x + w, y + h])

boxes = np.array(boxes)
picked_boxes = non_max_suppression(boxes, overlapThresh=0.3)

# Create a directory to save cropped text box images
output_dir = 'cropped_text_boxes'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Draw rectangles around the matches and store the text box areas
text_boxes = []
for i, (x1, y1, x2, y2) in enumerate(picked_boxes):
    # Draw rectangle around each match
    cv2.rectangle(large_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Define a bounding box that likely contains the text area (adjust as needed)
    text_box = (x1 - 900, y1 - 500, x2 + 20, y2 + 30)
    text_boxes.append(text_box)
    # Draw rectangle around the text area
    cv2.rectangle(large_image, (text_box[0], text_box[1]), (text_box[2], text_box[3]), (255, 0, 0), 2)
    # Crop the text box area from the large image
    cropped_image = large_image[text_box[1]:text_box[3], text_box[0]:text_box[2]]
    # Save the cropped image
    cv2.imwrite(os.path.join(output_dir, f'cropped_text_box_{i}.png'), cropped_image)

# Show the result
# plt.figure(figsize=(10, 10))
# plt.imshow(cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB))
# plt.title('Detected Template Matches and Text Areas')
# plt.show()

# Print the locations of the heart icons and text boxes
print("Heart icon locations (bounding boxes):")
for box in picked_boxes:
    print(f"Top-left: ({box[0]}, {box[1]}), Bottom-right: ({box[2]}, {box[3]})")

print("\nText box areas:")
for box in text_boxes:
    print(f"Top-left: ({box[0]}, {box[1]}), Bottom-right: ({box[2]}, {box[3]})")
