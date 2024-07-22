import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings("ignore")
import mediapipe as mp


# Extracts all the images from the profile using the long screenshot

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


def remove_non_images():                                                                        # removes smaller cropped pieces of the long screenshot that are not images
    not_profile_img = []                                            

    for item in os.listdir('profile_elements'):
        img = cv2.imread(os.path.join('profile_elements', item))
        if img.shape[0] >= 1000 and img.shape[1] >= 1000:                                       # somewhat hard-coded but will mostly always work 
            continue
        else:
            not_profile_img.append(item)
        
    for item in not_profile_img:
        os.remove(os.path.join('profile_elements', item))

    return None


def extract_landmarks(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark])
            return landmarks.flatten()
    return None


def classify_image(classifier, image_path):
    landmarks = extract_landmarks(image_path)
    if landmarks is not None:
        landmarks = landmarks.reshape(1,-1)
        prediction = classifier.predict(landmarks)
        return prediction
    return None



image_path = "screenshots/masti.png"
img, gray, binary = preprocess_image(image_path)
image_bboxes = detect_and_save_images(binary, img)
remove_non_images()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

clf = joblib.load('random_forest_classifier.pkl')
img_folder = 'profile_elements/'

count = 0
for image in os.listdir(img_folder):
    print(image, classify_image(clf, os.path.join(img_folder, image)))
    if classify_image(clf, os.path.join(img_folder, image)) == [1]:
        count += 1

    

    
