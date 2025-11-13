import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

ADMINS = {}
for i in range(1, 4):
    cred = os.getenv(f"ADMIN{i}")
    if cred:
        user, pw = cred.split(":")
        ADMINS[user] = pw

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Admin Login")
user = st.text_input("Username")
pw = st.text_input("Password", type="password")

if st.button("Login"):
    if user in ADMINS and pw == ADMINS[user]:
        st.session_state.logged_in = True
        st.success("Logged in")
    else:
        st.error("Invalid credentials")


if st.session_state.logged_in and st.button("Logout"):
    st.session_state.logged_in = False
    st.success("Logged out")
    st.rerun()
