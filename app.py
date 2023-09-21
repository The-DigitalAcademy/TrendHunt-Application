
import streamlit as st
import os
import keras
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, decode_predictions, preprocess_input
from PIL import Image
import pickle
from scipy.spatial import distance
import pandas as pd

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet')

# Load the saved PCA features and images list
file_path = '/content/my_data.p'
images, pca_features, pca = pickle.load(open(file_path, 'rb'))

# Define the feature extractor using the VGG16 model
base_model = VGG16(weights='imagenet')
layer_name = 'fc2'
feat_extractor = keras.models.Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)

# Function to load and preprocess an image
def load_image(path):
    img = image.load_img(path, target_size=(224, 224))

    # Ensure the image is in RGB mode
    if img.mode != "RGB":
        img = img.convert("RGB")

    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    return x

# Streamlit UI
st.title("Trendhunt Application")

# Landing page (About and Login)
landing_page = st.sidebar.selectbox("Select Page", ["About", "Login"])

if landing_page == "About":
    st.write("The Trendhunt app is a revolutionary solution designed to address the challenges people face in locating specific items they desire in today's digital age. With the abundance of information on the internet, finding the exact product can be a daunting task. Trendhunt aims to simplify this process by providing a comprehensive and easily accessible platform for users to discover similar items based on a picture they upload.")

    # Add a picture under the "Trendhunt application" text
    #st.sidebar.image("https://i.fbcd.co/products/resized/resized-750-500/ddc5250f28dcf85d8238ecc732a8752b73e3685762d6dad4b32c4c9359538e77.jpg", caption="Trendhunt Logo", use_column_width=True)
    #image = Image.open('/Users/da_m1_19/Downloads/icon.jpg') 
    #st.image(image, caption='TrendHunt App')
elif landing_page == "Login":
    st.sidebar.write("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Check login credentials (you can replace this with your authentication logic)
        if username == "your_username" and password == "your_password":
            st.success("Login successful! Redirecting to the upload page...")
            landing_page = "Upload Image"  # Redirect to the upload page
        else:
            st.error("Login failed. Please check your credentials.")

# Upload an image
uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Perform predictions on the uploaded image
    img = Image.open(uploaded_image)

    # Convert the image to RGB mode explicitly
    img = img.convert("RGB")

    img_path = "temp_image.jpg"
    img.save(img_path)

    # Load and preprocess the uploaded image
    x = load_image(img_path)

    # Make predictions using the model
    predictions = model.predict(x)

    # Decode the predictions to get class labels and probabilities
    decoded_predictions = decode_predictions(predictions, top=5)[0]


    # Calculate PCA features for the uploaded image
    img_features = feat_extractor.predict(x)[0]
    img_pca_features = pca.transform([img_features])[0]

    # Calculate distances to all other images
    distances = [distance.cosine(img_pca_features, feat) for feat in pca_features]
    idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[0:5]

    st.subheader("Most Similar Images:")

    # Read the data from the CSV file once
    data = pd.read_csv("styles_eddie.csv", sep=";", error_bad_lines=False, warn_bad_lines=True)
    data = data.reset_index(drop=True)
    for idx in idx_closest:
        similar_img = Image.open(images[idx])
        product_id = os.path.splitext(os.path.basename(images[idx]))[0]
        print(product_id)
        print(type(product_id))
        print(data)
        caption = data[data['id'] == int(product_id)]['productDisplayName'].values[0]
        caption1 = data[data['id'] == int(product_id)]['gender'].values[0]
        caption2 = data[data['id'] == int(product_id)]['Price'].values[0]
        caption3 = data[data['id'] == int(product_id)]['store_name'].values[0]
        caption4 = data[data['id'] == int(product_id)]['Location'].values[0]


        st.image(similar_img, use_column_width=True)
        lst = [caption, caption1,caption2,caption3,caption4]

        lst = [f'Product Name: {caption}' , f'Gender: {caption1}' , f'Price: {caption2}', f'store_name: {caption3}', f'Location: {caption4}', f'Gender: {caption1}']
        for i in lst:
            st.markdown(i)
        
