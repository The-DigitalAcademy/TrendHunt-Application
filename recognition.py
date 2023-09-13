import streamlit as st
import cv2
import numpy as np
import os
import gdown
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# Authenticate with Google Drive API
gauth = GoogleAuth()
gauth.LocalWebserverAuth() 

drive = GoogleDrive(gauth)

# Replace 'file_id' with your model's file ID
file_id = '1-34mfUqojaxl16p4LKQGQ-KSP7IqeJI5.'

# Find the file by its ID
file = drive.CreateFile({'id': file_id})

# Read the model file's content
model_content = file.GetContentString()
# For example, you can save it to a .h5 file and load the TensorFlow model
with open('my_model.h5', 'wb') as f:
    f.write(model_content.encode())

# Load the TensorFlow model
from tensorflow.keras.models import load_model
model = load_model('my_model.h5')
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

    # Load YOLOv3 model
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    with open("coco.names", "r") as f:
        classes = f.read().strip().split("\n")
    
    # Load the image for detection
    image = cv2.imread(image_path)
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    
    net.setInput(blob)
    layer_names = net.getUnconnectedOutLayersNames()
    outputs = net.forward(layer_names)

    # Loop over each detection
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x, center_y, width, height = list(map(int, detection[0:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])))
                x, y = center_x - width // 2, center_y - height // 2
                color = (0, 255, 0)
                cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)
                label = f"{classes[class_id]}: {confidence:.2f}"
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
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

