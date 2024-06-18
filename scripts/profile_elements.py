import cv2
# import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import os

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    return img, gray, binary

def detect_and_save_images(binary, img):
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_count = 0
    # text_count = 0
    image_bboxes = []

    os.makedirs("profile_elements", exist_ok=True)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 100 and h > 100:
            # aspect_ratio = w / float(h)

            image_bboxes.append((x, y, w, h))
            image_roi = img[y:y + h, x:x + w]
            cv2.imwrite(f"profile_elements/element_{image_count}.png", image_roi)
            image_count += 1
    return image_bboxes

def remove_non_images():
    not_profile_img = []

    for item in os.listdir('profile_elements'):
        img = cv2.imread(os.path.join('profile_elements', item))
        if img.shape[0] >= 1000 and img.shape[1] >= 1000:
            continue
        else:
            not_profile_img.append(item)
        
    for item in not_profile_img:
        os.remove(os.path.join('profile_elements', item))


if __name__ == "__main__":
    image_path = "screenshots/masti.png"
    img, gray, binary = preprocess_image(image_path)
    image_bboxes = detect_and_save_images(binary, img)
    remove_non_images()