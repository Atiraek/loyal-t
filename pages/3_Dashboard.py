# pages/3_Dashboard.py
import streamlit as st, sqlite3

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
