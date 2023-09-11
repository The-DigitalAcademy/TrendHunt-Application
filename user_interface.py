import streamlit as st
import os
import json

def main_user():
    st.title("Image Viewer and Details")

    # Directories (hardcoded paths)
    base_directory = "/Users/da_m1_24/Desktop/Final_Project"
    image_directory = os.path.join(base_directory, "images")
    json_file_path = os.path.join(base_directory, "styles.json")

    if not os.path.exists(image_directory) or not os.path.exists(json_file_path):
        st.error("Image directory or JSON file does not exist.")
        return

    # Load JSON data
    try:
        with open(json_file_path, 'r') as json_file:
            image_details = json.load(json_file)
    except Exception as e:
        st.error(f"Error loading JSON file: {str(e)}")
        return

    # List all image files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not image_files:
        st.error("No image files found in the directory.")
        return

    # Display image selection dropdown
    selected_image = st.selectbox("Select an image:", image_files)

    # Display the selected image
    image_path = os.path.join(image_directory, selected_image)
    st.image(image_path, use_column_width=True)

    # Display image details from JSON file
    if selected_image in image_details:
        st.subheader("Image Details:")
        details = image_details[selected_image]
        for key, value in details.items():
            st.write(f"{key}: {value}")
    else:
        st.warning("No details found for this image in the JSON file.")

if __name__ == "__main__":
    main()
