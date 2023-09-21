import streamlit as st
import pandas as pd
import os
import shutil

# Create a folder to store uploaded files and folders
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create a folder to store uploaded folders
if not os.path.exists("uploaded_folders"):
    os.makedirs("uploaded_folders")

# Streamlit app header
st.title("Vendor")
st.write("This is where you will upload your products in the form of CSV/Excel files or folders to be loaded in the system")

# Sidebar for upload option
upload_option = st.sidebar.radio("Select upload option:", ("CSV/Excel File", "Folder"))

if upload_option == "CSV/Excel File":
    # Sidebar for file upload
    st.sidebar.header("Upload a CSV/Excel File")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Display file details
        st.sidebar.write("File details:")
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.sidebar.write(file_details)

        # Save the file in the 'uploads' folder
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.sidebar.success("File uploaded successfully!")

elif upload_option == "Folder":
    # Sidebar for folder upload
    st.sidebar.header("Upload a Folder")
    selected_folder = st.sidebar.text_input("Enter the path to a folder:")

    if selected_folder:
        # Check if the selected folder exists
        if os.path.exists(selected_folder) and os.path.isdir(selected_folder):
            # Move the selected folder to the 'uploaded_folders' directory
            destination_folder = os.path.join("uploaded_folders", os.path.basename(selected_folder))
            shutil.move(selected_folder, destination_folder)
            st.sidebar.success("Folder uploaded successfully!")

# List the files in the 'uploads' folder
uploaded_files = os.listdir("uploads")

# Display uploaded files
st.header("Uploaded Files")
if not uploaded_files:
    st.write("No files have been uploaded yet.")
else:
    st.write("List of uploaded files:")
    for file in uploaded_files:
        st.write(file)

# List the folders in the 'uploaded_folders' directory
uploaded_folders = os.listdir("uploaded_folders")

# Display uploaded folders
st.header("Uploaded Folders")
if not uploaded_folders:
    st.write("No folders have been uploaded yet.")
else:
    st.write("List of uploaded folders:")
    for folder in uploaded_folders:
        st.write(folder)

# You can now perform operations on these uploaded files and folders as needed.
