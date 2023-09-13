import tensorflow as tf
import streamlit as st
import cv2
import numpy as np
import os
import gdown
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tensorflow.keras.models import load_model
# Authenticate with Google Drive API
try:
    model_path = r"https://drive.google.com/file/d/1-34mfUqojaxl16p4LKQGQ-KSP7IqeJI5/my data/model.h5"
    model = load_model(model_path)
except:
   
    print("...it seems to be better to use more simple naming with the .h5 file!")


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

    ##test
    # Get the classes
classes =['Hand-bags', 'wallets', 'Bags', 'Balls', 'Sunglasses', 'shorts', 'Pants', 'T-shirts', 'sneakers', 'Loafers', 'Socks', 'Watches', 'Sandals']

# Load the image for detection
image_path = "path/to/image.jpg"
image = cv2.imread(image_path)

# Convert the image to a tensor
image_tensor = tf.convert_to_tensor(image)

# Resize the image to the input size of the model
image_tensor = tf.image.resize(image_tensor, (416, 416))

# Predict the bounding boxes and classes for the image
boxes, classes, scores = model(image_tensor)

# Draw the bounding boxes and labels on the image
for box, class_id, score in zip(boxes, classes, scores):
    center_x, center_y, width, height = box.numpy()
    x, y = int(center_x - width / 2), int(center_y - height / 2)
    color = (0, 255, 0)
    cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)
    label = f"{classes[class_id]}: {score:.2f}"
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Display the image
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
    ###end test
   
    
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

