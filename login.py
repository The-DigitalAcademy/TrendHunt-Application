import streamlit as st
import sqlite3
from PIL import Image
import io
import psycopg2

#Databasde Management
#Conneting to db
def init_connection():
    db_params = {
        'host': 'localhost',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '',
        'port':5432
    }
    
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None
conn = init_connection()
cur = conn.cursor()

def create_usertable():
    cur.execute('CREATE TABLE IF NOT EXISTS user_tabl(username TEXT,password TEXT);')
    

def add_userdata(username,password):
    cur.execute('INSERT INTO user_tabl(username,password) VALUES(%s,%s)',(username,password))
    conn.commit()
    
# Login function
def login_user(username,password):
    cur.execute('SELECT * FROM user_tabl WHERE username=%s AND password=%s',(username,password))
    data=cur.fetchall()
    return data

def view_all_users():
    cur.execute('SELECT * FROM user_tabl')
    data=cur.fetchall()
    return data

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
            
            #password ="12345"
            #username="Admin"
            create_usertable()
            result=login_user(username,password)
            st.success("Login Successful!")
            st.text('Redirecting to the main app...')
                # Add your redirection code here
            st.write(view_all_users())
        else:
                st.error("Invalid Credentials. Please try again.")
    else:
        if st.button("Register"):
            create_usertable()
            add_userdata(username,password)
            st.success("You have succesfully created a valid Acccount")
            st.info("Go to Login Menu to login")
            st.success("Registration Successful! You can now login.")
        else:
                st.error("Registration failed. User already exists or invalid data.")

 


if __name__ == "__main__":
    main()

