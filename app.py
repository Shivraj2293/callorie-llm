from dotenv import load_dotenv
import streamlit as st
import os
import io
from PIL import Image
from google.cloud import vision
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Google Gemini API with the API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key for Google Gemini is missing! Please check your environment settings.")
else:
    genai.configure(api_key=api_key)

# Function to analyze the uploaded image using Google Vision API
def analyze_image(image_bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Extract labels (e.g., food items)
    result = [label.description for label in labels]

    if response.error.message:
        raise Exception(f"{response.error.message}")

    return result

# Function to load the Gemini model and get responses
def get_gemini_response(food_items, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    input_text = "The image contains: " + ", ".join(food_items)
    response = model.generate_content([input_text, prompt])
    return response.text

# Function to handle image uploads
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.getvalue()
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
    You are a nutrition expert. Analyze the food items and display each item's name along with its nutritional values.
"""

# Submit button
if st.button("Analyze", key="submit", help="Click to analyze the uploaded image"):
    if uploaded_file is not None:
        # Process the uploaded image
        image_data = input_image_setup(uploaded_file)

        # Analyze the image using Google Vision API
        try:
            food_items = analyze_image(image_data)
            # Pass the extracted food items to Gemini for further analysis
            response = get_gemini_response(food_items, input_prompt)
            
            # Display the response
            st.markdown("<div class='response-area'><h4>Analysis Result:</h4>", unsafe_allow_html=True)
            st.write(response)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error analyzing the image: {str(e)}")
    else:
        st.error("Please upload an image first.")
