import re
import random
import sqlite3
import uuid
import qrcode
import streamlit as st
from io import BytesIO


def get_db():
    conn = sqlite3.connect("loyalty.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        identifier TEXT UNIQUE
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS visits (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    return conn


def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e)


def generate_unique_code(conn):
    while True:
        code = str(random.randint(10000000, 99999999))  # 8-digit numeric
        exists = conn.execute("SELECT 1 FROM customers WHERE identifier=?", (code,)).fetchone()
        if not exists:
            return code


st.title("Customer Registration")
name = st.text_input("Name")
email = st.text_input("Email")


if st.button("Register"):
    if not name or not email:
        st.error("Name and email required")
    elif not valid_email(email):
        st.error("Invalid email format")
    else:
        conn = get_db()
        # ensure unique email
        existing = conn.execute("SELECT 1 FROM customers WHERE email=?", (email,)).fetchone()
        if existing:
            st.error("Email already registered")
        else:
            cid = str(uuid.uuid4())
            code = generate_unique_code(conn)  # see next section
            conn.execute("INSERT INTO customers (id,name,email,identifier) VALUES (?,?,?,?)",
                         (cid, name, email, code))
            conn.commit()
            img = qrcode.make(code)
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption=f"QR for {name}. Save for scanning at each visit!")
