
import streamlit as st
import pandas as pd
import os

# Create a folder for user data if it doesn't exist
data_folder = "user_data"
os.makedirs(data_folder, exist_ok=True)

# Define the CSV file path for user data
user_data_file = os.path.join(data_folder, "user_data.csv")

# Create an empty DataFrame to store user data
if not os.path.exists(user_data_file):
    user_data = pd.DataFrame(columns=["Username", "Password", "Role"])
    user_data.to_csv(user_data_file, index=False)
else:
    user_data = pd.read_csv(user_data_file)

# Streamlit app
st.title("User Login and Registration")

# Sidebar option to select between login and registration
menu = st.sidebar.radio("Menu", ["Login", "Register", "Registered Users"])

# Function to register a new user or supplier
def register_user(username, password, role):
    global user_data
    user_data = user_data.append({"Username": username, "Password": password, "Role": role}, ignore_index=True)
    user_data.to_csv(user_data_file, index=False)
    st.success("Registration successful! You can now log in as a {}.".format(role))

# Function to check if a user or supplier exists and the provided password is correct
def login_user(username, password, role):
    global user_data
    user_exists = (user_data["Username"] == username) & (user_data["Password"] == password) & (user_data["Role"] == role)
    return user_exists.any()

if menu == "Register":
    st.header("User Registration")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Select Role", ["User", "Supplier"])

    if st.button("Register"):
        if new_username and new_password:
            register_user(new_username, new_password, new_role)
        else:
            st.warning("Both username and password are required for registration.")

elif menu == "Login":
    st.header("User Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    login_role = st.selectbox("Select Role", ["User", "Supplier"])

    if st.button("Login"):
        if login_username and login_password:
            if login_user(login_username, login_password, login_role):
                st.success("Login successful as a {}.".format(login_role))

                # Redirect to user.py or supplier.py based on the role
                if login_role == "User":
                    st.experimental_set_query_params(role="User")
                elif login_role == "Supplier":
                    st.experimental_set_query_params(role="Supplier")
            else:
                st.error("Login failed. Check your username, password, and role.")
        else:
            st.warning("Both username and password are required for login.")

elif menu == "Registered Users":
    st.header("Registered Users")
    st.table(user_data[["Username", "Role"]])

# Button to initiate redirection
if "role" in st.experimental_get_query_params():
    role = st.experimental_get_query_params()["role"]
    if role == "User":
        if st.button("Go to User Dashboard"):
            st.experimental_set_query_params()
            # Redirect to user.py
            st.experimental_rerun()
    elif role == "Supplier":
        if st.button("Go to Supplier Dashboard"):
            st.experimental_set_query_params()
            # Redirect to supplier.py
            st.experimental_rerun()
