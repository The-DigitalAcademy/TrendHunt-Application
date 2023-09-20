import streamlit as st
import psycopg2
#import psycopg2-binary
import numpy as np
import os
#import subprocess



# Connecting to the DB
def init_connection():
    db_params = {
        'host': 'localhost',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '',
        'port': 5432
    }

    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


# Create the 'user_tabl' table if it doesn't exist
def create_usertable():
    cur.execute('CREATE TABLE IF NOT EXISTS user_tabl (username TEXT, password TEXT);')
    conn.commit()

# Add new user data to the 'user_tabl' table
def add_userdata(username, password):
    cur.execute('INSERT INTO user_tabl (username, password) VALUES (%s, %s);', (username, password))
    conn.commit()

# Login function
def login_user(username, password):
    cur.execute('SELECT * FROM user_tabl WHERE username=%s AND password=%s;', (username, password))
    data = cur.fetchall()
    return data

# Create Streamlit app
def main():
    st.title("Login or Register")
    # Initialize the database connection and cursor
    conn = init_connection()
    
    if conn is None:
        st.error("Error connecting to the database.")
    else:
        try:
            cur = conn.cursor()
    
            st.title("Login or Register")
    
            # Create input fields for username and password
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
    
            # Radio button for login or registration
            action = st.radio("Select Action:", ("Login", "Register"))
    
            if action == "Login":
                if st.button("Login"):
                    create_usertable()
                    result = login_user(username, password)
                    if result:
                        st.success("Login Successful!")
                        st.text('Redirecting to the main app...')
                        st.write("My name is Malebo founder at TrendHunt")
                    else:
                        st.error("Invalid Credentials. Please try again.")
            else:
                if st.button("Register"):
                    create_usertable()
                    add_userdata(username, password)
                    st.success("Registration Successful! You can now login.")
                else:
                    st.error("Registration failed. User already exists or invalid data.")
    
        except psycopg2.Error as e:
            st.error(f"Error: {e}")


   
if __name__ == "__main__":
    main()
