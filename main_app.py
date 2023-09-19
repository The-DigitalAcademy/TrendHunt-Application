import streamlit as st
import os
import keras
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, decode_predictions, preprocess_input
from PIL import Image
import pickle
from scipy.spatial import distance 




# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet')

# Load the saved PCA features and images list
file_path = 'pickle.p'
images, pca_features, pca = pickle.load(open(file_path, 'rb'))

# Define the feature extractor using the VGG16 model
base_model = VGG16(weights='imagenet')
layer_name = 'fc2'
feat_extractor = keras.models.Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)

# Function to load and preprocess an image
def load_image(path):
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    return x

# Streamlit UI
st.title("Trendhunt Application")

# Upload an image
uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Perform predictions on the uploaded image
    img = Image.open(uploaded_image)
    img_path = "temp_image.jpg"
    img.save(img_path)

    # Load and preprocess the uploaded image
    x = load_image(img_path)

    # Make predictions using the model
    predictions = model.predict(x)

    # Decode the predictions to get class labels and probabilities
    decoded_predictions = decode_predictions(predictions, top=5)[0]

    #st.subheader("Top Predicted Classes:")
    #for label, description, score in decoded_predictions:
    #    st.write(f"{description} ({label}): {score:.2f}")

    # Calculate PCA features for the uploaded image
    img_features = feat_extractor.predict(x)[0]
    img_pca_features = pca.transform([img_features])[0]

    # Calculate distances to all other images
    distances = [distance.cosine(img_pca_features, feat) for feat in pca_features]
    idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[0:5]

    st.subheader("Most Similar Images:")
    for idx in idx_closest:
        similar_img = Image.open(images[idx])
        st.image(similar_img, caption=f"Similar Image {idx}", use_column_width=True)

