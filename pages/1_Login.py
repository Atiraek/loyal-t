# pages/1_Login.py
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Employee Login")
user = st.text_input("Username")
pw = st.text_input("Password", type="password")
if st.button("Login"):
    if user == "admin" and pw == "secret":  # replace with env vars
        st.session_state.logged_in = True
        st.success("Logged in")
    else:
        st.error("Invalid credentials")
