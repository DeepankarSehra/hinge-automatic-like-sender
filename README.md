# Hinge Automatic Like Sender

This project automates the process of sending likes on the dating app Hinge. It scrolls through profiles, detects facial landmarks, classifies profiles using a trained model, generates responses to prompts, and sends likes automatically.

## Features

- **Automated Scrolling and Screenshot Capturing:** The script scrolls through profiles and captures multiple screenshots, stitching them into a single long screenshot to create a complete profile page using ADB.
- **Profile Analysis:** It detects prompts and images on the profile.
- **Face Landmark Detection:** Uses MediaPipe's face mesh task to detect facial landmarks in profile images.
- **Profile Classification:** Classifies profiles into 'yes' or 'no' categories using a pre-trained Random Forest classifier.
- **Automated Responses:** Generates responses to prompts using the Gemini API based on the number of 'yes' classifications.
- **Automated Liking:** Sends likes automatically based on the generated responses.

## Requirements

- Python 3.x
- ADB
- MediaPipe
- Gemini API
- OpenCV
- Scikit-learn
- Joblib
- PIL
- Numpy
- Other dependencies as listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DeepankarSehra/hinge-automatic-like-sender.git
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r hinge-automatic-like-sender/requirements.txt
    ```

## Usage

1. **Configure the Gemini API:**
    - Sign up for a Gemini API key and set it in [prompt_gemini.py](prompt_gemini.py).

2. **Using a classifier:**
    - If you want to send likes based on your preferences then ensure you have a trained classifier job saved locally. If not, train it using your dataset and save the model. Use it in [profile_elements.py](profile_elements.py).
    - If not, then edit the ```main``` function in [after_extract.py](after_extract.py) to remove the if-else statement.

3. **Run the Script:**
    ```sh
    python /hinge-automatic-like-sender/final.py
    ```

4. **Automated Liking:**
    - The script will start scrolling through profiles, capturing screenshots, detecting facial landmarks, classifying profiles, generating responses, and sending likes automatically.
    - It also deletes the captured screenshots that are saved from your device simultaneously. All the saved data is cleaned up after [cleanup.py](cleanup.py) has run.

## File Structure

- `final.py`: Main script for the entire process.
- `requirements.txt`: List of required Python packages.
- `README.md`: This file.
- `random_forest_classifier.pkl`: Here is my personal preference trained random forest classifier.
- `screenshots/`: Directory where the captured screenshots will be saved temporarily.
- `cropped_text_boxes/`: Directory where the prompts will be saved as screenshots temporarily.
- `profile_elements/`: Directory where the images from the profile will be saved temporarily.
- `screenshot_separate.py` and `screenshot_joining.py`: Scripts to capture screenshots and make a long one of the entire profile.
- `prompt_gemini_rizzy.py`: Script that generates responses to the prompts.
- `prompt_finder.py`: Script that finds location of prompts and saves them as screenshots.
- `profile_elements.py`: Script that extracts all images of the profile.

## Disclaimer

This project is for educational purposes only. Use responsibly and ensure compliance with Hinge's terms of service.
