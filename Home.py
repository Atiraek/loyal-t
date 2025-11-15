import streamlit as st
from modules import db, qr, utils

st.title("Customer Registration")
name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Register"):
    if not name or not email:
        st.error("Name and email required")
    elif not utils.valid_email(email):
        st.error("Invalid email format")
    else:
        conn = db.get_db()
        existing = conn.execute("SELECT 1 FROM customers WHERE email=?", (email,)).fetchone()
        if existing:
            st.error("Email already registered")
        else:
            code = qr.generate_unique_code(conn)
            db.add_customer(conn, name, email, code)
            st.image(qr.make_qr(code), caption=f"QR for {name}")
