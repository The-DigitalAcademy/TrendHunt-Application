import streamlit as st
import cv2
import numpy as np
import os
import gdown
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tensorflow.keras.models import load_model
# Authenticate with Google Drive API
###
import pandas as pd
from tensorflow.keras.models import load_model
import requests

# Replace 'your_direct_download_link' with the actual direct download link you generated.
model_url = 'https://drive.google.com/uc?id=1-34mfUqojaxl16p4LKQGQ-KSP7IqeJI5'
model_file_path = 'my_model.h5'

response = requests.get(model_url)

if response.status_code == 200:
    with open(model_file_path, 'wb') as file:
        file.write(response.content)
    print(f'Model saved to {model_file_path}')
else:
    print('Failed to download the model.')
###
model=load_model('my_model.h5')

# Set the title and description of the app
st.title("Image Capture, Object Detection, and Image Details App")
st.write("This app allows you to capture or upload an image, perform object detection using YOLOv3, and add image details.")

# Function to capture an image from the webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    st.write("Press the 'Capture' button to take a picture.")
    
    if st.button("Capture"):
        ret, frame = cap.read()
        if ret:
            st.image(frame, caption= add_image_details(), use_column_width=True)
            cv2.imwrite("captured_image.jpg", frame)
        else:
            st.warning("Unable to capture image.")
    cap.release()

# Function to upload an image file
def upload_image():
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        cv2.imwrite("uploaded_image.jpg", image)

# Function to input image details
def add_image_details():
    st.header("Add Image Details")
    image_name = st.text_input("Image Name:", "MyImage")
    image_description = st.text_area("Image Description:")
    return image_name, image_description

# Main app logic
option = st.selectbox("Choose an option:", ("Capture Image", "Upload Image"))

if option == "Capture Image":
    capture_image()
elif option == "Upload Image":
    upload_image()

# Perform object detection using YOLOv3
if st.button("Detect Objects"):
    image_path = "captured_image.jpg" if option == "Capture Image" else "uploaded_image.jpg"
    st.write("Performing object detection...")

   st.write(
    st.image(image, caption="Detected Objects", use_column_width=True)

# Add image details and specify a directory to save the detected image
if st.button("Add Image Details and Save"):
    image_name, image_description = add_image_details()
    st.write("Saving detected image with details...")
    
    # Create a directory to save the images if it doesn't exist
    save_dir = "/Users/da_m1_48_/Desktop/Image_recognition_max/images"
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the image with details
    save_path = os.path.join(save_dir, f"{image_name}.jpg")
    cv2.imwrite(save_path, image)
    
    # Save image details to a text file
    with open(os.path.join(save_dir, f"{image_name}_details.txt"), "w") as details_file:
        details_file.write(f"Image Name: {image_name}\n")
        details_file.write(f"Image Description:\n{image_description}\n")
    
    st.success(f"Image and details saved in the '{save_dir}' directory.")
