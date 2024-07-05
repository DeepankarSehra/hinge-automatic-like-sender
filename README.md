# Hinge Automation Project

This project automates the process of sending likes on Hinge. It scrolls through profiles, captures screenshots, detects facial landmarks, classifies profiles using a trained model, generates responses to prompts, and sends likes automatically.

## Features

- **Automated Scrolling and Screenshot Capturing:** The script scrolls through profiles and captures multiple screenshots, stitching them into a single long screenshot to create a complete profile page.
- **Profile Analysis:** It detects prompts and images on the profile.
- **Face Landmark Detection:** Uses MediaPipe's face mesh task to detect facial landmarks in profile images.
- **Profile Classification:** Classifies profiles into 'yes' or 'no' categories using a pre-trained random forest classifier.
- **Automated Responses:** Generates responses to prompts using the Gemini API based on the number of 'yes' classifications.
- **Automated Liking:** Sends likes automatically based on the generated responses.

## Requirements

- Python 3.x
- MediaPipe
- Gemini API
- OpenCV
- Scikit-learn
- Other dependencies as listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/hinge-automation.git
    cd hinge-automation
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Configure the Gemini API:**
    - Sign up for a Gemini API key and set it in your environment variables or in the script configuration.

2. **Train the Random Forest Classifier:**
    - Ensure you have a trained random forest classifier saved locally. If not, train it using your dataset and save the model.

3. **Run the Script:**
    ```sh
    python hinge_automation.py
    ```

4. **Automated Liking:**
    - The script will start scrolling through profiles, capturing screenshots, detecting facial landmarks, classifying profiles, generating responses, and sending likes automatically.

## File Structure

- `hinge_automation.py`: Main script for the automation process.
- `requirements.txt`: List of required Python packages.
- `README.md`: This file.
- `models/`: Directory to store the trained random forest classifier.
- `screenshots/`: Directory where the captured screenshots will be saved.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/fooBar`).
3. Commit your changes (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [MediaPipe](https://github.com/google/mediapipe)
- [OpenCV](https://opencv.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Gemini API](https://example.com/gemini-api)

## Disclaimer

This project is for educational purposes only. Use responsibly and ensure compliance with Hinge's terms of service.
