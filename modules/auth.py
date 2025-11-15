import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

ADMINS = {}
for i in range(1, 4):
    cred = os.getenv(f"ADMIN{i}")
    if cred:
        user, pw = cred.split(":")
        ADMINS[user] = pw

def login(user, pw):
    return user in ADMINS and pw == ADMINS[user]

def logout():
    st.session_state.logged_in = False
    st.rerun()
