import streamlit as st
from PIL import Image

# Title of the app
st.title("Food Tracking App")

# Sidebar for navigation
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", ["Home", "Upload Food Image", "About"])

# Custom background and button styles using CSS
custom_css = """
    <style>
    .stApp {
        background-color: #f3f4f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 18px;
    }
    </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

# Define home page
if nav_option == "Home":
    st.header("Welcome to the Food Tracking App!")
    st.write("This app allows you to track the nutritional information and calories of food by simply uploading an image.")
    st.write("Navigate to the 'Upload Food Image' section to get started.")

# Define upload page
elif nav_option == "Upload Food Image":
    st.header("Upload a Food Image")
    
    # Image upload widget
    uploaded_image = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])
    
    # If an image is uploaded
    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # In a real app, you would pass the image to your model or API to get nutrition data
        st.write("Processing image...")

        # Placeholder example for calorie and nutrition data
        # Replace this with actual API call and response
        example_nutrition_data = {
            "Calories": "250 kcal",
            "Carbohydrates": "30 g",
            "Protein": "12 g",
            "Fat": "10 g"
        }

        # Display the nutrition data
        st.subheader("Nutritional Information:")
        for nutrient, value in example_nutrition_data.items():
            st.write(f"{nutrient}: {value}")

# Define About page
elif nav_option == "About":
    st.header("About")
    st.write("This food tracking app uses AI to identify food items from images and provides nutritional information and calorie count.")
    st.write("Powered by Streamlit and integrated with various APIs for image recognition and nutrition data.")
