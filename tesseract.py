import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import os

def preprocess_image(image_path):
    """
    Load and preprocess the image for contour detection.
    
    :param image_path: Path to the image file
    :return: Grayscale image, binary image
    """
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to binarize the image
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    return img, gray, binary

def detect_and_save_images(binary, img):
    """
    Detect images in the binary image and save them separately.

    :param binary: Binary image for contour detection
    :param img: Original image for extracting the detected regions
    :return: List of bounding boxes of detected images
    """
    # Use morphological operations to remove small noise
    kernel = np.ones((5,5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_count = 0
    image_bboxes = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Assuming images are larger blocks, you can filter out smaller contours
        if w > 100 and h > 100:
            image_bboxes.append((x, y, w, h))
            image_roi = img[y:y+h, x:x+w]
            cv2.imwrite(f"image_{image_count}.png", image_roi)
            image_count += 1
    
    return image_bboxes

def extract_text_from_regions(img, image_bboxes):
    """
    Extract text from the regions not containing images.

    :param img: Original image
    :param image_bboxes: List of bounding boxes of detected images
    :return: Extracted text
    """
    mask = np.ones(img.shape[:2], dtype="uint8") * 255

    for (x, y, w, h) in image_bboxes:
        cv2.rectangle(mask, (x, y), (x+w, y+h), 0, -1)

    # Invert mask
    mask_inv = cv2.bitwise_not(mask)
    text_regions = cv2.bitwise_and(img, img, mask=mask_inv)

    # Convert the text regions to RGB
    text_regions_rgb = cv2.cvtColor(text_regions, cv2.COLOR_BGR2RGB)

    # Perform OCR on the text regions
    text = pytesseract.image_to_string(text_regions_rgb, config='--psm 6')

    return text

if __name__ == "__main__":

    # folder_path = "myprofile/"
    # for file in os.listdir(folder_path):
    #     image_path = folder_path + file

    image_path = "hinge.jpeg"
    img, gray, binary = preprocess_image(image_path)
    image_bboxes = detect_and_save_images(binary, img)
    extracted_text = extract_text_from_regions(img, image_bboxes)
    print("Extracted Text:\n", extracted_text)

    # Display the original image with bounding boxes for verification
    for (x, y, w, h) in image_bboxes:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
