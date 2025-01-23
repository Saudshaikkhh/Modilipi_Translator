# AI-based Modi Lipi Translator

AI-based Modi Lipi Translator is an AI-powered tool designed to translate Modi Lipi (an ancient script) into English. This tool leverages machine learning models for both image-to-text and text translation. It provides a user-friendly interface built with Python, TensorFlow, and Streamlit for seamless translation operations.

## Overview

The AI-based Modi Lipi Translator is an innovative tool that helps in translating text from the Modi Lipi script, a historical Indian script used in the region of Maharashtra. The project uses advanced OCR (Optical Character Recognition) technology to extract text from images containing Modi Lipi and then translates the extracted text into English. 

The project is powered by:
- **Python**
- **TensorFlow**
- **Streamlit**
- **Tesseract OCR** (for text extraction)

Contributions to the project are welcome!

## Features
- **Image-to-Text Translation**: Extract text from images containing Modi Lipi and translate it into English.
- **Text Translation**: Input Modi Lipi text for direct translation to English.
- **User-Friendly Interface**: Streamlit provides a simple interface for interacting with the translator.

## Setup Instructions

### Step 1: Install Tesseract OCR

To extract text from images, Tesseract OCR is required. Follow the steps below to install Tesseract OCR on your device:

#### Windows:
1. Download the Tesseract installer from [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract).
2. Run the installer and note the installation path (e.g., `C:\Program Files\Tesseract-OCR`).
3. Add Tesseract to your system’s PATH:
   - Go to **Control Panel > System and Security > System > Advanced system settings > Environment Variables**.
   - Under **System Variables**, find **Path**, click **Edit**, and add the Tesseract installation path (e.g., `C:\Program Files\Tesseract-OCR`).

#### Linux:
```bash
sudo apt-get install tesseract-ocr
```
## macOS:
Install using Homebrew:
```bash
brew install tesseract
```
## Step 2: Install Required Python Libraries
Create a requirements.txt file in your project directory (if not already created) and add the following content:
```bash
pytesseract
pillow
```
Then, install the required libraries by running the following command:
```bash
pip install -r requirements.txt
```
Alternatively, you can install them directly using:
```bash
pip install pytesseract pillow
```
## Step 3: Configure Pytesseract
After installing Tesseract and Python libraries, configure Tesseract in your code. Add the following configuration in your Python script:
```python
import pytesseract
from PIL import Image
# Specify the Tesseract executable path (only needed on Windows if it's not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # For Windows
```
## Running the Application
Clone this repository or download the project files to your local system.
Navigate to the project directory.
Launch the Streamlit app by running:
```bash
streamlit run app.py
```
Open your web browser and go to `http://localhost:8501` to use the translator.

## File Structure
The project directory is organized as follows:

```php
.
├── app.py                   # Main application script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── models/                  # Pre-trained models for translation (if applicable)
├── data/                    # Sample datasets for testing
├── static/                  # Static files (e.g., images, CSS, etc.)
└── templates/               # HTML templates (if any)
```
## Contributing
Contributions are welcome! If you have suggestions or want to report issues, feel free to open a pull request or raise an issue in the repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Tesseract OCR
- Streamlit Documentation
- TensorFlow and Pillow for their excellent libraries
- Special thanks to the developers of Modi Lipi datasets and resources.
```arduino
This expanded README file includes detailed setup instructions, features, and a project overview, ensuring clarity for users and contributors.
```