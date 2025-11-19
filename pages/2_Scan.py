import streamlit as st
from modules import db, qr

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("Scan QR")
use_camera = st.checkbox("Use camera to scan QR")
identifier = None

if use_camera:
    img = st.camera_input("Scan QR")
    if img:
        identifier = qr.decode_qr(img)

if not identifier:
    identifier = st.text_input("Enter QR code manually")

if st.button("Record Visit") and identifier:
    conn = db.get_db()
    cust = db.get_customer_by_identifier(conn, identifier)
    if not cust:
        st.error("Customer not found")
    else:
        total = db.record_visit(conn, cust[0])
        streak, threshold = db.visit_progress(total)
        st.success(f"{cust[1]} now has {total} total visits")
        st.info(f"Current streak: {streak}/{threshold}")
        if streak == threshold:
            st.success("🎉 Base reward available!")

if st.button("Logout"):
    from modules import auth
    auth.logout()
