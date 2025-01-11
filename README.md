# Modilipi_Translator
AI-based Modi Lipi Translator is an AI-powered tool that translates Modi Lipi (an ancient script) into English. It supports image-to-text and text translation using machine learning models. Built with Python, TensorFlow, and Streamlit, it offers a user-friendly interface for seamless translations. Contributions are welcome!

Firstly you have to download tessaract ocr and setup in your device
To set up Tesseract OCR for your AI-based Modi Lipi Translator project, follow these steps:

Libraries:
Tesseract OCR: For extracting text from images.
Pillow: For image processing.
Pytesseract: Python wrapper for Tesseract OCR.
Installation & Setup:
1. Install Tesseract OCR:
Windows:

Download the installer from Tesseract OCR GitHub.
Run the installer and note the installation path (e.g., C:\Program Files\Tesseract-OCR).
Add Tesseract to your system's PATH environment variable:
Go to Control Panel > System and Security > System > Advanced system settings > Environment Variables.
In System Variables, find Path, click Edit, and add the Tesseract installation path (e.g., C:\Program Files\Tesseract-OCR).
Linux:

Run the following command:
bash
Copy code
sudo apt-get install tesseract-ocr
macOS:

Install using Homebrew:
bash
Copy code
brew install tesseract
2. Install Python Libraries:
In your project directory, create a requirements.txt file (if not already) with the following content:

Copy code
pytesseract
pillow
Then install the required libraries:

bash
Copy code
pip install -r requirements.txt
Alternatively, install them directly using:

bash
Copy code
pip install pytesseract pillow
3. Configure Pytesseract:
After installation, you need to configure the path for Tesseract in your code. Add the following configuration in your Python script (typically after importing pytesseract):

python
Copy code
import pytesseract
from PIL import Image

# Specify the Tesseract executable path (only needed on Windows if it's not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # For Windows

# Example of using Tesseract to extract text from an image
image = Image.open('your_image.png')  # Replace with your image path
extracted_text = pytesseract.image_to_string(image)

print(extracted_text)
4. Test the Setup:
Test the installation by running the above Python code. If Tesseract is correctly installed and configured, it will print the extracted text from the image.
Notes:
Ensure that the Tesseract executable path is correctly set, especially for Windows, where it may not be automatically recognized.
You can also specify the language for Tesseract (e.g., lang='eng' for English, or lang='mar' for Marathi, if supported).
With these steps, you should be ready to integrate Tesseract OCR into your project for text extraction from Modi Lipi images.
