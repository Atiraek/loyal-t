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
cols += ["ID", "Total Visits", "Streak"]

table_data = []
for cid, name, email, identifier, visits in customers:
    streak, threshold = db.visit_progress(visits)
    row = [name]
    if config.SHOW_EMAILS:
        row.append(email)
    row += [identifier, visits, f"{streak}/{threshold}"]
    table_data.append(row)

df = pd.DataFrame(table_data, columns=cols)

# Search feature
query = st.text_input("Search by name, email, or code.\n\n_[click outside to apply]_")
if query:
    query_lower = query.lower()
    df = df[df.apply(lambda row:
        query_lower in str(row["Name"]).lower() or
        query_lower in str(row["Email"]).lower() or
        query_lower in str(row["ID"]).lower(),
        axis=1
    )]

# Show filtered table
if config.SHOW_EMAILS:
    st.dataframe(df, hide_index=True)
else:
    st.dataframe(df.drop(columns=["Email"]), hide_index=True)

if st.button("Logout"):
    auth.logout()
