import sqlite3, uuid
from modules import config

def get_db():
    conn = sqlite3.connect(config.DB_PATH)
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

def add_customer(conn, name, email, identifier):
    cid = str(uuid.uuid4())
    conn.execute("INSERT INTO customers (id,name,email,identifier) VALUES (?,?,?,?)",
                 (cid, name, email, identifier))
    conn.commit()
    return cid

def get_customer_by_identifier(conn, identifier):
    return conn.execute("SELECT id,name,email FROM customers WHERE identifier=?", (identifier,)).fetchone()

def record_visit(conn, customer_id):
    conn.execute("INSERT INTO visits (id,customer_id) VALUES (?,?)",(str(uuid.uuid4()), customer_id))
    conn.commit()
    return conn.execute("SELECT COUNT(*) FROM visits WHERE customer_id=?", (customer_id,)).fetchone()[0]

def stats(conn):
    cust_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    visit_count = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    return cust_count, visit_count

def all_customers_with_visits(conn):
    return conn.execute("""
        SELECT c.name, c.email, c.identifier, COUNT(v.id) as visits
        FROM customers c
        LEFT JOIN visits v ON c.id = v.customer_id
        GROUP BY c.id
        ORDER BY visits DESC
    """).fetchall()

def search_customer(conn, query):
    return conn.execute("""
        SELECT c.name, c.email, c.identifier, COUNT(v.id) as visits
        FROM customers c
        LEFT JOIN visits v ON c.id = v.customer_id
        WHERE c.name LIKE ? OR c.email LIKE ? OR c.identifier LIKE ?
        GROUP BY c.id
    """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
