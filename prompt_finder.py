import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

large_image_path = 'screenshots/masti.png'
template_image_path = 'like_box.png'

large_image = cv2.imread(large_image_path)
template = cv2.imread(template_image_path)

large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

w, h = template_gray.shape[::-1]                                                                # used to detect the like squares exact coordinates

result = cv2.matchTemplate(large_image_gray, template_gray, cv2.TM_CCOEFF_NORMED)               # detects occurences of "template"

threshold = 0.8                                                                                 # sets a threshold for matching
loc = np.where(result >= threshold)

match_locations = []

for pt in zip(*loc[::-1]):                                                                      # gives locations for each like 
    match_locations.append(pt)

def non_max_suppression(boxes, overlapThresh):                                                  # function to perform non-maximum suppression
    if len(boxes) == 0:                                                                         # too much to comment
        return []                                                                               # treat as blackbox for "correctly" detecting the boxes

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

boxes = []
for pt in match_locations:                                                                      # prepare bounding boxes for non-maximum suppression
    x, y = pt
    boxes.append([x, y, x + w, y + h])

boxes = np.array(boxes)
picked_boxes = non_max_suppression(boxes, overlapThresh=0.3)

if len(picked_boxes) > 3:                                                                       # hard-coded error skipping if somehow more than 3 prompts are detected 
    print('extra detected')
    picked_boxes = picked_boxes[:3]

output_dir = 'cropped_text_boxes'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

text_boxes = []                                                                                 # draw rectangles around the matches and store the text box areas
for i, (x1, y1, x2, y2) in enumerate(picked_boxes):

    cv2.rectangle(large_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    text_box = (x1 - 900, y1 - 500, x2 + 20, y2 + 30)                                           # defined a box of dimensions 920 x 530 (winged it and it somehow works)
    text_boxes.append(text_box)

    cv2.rectangle(large_image, (text_box[0], text_box[1]), (text_box[2], text_box[3]), (255, 0, 0), 2)

    cropped_image = large_image[text_box[1]:text_box[3], text_box[0]:text_box[2]]

    cv2.imwrite(os.path.join(output_dir, f'cropped_text_box_{i}.png'), cropped_image)           # save the cropped prompt rectangle


# print("Heart icon locations (bounding boxes):")
# for box in picked_boxes:
#     print(f"Top-left: ({box[0]}, {box[1]}), Bottom-right: ({box[2]}, {box[3]})")

# print("\nText box areas:")
# for box in text_boxes:
#     print(f"Top-left: ({box[0]}, {box[1]}), Bottom-right: ({box[2]}, {box[3]})")
