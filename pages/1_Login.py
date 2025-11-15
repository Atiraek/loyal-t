import streamlit as st
from modules import auth

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Admin Login")
user = st.text_input("Username")
pw = st.text_input("Password", type="password")

if st.button("Login"):
    if auth.login(user, pw):
        st.session_state.logged_in = True
        st.success("Logged in")
    else:
        st.error("Invalid credentials")

if st.session_state.logged_in and st.button("Logout"):
    auth.logout()
