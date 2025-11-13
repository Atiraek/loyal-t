import uuid
import sqlite3
import datetime
import streamlit as st
import pyzbar.pyzbar as pyzbar
from PIL import Image


def get_db():
    return sqlite3.connect("loyalty.db")


if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()


st.title("Scan QR")


use_camera = st.checkbox("Use camera to scan QR")
identifier = None

if use_camera:
    img = st.camera_input("Scan QR")
    if img:
        # decode QR using Pillow + qrcode or pyzbar
        image = Image.open(img)
        decoded = pyzbar.decode(image)
        if decoded:
            identifier = decoded[0].data.decode("utf-8")
            
if not identifier:
    identifier = st.text_input("Enter QR code manually")

# identifier = st.text_input("Paste scanned QR code")

if st.button("Record Visit") and identifier:
    conn = get_db()
    cust = conn.execute("SELECT id,name FROM customers WHERE identifier=?",(identifier,)).fetchone()
    if not cust:
        st.error("Customer not found")
    else:
        conn.execute("INSERT INTO visits (id,customer_id) VALUES (?,?)",(str(uuid.uuid4()),cust[0]))
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM visits WHERE customer_id=?",(cust[0],)).fetchone()[0]
        st.success(f"{cust[1]} now has {count} visits")
        if count % 4 == 0:
            st.info("Base reward available!")


if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
