import streamlit as st
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
cols += ["Identifier", "Visits"]

table_data = []
for name, email, identifier, visits in customers:
    row = [name]
    if config.SHOW_EMAILS:
        row.append(email)
    row += [identifier, visits]
    table_data.append(row)

st.table(table_data)

# Search feature
st.subheader("Search Customer")
query = st.text_input("Search by name, email, or code")
if query:
    results = db.search_customer(conn, query)
    if results:
        for name, email, identifier, visits in results:
            st.write(f"**{name}** ({identifier})")
            if config.SHOW_EMAILS:
                st.write(f"Email: {email}")
            st.write(f"Visits: {visits}")
            if visits >= config.REWARD_VISITS:
                st.info("Reward available!")
    else:
        st.warning("No matching customer found.")

if st.button("Logout"):
    auth.logout()
