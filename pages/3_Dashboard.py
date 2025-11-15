import streamlit as st
from modules import db, auth

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("Dashboard")
conn = db.get_db()
cust_count, visit_count = db.stats(conn)
st.metric("Customers", cust_count)
st.metric("Visits", visit_count)

if st.button("Logout"):
    auth.logout()
