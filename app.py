import streamlit as st
import sqlite3
import os

# DB path (same folder)
DB_PATH = os.path.join(os.path.dirname(__file__), "olx.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price TEXT,
                category TEXT,
                description TEXT,
                owner TEXT)''')

conn.commit()

# ---------------- FUNCTIONS ----------------
def add_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def add_product(name, price, category, description, owner):
    c.execute("INSERT INTO products (name, price, category, description, owner) VALUES (?,?,?,?,?)",
              (name, price, category, description, owner))
    conn.commit()

def view_products():
    c.execute("SELECT * FROM products")
    return c.fetchall()

def my_products(user):
    c.execute("SELECT * FROM products WHERE owner=?", (user,))
    return c.fetchall()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- UI ----------------
st.title("🛒 Mini OLX App")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# -------- REGISTER --------
if choice == "Register":
    st.subheader("Create Account")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type='password')

    if st.button("Register"):
        add_user(user, pwd)
        st.success("Account Created!")

# -------- LOGIN --------
elif choice == "Login":
    st.subheader("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type='password')

    if st.button("Login"):
        result = login_user(user, pwd)

        if result:
            st.session_state.user = user
            st.success(f"Welcome {user}")
        else:
            st.error("Invalid Login")

# -------- AFTER LOGIN --------
if st.session_state.user:

    st.sidebar.write(f"👤 {st.session_state.user}")

    page = st.sidebar.selectbox(
        "Select Page",
        ["Post Item", "View Items", "My Items", "Logout"]
    )

    # -------- POST ITEM --------
    if page == "Post Item":
        st.subheader("📤 Post New Item")

        pname = st.text_input("Product Name")
        price = st.text_input("Price")
        category = st.selectbox("Category", ["Electronics", "Vehicles", "Furniture"])
        desc = st.text_area("Description")

        if st.button("Post"):
            add_product(pname, price, category, desc, st.session_state.user)
            st.success("Item Posted Successfully!")

    # -------- VIEW ITEMS --------
    elif page == "View Items":
        st.subheader("📦 All Products")

        products = view_products()

        if products:
            for p in products:
                st.write(f"### 📦 {p[1]}")
                st.write(f"💰 Price: {p[2]}")
                st.write(f"📂 Category: {p[3]}")
                st.write(f"📝 {p[4]}")
                st.write(f"👤 Seller: {p[5]}")
                st.markdown("---")
        else:
            st.info("No products available")

    # -------- MY ITEMS --------
    elif page == "My Items":
        st.subheader("📌 My Products")

        products = my_products(st.session_state.user)

        if products:
            for p in products:
                st.write(f"### 📦 {p[1]}")
                st.write(f"💰 Price: {p[2]}")
                st.write(f"📂 Category: {p[3]}")
                st.write(f"📝 {p[4]}")
                st.markdown("---")
        else:
            st.info("You have not posted any items")

    # -------- LOGOUT --------
    elif page == "Logout":
        st.session_state.user = None
        st.success("Logged out successfully")