from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Google Gemini API with the API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key for Google Gemini is missing! Please check your environment settings.")
else:
    genai.configure(api_key=api_key)

# Function to load the Gemini model and get responses
def get_gemini_response(input_text, image_data, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

# Function to handle image uploads
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit page config
st.set_page_config(page_title="Gemini Nutrition Analyzer", layout="centered")

# Custom CSS for UI design
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        .main-header {
            text-align: center;
            padding: 20px;
            background-color: #ff9800;
            color: white;
        }
        .file-upload-area {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .submit-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .submit-btn:hover {
            background-color: #45a049;
        }
        .response-area {
            margin-top: 20px;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("<div class='main-header'><h2>Gemini Nutrition Analyzer</h2></div>", unsafe_allow_html=True)

# Text input for prompt
input_text = st.text_input("Input Prompt: ", key="input")

# File uploader for image
uploaded_file = st.file_uploader("Upload an image of food (JPG/PNG):", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Base prompt for the nutritional analysis
input_prompt = """
    You are a nutrition expert. Analyze the food items and display each item name along with its nutritional values.
"""

# Submit button
if st.button("Analyze", key="submit", help="Click to analyze the uploaded image"):
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        
        # Display the response
        st.markdown("<div class='response-area'><h4>Analysis Result:</h4>", unsafe_allow_html=True)
        st.write(response)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Please upload an image first.")
