import streamlit as st
import subprocess
import os

# Create a dictionary to store user credentials (in-memory, not secure)
user_credentials = {
    'username': 'admin',
    'password': 'password123',
}

# Create Streamlit app
def main():
    st.title("Login Page")

    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the provided credentials match the stored credentials
    if st.button("Login"):
        if username == user_credentials['username'] and password == user_credentials['password']:
            st.success("Login Successful!")
            st.text('Redirecting to the main app...')
            subprocess.Popen(['streamlit', 'run', 'recognition.py'])
            os._exit(status=True)
        else:
            st.error("Invalid Credentials. Please try again.")

if __name__ == "__main__":
    main()
