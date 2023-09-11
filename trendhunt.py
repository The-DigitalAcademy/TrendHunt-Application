import streamlit as st
from main import perform_action
from user_interface import main_user
import sys 

# Define user and merchant login credentials (for demonstration purposes)
user_credentials = {
    "user1": "password1",
    "user2": "password2",
}

merchant_credentials = {
    "merchant1": "password1",
    "merchant2": "password2",
}

def main():
    st.title("Trendhunt")

    # Create a form to choose between user and merchant login
    login_option = st.selectbox("Select User Type:", ("User", "Merchant"))

    if login_option == "User":
        user_login()
    elif login_option == "Merchant":
        merchant_login()

def user_login():
    st.header("User Login")

    # Create user login form (e.g., username and password fields)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        # Authenticate the user and redirect to the user dashboard
        if authenticate_user(username, password):
            st.success("Login successful!")
            result = perform_action()
            st.write(result)
            # Run the new script after a successful login
            main_user()
            # Close the login script
            sys.exit()
        else:
            st.error("Invalid credentials!")

def merchant_login():
    st.header("Merchant Login")

    # Create merchant login form (e.g., merchant ID and password fields)
    merchant_id = st.text_input("Merchant ID", placeholder="Enter your merchant ID")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        # Authenticate the merchant and redirect to the merchant dashboard
        if authenticate_merchant(merchant_id, password):
            st.success("Login successful!")
            st.write("Redirecting to merchant dashboard...")
            # Close the login script
            st.experimental.stop()
        else:
            st.error("Invalid credentials!")

def authenticate_user(username, password):
    # Check if the provided username and password match user credentials
    if username in user_credentials and user_credentials[username] == password:
        return True
    return False

def authenticate_merchant(merchant_id, password):
    # Check if the provided merchant ID and password match merchant credentials
    if merchant_id in merchant_credentials and merchant_credentials[merchant_id] == password:
        return True
    return False

if __name__ == "__main__":
    main()
