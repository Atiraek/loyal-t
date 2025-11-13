import sqlite3
import streamlit as st

def get_db():
    return sqlite3.connect("loyalty.db")

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("Dashboard")
conn = get_db()
cust_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
visit_count = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
st.metric("Customers", cust_count)
st.metric("Visits", visit_count)


if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
