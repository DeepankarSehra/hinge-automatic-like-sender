import pytesseract
import os
import numpy as np
import cv2 

def extract_text_from_regions(img):
    tt = pytesseract.image_to_string(img, config='--psm 6')
    return tt

 
if __name__ == '__main__':
    image_path = 'cropped_text_boxes'
    image_text = []
    for img in os.listdir(image_path):
        extracted_text = extract_text_from_regions(os.path.join(image_path,img))
        image_text.append(extracted_text)

print(image_text[2])