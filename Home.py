# Home.py
import streamlit as st
import sqlite3, uuid, qrcode
from io import BytesIO

def get_db():
    conn = sqlite3.connect("loyalty.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT,
        identifier TEXT UNIQUE
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS visits (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    return conn

st.title("Customer Registration")
name = st.text_input("Customer name")
if st.button("Register"):
    conn = get_db()
    cid = str(uuid.uuid4())
    identifier = str(uuid.uuid4())
    conn.execute("INSERT INTO customers VALUES (?,?,?)", (cid, name, identifier))
    conn.commit()
    # generate QR
    img = qrcode.make(identifier)
    buf = BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption=f"QR for {name}")
