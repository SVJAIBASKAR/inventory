import streamlit as st
import pandas as pd
import bcrypt
import yaml
import datetime
import product
import bill

# YAML functions for user data
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# Password hashing
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(input_password, stored_hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

# Initialize session states
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "prod_name": "", "prod_id": "", "batch_id": "", "prod_rate": 0.0, "prod_mrp": 0.0, "prod_stock": 0
    }
    if 'save_clicked' not in st.session_state:
        st.session_state.save_clicked = False

# Pages
def login_page():
    st.title("Login")
    yaml_file = "users.yaml"
    user_data = load_yaml(yaml_file)

    if not st.session_state.logged_in:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        if login_button:
            if username in user_data:
                if verify_password(password, user_data[username]['password']):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.current_page = "Dashboard"
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Incorrect password.")
            else:
                st.error("Username not found.")

    if st.button("Register"):
        st.session_state.current_page = "Register"

def register_page():
    st.title("Register")
    yaml_file = "users.yaml"
    user_data = load_yaml(yaml_file)

    with st.form("register_form"):
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        register_button = st.form_submit_button("Register")

    if register_button:
        if username and password:
            if username in user_data:
                st.error("Username already exists.")
            else:
                user_data[username] = {"password": hash_password(password)}
                write_yaml(user_data, yaml_file)
                st.success("Registration successful. Please log in.")
                st.session_state.current_page = "Login"
        else:
            st.error("Please fill in all fields.")

def dashboard_page():
    st.title("Dashboard")
    col1, col2, col3 = st.columns(3)
    if col1.button("Product"):
        st.session_state.current_page = "Product"
    if col2.button("Billing"):
        st.session_state.current_page = "Billing"
    if col3.button("Analytics"):
        st.session_state.current_page = "Analytics"



def analytics_page():
    st.title("Analytics")
    st.write("Analytics coming soon...")
    if st.button("Back to Dashboard"):
        st.session_state.current_page = "Dashboard"


# Main app logic
def main():
    if st.session_state.current_page == "Login":
        login_page()
    elif st.session_state.current_page == "Register":
        register_page()
    elif st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "Product":
        product.product_page()
    elif st.session_state.current_page == "Billing":
        bill.billing_page()
    elif st.session_state.current_page == "Analytics":
        analytics_page()

if __name__ == "__main__":
    main()
