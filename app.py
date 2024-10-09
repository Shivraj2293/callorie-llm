import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Set up Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the page layout
st.set_page_config(page_title="Gemini Food Nutrition Analysis", layout="centered")

# Custom CSS for background, buttons, and animations
custom_css = """
    <style>
    /* Custom background */
    .stApp {
        background-image: url('https://source.unsplash.com/1600x900/?healthy-food');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }

    /* Navigation Buttons */
    .nav-button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 18px;
        transition: transform 0.3s ease-in-out;
    }

    .nav-button:hover {
        background-color: #45a049;
        transform: scale(1.1);
    }

    /* Upload Image Button */
    .upload-btn {
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 16px;
    }

    .upload-btn:hover {
        background-color: #0b7dda;
    }

    /* Response box animation */
    .response-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        animation: fadeIn 1.5s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """

st.markdown(custom_css, unsafe_allow_html=True)

# Define navigation buttons using st.sidebar
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", ["Home", "Upload Food Image", "About"])

# Define the home page
if nav_option == "Home":
    st.header("Welcome to Gemini Food Nutrition Analysis!")
    st.subheader("Powered by Gemini AI")
    st.write("Upload an image of food, and I will provide an estimated nutritional breakdown based on the image.")
    st.markdown('<button class="nav-button">Get Started</button>', unsafe_allow_html=True)

# Define upload page
elif nav_option == "Upload Food Image":
    st.header("Upload Your Food Image")

    # Input prompt section
    input = st.text_input("Enter your dietary preferences or instructions:", key="input")

    # Image upload section with custom styled button
    uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Button to submit the input and image
    submit = st.button("Analyze Nutrition", key="analyze-btn", help="Click to analyze the nutrition")

    # Custom prompt for nutrition analysis
    input_prompt = """
                  You are a nutrition expert. Analyze the food items shown in the image and provide a detailed breakdown of their nutritional content. For each food item, list the following information in short:

    1. Item Name:
       - Calories: [Number of calories]
       - Protein: [Grams of protein]
       - Carbohydrates: [Grams of carbohydrates]
       - Fats: [Grams of fats]
       - Fiber: [Grams of fiber]
       - Sugars: [Grams of sugars]
    ---
    Total Calories: [Sum of all calories]
    Total Protein: [Sum of all Protein]
    Total Carbohydrates: [Sum of all Carbohydrates]
    Total Fats: [Sum of all Fats]
    Total Fiber: [Sum of all Fiber]
    Total Sugars: [Sum of all Sugars]

    Don't answer 'I cannot give you exact details'. Provide estimated information.
    Suggest dietary recommendations according to Indian cuisine in short.
    """

    # Function to process the uploaded image and get the response from the Gemini model
    def input_image_setup(uploaded_file):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")

    # Function to get the Gemini model response
    def get_gemini_response(input, image, prompt):
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([input, image[0], prompt])
        return response.text

    # Process when the submit button is clicked
    if submit:
        if uploaded_file:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input, image_data, input_prompt)
            st.markdown(f'<div class="response-box"><h4>Nutrition Analysis Result:</h4><p>{response}</p></div>', unsafe_allow_html=True)
        else:
            st.error("Please upload an image to analyze.")

# Define the About page
elif nav_option == "About":
    st.header("About the Gemini Food Nutrition App")
    st.write("""
    This application allows users to upload images of food items, and the Gemini AI will analyze the image and provide an estimated breakdown of the nutritional content.
    
    The app is powered by Google Gemini's advanced AI capabilities, providing a fast and intelligent way to track food intake and make informed dietary decisions.
    """)
    st.markdown('<button class="nav-button">Learn More</button>', unsafe_allow_html=True)

# Footer
st.write("---")
st.write("© 2024 Gemini Food Nutrition Analysis. Powered by AI.")
