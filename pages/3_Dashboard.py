import streamlit as st
import pandas as pd
from modules import db, auth, config

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("Dashboard")

conn = db.get_db()
cust_count, visit_count = db.stats(conn)
st.metric("Customers", cust_count)
st.metric("Visits", visit_count)

st.subheader("Customer List")
customers = db.all_customers_with_visits(conn)

# Display table
cols = ["Name"]
if config.SHOW_EMAILS:
    cols.append("Email")
cols += ["Identifier", "Total Visits", "Streak"]

table_data = []
for cid, name, email, identifier, visits in customers:
    streak, threshold = db.visit_progress(visits)
    row = [name]
    if config.SHOW_EMAILS:
        row.append(email)
    row += [identifier, visits, f"{streak}/{threshold}"]
    table_data.append(row)

df = pd.DataFrame(table_data, columns=cols)
st.table(df)

# Search feature
st.subheader("Search Customer")
query = st.text_input("Search by name, email, or code")
if query:
    results = db.search_customer(conn, query)
    if results:
        for cid, name, email, identifier, visits in results:
            streak, threshold = db.visit_progress(visits)
            st.write(f"**{name}** ({identifier})")
            if config.SHOW_EMAILS:
                st.write(f"Email: {email}")
            st.write(f"Total visits: {visits}")
            st.write(f"Current streak: {streak}/{threshold}")
            if streak == threshold:
                st.success("🎉 Reward available! 🎉")
    else:
        st.warning("No matching customer found.")

if st.button("Logout"):
    auth.logout()
