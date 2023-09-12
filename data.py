import streamlit as st
import sqlite3
from PIL import Image
import io


# Create a Streamlit app
def main():
    st.title("Login or Register")

    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Radio button for login or registration
    action = st.radio("Select Action:", ("Login", "Register"))

    if action == "Login":
        if st.button("Login"):
            if check_credentials(username, password):
                st.success("Login Successful!")
                st.text('Redirecting to the main app...')
                # Add your redirection code here
            else:
                st.error("Invalid Credentials. Please try again.")
    else:
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration Successful! You can now login.")
            else:
                st.error("Registration failed. User already exists or invalid data.")

def check_credentials(username, password):
    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Create a table to store user credentials if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    # Check if the provided credentials match the stored credentials
    cursor.execute("SELECT * FROM user WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data and user_data[2] == password:
        conn.close()
        return True

    conn.close()
    return False

def register_user(username, password):
    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Create a table to store user credentials if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    # Check if the user already exists
    cursor.execute("SELECT * FROM user WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False

    # Insert the user into the database
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    main()
