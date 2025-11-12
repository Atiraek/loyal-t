# pages/2_Scan.py
import uuid
import streamlit as st, sqlite3, datetime

def get_db():
    return sqlite3.connect("loyalty.db")

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("Scan QR")
identifier = st.text_input("Paste scanned QR code")
if st.button("Record Visit"):
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
