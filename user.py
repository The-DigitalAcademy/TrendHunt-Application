# user_interface.py
import streamlit as st
from main import perform_action

def main():
    st.title("Streamlit App")

    if st.button("Click to Perform Action"):
        result = perform_action()
        st.write(result)

if __name__ == "__main__":
    main()
