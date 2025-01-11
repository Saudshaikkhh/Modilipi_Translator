import streamlit as st
import pandas as pd
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from PIL import Image
import cv2
import numpy as np
import pytesseract
import time
from datetime import datetime

# Set page config at the very beginning
st.set_page_config(page_title="Modi Lipi Translator", page_icon="🖋️", layout="wide")

# Load pre-trained MarianMT models and tokenizers
@st.cache_resource
def load_models():
    en_mr_model_name = 'facebook/m2m100_418M'
    en_mr_tokenizer = M2M100Tokenizer.from_pretrained(en_mr_model_name)
    en_mr_model = M2M100ForConditionalGeneration.from_pretrained(en_mr_model_name)

    mr_en_model_name = 'facebook/m2m100_418M'
    mr_en_tokenizer = M2M100Tokenizer.from_pretrained(mr_en_model_name)
    mr_en_model = M2M100ForConditionalGeneration.from_pretrained(mr_en_model_name)

    return en_mr_tokenizer, en_mr_model, mr_en_tokenizer, mr_en_model

en_mr_tokenizer, en_mr_model, mr_en_tokenizer, mr_en_model = load_models()

# Character mappings (abbreviated for brevity)
devanagari_to_modilipi = {
    # Vowels
    'अ': '𑘀', 'आ': '𑘁', 'इ': '𑘂', 'ई': '𑘃', 'उ': '𑘄', 'ऊ': '𑘅',
    'ऋ': '𑘆', 'ॠ': '𑘇', 'ऌ': '𑘈', 'ॡ': '𑘉', 'ए': '𑘊', 'ऐ': '𑘋',
    'ओ': '𑘌', 'औ': '𑘍',

    # Vowel Signs
    'ा': '𑘰', 'ि': '𑘱', 'ी': '𑘲', 'ु': '𑘳', 'ू': '𑘴', 'ृ': '𑘵',
    'ॄ': '𑘶', 'ॢ': '𑘷', 'ॣ': '𑘸', 'े': '𑘹', 'ै': '𑘺', 'ो': '𑘻',
    'ौ': '𑘼',

    # Consonants
    'क': '𑘎', 'ख': '𑘏', 'ग': '𑘐', 'घ': '𑘑', 'ङ': '𑘒',
    'च': '𑘓', 'छ': '𑘔', 'ज': '𑘕', 'झ': '𑘖', 'ञ': '𑘗',
    'ट': '𑘘', 'ठ': '𑘙', 'ड': '𑘚', 'ढ': '𑘛', 'ण': '𑘜',
    'त': '𑘝', 'थ': '𑘞', 'द': '𑘟', 'ध': '𑘠', 'न': '𑘡',
    'प': '𑘢', 'फ': '𑘣', 'ब': '𑘤', 'भ': '𑘥', 'म': '𑘦',
    'य': '𑘧', 'र': '𑘨', 'ल': '𑘩', 'व': '𑘪',
    'श': '𑘫', 'ष': '𑘬', 'स': '𑘭', 'ह': '𑘮',

    # Special Characters
    'ं': '𑘽',  # Anusvara
    'ः': '𑘾',  # Visarga
    'ँ': '𑙀',  # Chandrabindu
    '्': '𑘿',  # Virama

    # Numbers
    '०': '𑙐', '१': '𑙑', '२': '𑙒', '३': '𑙓', '४': '𑙔',
    '५': '𑙕', '६': '𑙖', '७': '𑙗', '८': '𑙘', '९': '𑙙'
}

modilipi_to_devanagari = {v: k for k, v in devanagari_to_modilipi.items()}

# Helper functions
def translate_to_marathi(texts):
    if not texts:
        return []
    if isinstance(texts, str):
        texts = [texts]
    en_mr_tokenizer.src_lang = "en"
    inputs = en_mr_tokenizer(texts, return_tensors="pt", padding=True)
    translated = en_mr_model.generate(**inputs, forced_bos_token_id=en_mr_tokenizer.get_lang_id("mr"))
    translated_texts = en_mr_tokenizer.batch_decode(translated, skip_special_tokens=True)
    return translated_texts

def convert_to_modilipi(text):
    return ''.join([devanagari_to_modilipi.get(char, char) for char in text])

def translate_to_modilipi(english_text):
    marathi_texts = translate_to_marathi(english_text)
    cleaned_marathi_texts = [marathi.replace('@ action', '').strip() for marathi in marathi_texts]
    modilipi_translations = [convert_to_modilipi(marathi) for marathi in cleaned_marathi_texts]
    return modilipi_translations

def process_image(image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ocr_result = pytesseract.image_to_string(gray, lang='modi')
    return ocr_result

def modilipi_to_devanagari_text(text):
    return ''.join([modilipi_to_devanagari.get(char, char) for char in text])

def translate_marathi_to_english(marathi_text):
    mr_en_tokenizer.src_lang = "mr"
    inputs = mr_en_tokenizer([marathi_text], return_tensors="pt", padding=True)
    translated = mr_en_model.generate(**inputs, forced_bos_token_id=mr_en_tokenizer.get_lang_id("en"))
    translated_text = mr_en_tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return translated_text

def init_session_state():
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    if 'total_translations' not in st.session_state:
        st.session_state.total_translations = 0
    if 'translation_history' not in st.session_state:
        st.session_state.translation_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'


init_session_state()



st.title("🖋️ Modi Lipi Translator")

st.sidebar.header("Instructions")
with st.sidebar.expander("How to use"):
    st.write("""
    1. Choose a translation direction using the tabs.
    2. For English to Modi Lipi:
       - Enter your English text in the left text area.
       - Click 'Translate' to see the Modi Lipi translation in the right text area.
       - Explore the character mapping and translation process details.
    3. For Modi Lipi to English:
       - Upload an image containing Modi Lipi text.
       - The image will appear on the left side.
       - The translation process and results will appear on the right side.
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["Translate Text", "Translate File", "Feedback & Support"])

with tab1:
    st.header("Translate Text")
    
    col1, col2 = st.columns(2)
    
    with col1:
        english_input = st.text_area("Enter English Text:", height=200, key="english_input")
    
    with col2:
        modilipi_output = st.empty()
        modilipi_output.text_area("Modi Lipi Translation:", height=200, key="modilipi_translation")

    translate_button = st.button("Translate", key="translate_button")
    
    if translate_button and english_input:
        with st.spinner("Translating..."):
            marathi_translation = translate_to_marathi(english_input)[0]
            modilipi_translation = translate_to_modilipi(english_input)[0]
            time.sleep(1)  # Simulating processing time
        
        st.success("Translation complete!")
        modilipi_output.text_area("Modi Lipi Translation:", value=modilipi_translation, height=200, key="modilipi_translation_updated")
        
        with st.expander("Translation Process Details"):
            st.write("1. English to Marathi Translation:")
            st.code(marathi_translation)
            st.write("2. Marathi to Modi Lipi Conversion:")
            st.code(modilipi_translation)
        
        with st.expander("Character Mapping"):
            df = pd.DataFrame(list(devanagari_to_modilipi.items()), columns=['Devanagari', 'Modi Lipi'])
            st.dataframe(df)
    
    elif translate_button:
        st.warning("Please enter some text to translate.")

    st.markdown("---")
    st.subheader("Interactive Character Explorer")
    selected_char = st.selectbox("Select a Devanagari character:", list(devanagari_to_modilipi.keys()))
    if selected_char:
        st.write(f"Devanagari: {selected_char}")
        st.write(f"Modi Lipi: {devanagari_to_modilipi[selected_char]}")

with tab2:
    st.header("Translate File")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Image with Modi Lipi Text", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

    with col2:
        if uploaded_file is not None:
            with st.spinner("Processing image..."):
                ocr_result = process_image(image)
                time.sleep(1)  # Simulating processing time

            if not ocr_result.strip():
                st.warning("No text found in the image.")
            else:
                devanagari_text = modilipi_to_devanagari_text(ocr_result)
                
                if not devanagari_text.strip():
                    st.warning("No valid Devanagari text found.")
                else:
                    with st.spinner("Translating to English..."):
                        english_translation = translate_marathi_to_english(devanagari_text)
                        time.sleep(1)  # Simulating processing time
                    
                    st.success("Translation complete!")
                    
                    with st.expander("Modi Lipi (Detected)", expanded=True):
                        st.text_area("", value=ocr_result, height=100, key="modilipi_detected")
                    
                    with st.expander("Devanagari", expanded=True):
                        st.text_area("", value=devanagari_text, height=100, key="devanagari_text")
                    
                    with st.expander("English Translation", expanded=True):
                        st.text_area("", value=english_translation, height=100, key="english_translation")
                    
                    with st.expander("Translation Process"):
                        st.write("1. Image Upload and OCR")
                        st.write("2. Modi Lipi to Devanagari Conversion")
                        st.write("3. Devanagari to English Translation")
                        
                        st.progress(100)

with tab3:
    st.header("Feedback & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rate Your Experience")
        satisfaction = st.slider("How satisfied are you with the translator?", 1, 5, 3)
        
        feedback_type = st.selectbox(
            "What type of feedback do you have?",
            ["General Feedback", "Bug Report", "Feature Request", "Accuracy Issue"]
        )
        
        feedback_text = st.text_area("Tell us more about your experience:")
        
        if st.button("Submit Feedback"):
            if feedback_text:
                st.session_state.feedback_submitted = True
                st.success("Thank you for your valuable feedback!")
                # Here you can implement functionality to save or process the feedback.
            else:
                st.warning("Please enter some feedback before submitting.")
    
    with col2:
        st.subheader("Frequently Asked Questions")
        faqs = {
            "How accurate is the translation?": "Our model strives for accuracy but may not be perfect for complex texts.",
            "Can I use this for commercial purposes?": "Yes, with proper attribution. Check our terms of service.",
            "How can I improve translation quality?": "Try shorter phrases and check our translation tips.",
            "Is my data safe?": "We do not store your translations permanently. All data is processed securely."
        }
        
        for question, answer in faqs.items():
            with st.expander(question):
                st.write(answer)
                        
# Footer
st.markdown("---")
st.markdown("© 2024 AI-based Modi Lipi Translator. All rights reserved.\n\n" 
            "This work is protected by copyright law and may not be reproduced,\n"
            "distributed, or used in any form without prior written permission.\n\n"
            "Unauthorized use of this work may result in legal action.")
# Add a fun fact about Modi Lipi
facts = [
    "Modi Lipi originated in the 12th century and is primarily used for writing Marathi.",
    "It was developed by the Maharashtrian community to simplify the writing of Marathi, making it more efficient than Devanagari.",
    "Modi Lipi was widely used in Maharashtra for official and literary purposes until the 20th century.",
    "Modi is an abugida, meaning each character represents a consonant with an inherent vowel.",
    "Modi Lipi uses diacritical marks to indicate vowel sounds, which can change the inherent vowel of consonants.",
    "The script was used extensively in administrative documents, legal papers, and personal correspondence.",
    "With the rise of Devanagari in the 20th century, the use of Modi Lipi declined significantly.",
    "In recent years, there have been efforts to revive Modi Lipi and promote its usage in education and literature.",
    "Today, Modi Lipi is taught in some schools and is included in the curriculum of Maharashtra.",
    "The script has several unique characters and ligatures that are not present in Devanagari.",
    "Modi Lipi has a distinct style of calligraphy, known for its fluid and cursive writing.",
    "The script is known for its cursive nature, making it faster to write compared to other scripts.",
    "Many historical texts and literary works in Marathi were written in Modi Lipi.",
    "Numerous manuscripts from the medieval period are preserved in Modi Lipi, providing insights into the language and culture of that era.",
    "Modi Lipi has influenced other scripts and writing systems used in neighboring regions.",
    "The script was designed to be written continuously without lifting the pen, which contributed to its speed.",
    "Modi Lipi was the official script of the Maratha Empire for administrative purposes.",
    "The script evolved over time, with variations in the shape of characters seen in different periods.",
    "Several handwritten documents from the Peshwa era are in Modi Lipi, providing valuable historical information.",
    "Modi Lipi was used alongside Devanagari for many centuries in Maharashtra.",
    "Unlike Devanagari, Modi Lipi has fewer horizontal lines connecting characters, which makes it distinct.",
    "The script was gradually replaced by Devanagari in official use after the British colonial period.",
    "Modi Lipi has its own numerals, distinct from Devanagari and other Indian scripts.",
    "Efforts are underway to digitize Modi Lipi texts and manuscripts for preservation.",
    "There are online resources and apps that help users learn and practice Modi Lipi.",
    "Inscriptions in Modi Lipi can still be found on ancient temples, monuments, and forts in Maharashtra.",
    "Modi Lipi was extensively used in the Peshwa courts for administrative work.",
    "Researchers and historians use Modi Lipi to study medieval Marathi texts.",
    "The script was not just confined to Maharashtra; it was also used in parts of Karnataka, Gujarat, and Madhya Pradesh.",
    "Modi Lipi is written from left to right, like most Indian scripts.",
    "In its heyday, the script was also used for poetry, literature, and religious texts.",
    "The British introduced typewriters with Modi Lipi keys for official use in India.",
    "Modi Lipi underwent several changes during its usage under different rulers.",
    "The Maratha Empire's extensive communication networks were maintained in Modi Lipi.",
    "Learning Modi Lipi requires understanding its distinct consonant and vowel combinations.",
    "Efforts to revive Modi Lipi include workshops, exhibitions, and publications.",
    "The script is still used in certain rural areas for personal correspondence.",
    "Modi Lipi has a simpler structure compared to Devanagari, making it easier to learn for some users.",
    "Several historical archives in India store Modi Lipi documents, which are being digitized.",
    "In modern times, Modi Lipi has been featured in art and design projects.",
    "Linguists study Modi Lipi to understand the evolution of the Marathi language.",
    "Modi Lipi's cursive style allowed scribes to write documents faster than using Devanagari.",
    "Some linguists believe that Modi Lipi could be adapted for digital communication.",
    "Several online tools are available to convert Devanagari text into Modi Lipi.",
    "The decline of Modi Lipi is often attributed to British educational reforms favoring Devanagari.",
    "Modi Lipi characters have variations that depend on the region and time period of use.",
    "Many old family documents in Maharashtra are still preserved in Modi Lipi.",
    "Modi Lipi's unique ligatures make it challenging to convert into modern scripts.",
    "There are only a limited number of experts who can fluently read Modi Lipi manuscripts.",
    "Modi Lipi's cursive nature made it more popular for administrative purposes than literary works.",
    "Various calligraphy styles of Modi Lipi evolved based on the scribe's region.",
    "Modi Lipi is considered a cultural treasure of Maharashtra.",
    "The script's name, 'Modi,' is believed to come from the word 'mod,' meaning 'to break' or 'to fold.'",
    "Modi Lipi was primarily used in royal and courtly contexts during the Maratha Empire.",
    "Some libraries in India hold extensive collections of Modi Lipi documents.",
    "The Peshwas maintained detailed records in Modi Lipi, which are crucial for studying Maratha history.",
    "The British government initially used Modi Lipi in official documents but gradually phased it out.",
    "Modi Lipi is still studied by historians researching the administrative history of Maharashtra.",
    "It was commonly used for financial transactions, including recording taxes and trade.",
    "Modi Lipi can be written faster than Devanagari due to its flowing script style.",
    "The Devanagari script gradually replaced Modi Lipi in schools and institutions after Indian independence.",
    "Several ancient royal decrees and letters were written in Modi Lipi.",
    "Marathi manuscripts written in Modi Lipi often feature religious hymns and epic poetry.",
    "Modi Lipi is often seen in historical documents related to land ownership and disputes.",
    "Scholars specializing in Indian scripts help decode Modi Lipi for historical research.",
    "The script includes numerous ligatures, where two or more consonants are combined into a single character.",
    "Modi Lipi characters have rounded shapes, which differ significantly from the angular shapes of Devanagari.",
    "The script uses fewer lines and strokes compared to Devanagari, making it visually distinct.",
    "Modi Lipi is one of the few scripts that was used for administrative and legal documentation.",
    "There are over 40 basic characters in the Modi script, including vowels and consonants.",
    "Modi Lipi has been categorized into different types depending on the time period.",
    "The script evolved to reduce the number of pen lifts required for writing, increasing speed.",
    "Several ancient Modi Lipi inscriptions have been found on copper plates.",
    "Historically, Modi Lipi was passed down from generation to generation through scribes.",
    "Many archives contain business-related documents written in Modi Lipi.",
    "The lack of horizontal lines in Modi Lipi was intended to speed up the writing process.",
    "Although used for administration, Modi Lipi was also employed in personal letters and diaries.",
    "Several regional dialects of Marathi are reflected in Modi Lipi texts.",
    "The introduction of the printing press in the 19th century reduced the use of Modi Lipi.",
    "Modi Lipi is making a comeback, with younger generations showing interest in learning it.",
    "The cursive nature of Modi Lipi allowed writers to cover more content in less space.",
    "The script was also used for military correspondence during the Maratha Empire.",
    "Modi Lipi can be difficult to read due to variations in handwriting styles.",
    "Several temples in Maharashtra have Modi Lipi inscriptions dating back centuries.",
    "The script has been recognized by the Unicode Standard, allowing for digital use.",
    "In its modern revival, Modi Lipi is being promoted through workshops and online courses.",
    "Modi Lipi's simplicity made it more efficient for quick writing compared to Devanagari.",
    "The script is regarded as one of the key elements of Maharashtra's rich cultural heritage.",
    "Learning Modi Lipi requires careful practice to master its unique ligatures and characters.",
    "Several researchers are working on developing fonts and digital tools for Modi Lipi.",
    "Many educational institutions in Maharashtra offer courses in Modi Lipi.",
    "Modi Lipi inscriptions have helped historians understand the socio-political history of the region.",
    "Digital libraries are being set up to store Modi Lipi manuscripts for future generations.",
    "The Indian government has taken steps to preserve and promote Modi Lipi.",
    "Modi Lipi's revival is seen as a way to reconnect with Maharashtra's past.",
    "The script played a vital role in the communication networks of the Maratha Empire.",
    "Many historical agreements and treaties were recorded in Modi Lipi.",
    "The inherent vowel in Modi Lipi characters can change based on diacritics.",
    "Many family archives in Maharashtra still hold Modi Lipi documents that are passed down through generations.",
    "Modi Lipi provides a glimpse into the administrative practices of medieval Maharashtra.",
    "The evolution of the script mirrors the changes in Marathi language and culture over time.",
    "Modi Lipi is considered a valuable part of India's epigraphic and linguistic history.",
    "Modern Modi Lipi fonts are being designed to make it easier for new learners to read",
    "The Modi script was extensively used by the Maratha Empire for diplomatic and administrative purposes.",
    "Peshwa-era documents are largely written in Modi Lipi, making them key sources for historical research.",
    "Modi Lipi was gradually replaced by Devanagari after the decline of the Maratha Empire.",
    "Modi Lipi is known for its speed and efficiency in writing due to its cursive nature.",
    "The word 'Modi' in the script's name is thought to mean 'to fold' or 'to break'.",
    "In some parts of Maharashtra, Modi Lipi remained in use until the early 20th century.",
    "Unlike Devanagari, Modi Lipi does not rely heavily on horizontal lines, making it more fluid.",
    "Modi Lipi was designed to be written continuously without lifting the pen, which enhanced writing speed.",
    "The script was widely used in legal and financial transactions in Maharashtra.",
    "Modi Lipi's flowing structure allowed scribes to record long documents quickly and efficiently.",
    "The script has a close relationship with the Brahmi script, from which it evolved.",
    "Modi Lipi evolved over time, with several variations in character shapes depending on the period.",
    "The British government introduced typewriters equipped with Modi Lipi characters for official use.",
    "Modi Lipi is still seen in certain inscriptions on temples and monuments in Maharashtra.",
    "Efforts to digitize Modi Lipi documents are ongoing in several historical archives.",
    "The Modi script was standardized in the 17th century under the rule of Shivaji Maharaj.",
    "Modi Lipi has fewer pen strokes than Devanagari, making it faster to write for administrative tasks.",
    "Many ancient land deeds, property documents, and official records in Maharashtra are written in Modi Lipi.",
    "Several scholars and linguists are working to preserve and promote the study of Modi Lipi.",
    "Modi Lipi's cursive nature made it especially useful for keeping military records and communications.",
    "The script is often seen in historical archives, museums, and libraries across Maharashtra.",
    "Several Modi Lipi manuscripts have been preserved, containing valuable information about the Maratha Empire.",
    "Modi Lipi had been the official script for the Marathi language for several centuries.",
    "Researchers are using optical character recognition (OCR) technology to digitize Modi Lipi documents.",
    "Modi Lipi was predominantly used by scribes for official documentation, legal matters, and business records.",
    "Shivaji Maharaj's administration adopted Modi Lipi to simplify the writing of Marathi for official use.",
    "In modern times, Modi Lipi has seen a revival with younger generations learning the script.",
    "The fluid, cursive design of Modi Lipi allowed documents to be written more compactly than Devanagari.",
    "Many Marathi-speaking people in rural areas continued using Modi Lipi into the 20th century.",
    "Modi Lipi is one of the few Indian scripts that was developed specifically for administrative use.",
    "Efforts are underway to include Modi Lipi in more school curriculums in Maharashtra.",
    "Modi Lipi inscriptions are an important part of India's cultural and historical heritage.",
    "Modi Lipi has several ligatures, combining two or more consonants into a single symbol.",
    "Linguists study Modi Lipi to gain insights into the development of the Marathi language.",
    "The script allowed for faster documentation and communication within the Maratha Empire.",
    "Modi Lipi manuscripts offer a unique glimpse into the bureaucratic workings of the Maratha Empire.",
    "Modi Lipi has its own system of numerals, distinct from Devanagari and other Indian scripts.",
    "Many ancient Modi Lipi documents are currently being digitized for preservation and research.",
    "Modi Lipi was once the dominant script used for writing Marathi, especially in Maharashtra.",
    "The British phased out Modi Lipi in favor of Devanagari during their rule in India.",
    "Modi Lipi's cursive nature makes it a popular subject for calligraphy and art enthusiasts.",
    "The script's ligatures can pose a challenge for modern learners accustomed to Devanagari.",
    "Many of the Peshwa's official communications and orders were written in Modi Lipi.",
    "Modi Lipi's simplicity made it more accessible for scribes than more complex scripts like Devanagari.",
    "Modi Lipi is characterized by its flowing, curved characters, which differ from the more angular Devanagari.",
    "The script was used not only for official documents but also for writing religious texts and poetry.",
    "Several workshops and courses are now available to help people learn Modi Lipi.",
    "Researchers are using Modi Lipi to better understand historical trade routes and financial transactions in Maharashtra.",
    "Modi Lipi's fluidity made it ideal for writing lengthy legal contracts and financial records.",
    "There are several online resources and apps designed to teach Modi Lipi to new learners.",
    "Shivaji Maharaj's rule saw the formal adoption of Modi Lipi for Marathi administration.",
    "Modi Lipi manuscripts provide key insights into the political and administrative history of Maharashtra.",
    "The script is still used in some traditional communities for personal and business correspondence.",
    "Several books and manuscripts from the Maratha period have been preserved in Modi Lipi.",
    "Many ancient copperplate inscriptions in Maharashtra are written in Modi Lipi.",
    "Modi Lipi is considered easier to write and read compared to other Indian scripts like Devanagari.",
    "During the Peshwa era, all official correspondence in Maharashtra was conducted in Modi Lipi.",
    "There are ongoing efforts to create Unicode fonts for Modi Lipi to make it more accessible digitally.",
    "The script evolved over centuries, incorporating influences from other regional writing systems.",
    "Modi Lipi was developed to meet the administrative needs of the rapidly expanding Maratha Empire.",
    "Many important historical treaties between the Marathas and other kingdoms are recorded in Modi Lipi.",
    "Modi Lipi is known for its distinctive rounded characters and ligatures.",
    "The Peshwas maintained records of taxes, land holdings, and military matters in Modi Lipi.",
    "The script's cursive style made it faster for scribes to write than the more rigid Devanagari script.",
    "Many Marathi manuscripts written in Modi Lipi feature religious hymns and devotional songs.",
    "The British administration played a major role in phasing out Modi Lipi in favor of Devanagari.",
    "Modi Lipi manuscripts are often stored in Indian libraries and archives for historical research.",
    "The inherent vowel in Modi Lipi can change based on the placement of diacritical marks.",
    "The revival of Modi Lipi is seen as part of a broader effort to preserve Maharashtra's cultural heritage.",
    "Several educational institutions now offer courses in Modi Lipi as part of Marathi language studies.",
    "Many ancient Maratha Empire documents written in Modi Lipi have yet to be fully deciphered.",
    "Some religious texts from Maharashtra have been written in Modi Lipi for centuries.",
    "The script has become an important part of Maharashtra's cultural identity and heritage.",
    "Modi Lipi is included in the Unicode Standard, allowing for its use in digital formats.",
    "Scholars are working to decode and translate Modi Lipi manuscripts for modern audiences.",
    "Modi Lipi's rounded shapes and ligatures make it visually distinct from other Indian scripts.",
    "The script was primarily used for official and administrative purposes by the Maratha Empire.",
    "Modi Lipi was created to streamline writing and reduce the number of strokes needed to form characters.",
    "Several Maratha-era treaties and agreements have been discovered written in Modi Lipi.",
    "Modi Lipi's ligatures often combine two or more consonants into a single fluid character.",
    "The script was widely used in Maharashtra but also spread to neighboring regions like Karnataka.",
    "Several efforts are underway to teach Modi Lipi through workshops and online courses.",
    "The Indian government has initiated projects to preserve and promote Modi Lipi as part of India's heritage.",
    "Modi Lipi has seen a resurgence in popularity with younger generations in Maharashtra.",
    "Shivaji Maharaj's administrative reforms cemented the use of Modi Lipi for official correspondence.",
    "The script has been the subject of several academic research papers and linguistic studies.",
    "Several inscriptions in Maharashtra's temples and forts are written in Modi Lipi.",
    "Learning Modi Lipi allows modern scholars to access valuable historical documents.",
    "Many legal documents and contracts from the Maratha Empire are preserved in Modi Lipi.",
    "Modi Lipi was favored for its speed and efficiency in writing long, detailed documents.",
    "Many temples and public buildings in Maharashtra have Modi Lipi inscriptions.",
    "Efforts are underway to create digital archives of Modi Lipi documents for future generations.",
    "Modi Lipi is now included in some school curriculums as part of Marathi language education.",
    "The script's unique characters and ligatures make it a subject of interest for typography enthusiasts.",
    "Modi Lipi played a crucial role in the administration of the Maratha Empire for several centuries.",
    "Several historical records of land grants and legal disputes were written in Modi Lipi.",
    "Modi Lipi offers valuable insights into the economic and social history of medieval Maharashtra.",
    "Many temples in Maharashtra feature Modi Lipi inscriptions that date back several centuries.",
    "Modi Lipi's cursive design allowed for fast, efficient writing, especially for administrative use.",
]
st.sidebar.markdown("---")
st.sidebar.subheader("Did you know?")
st.sidebar.info(np.random.choice(facts))