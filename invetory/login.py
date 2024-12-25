import streamlit as st
import bcrypt
import yaml
import product

# Function to load YAML data
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}

# Function to write YAML data
def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# Function to hash passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Function to verify passwords
def verify_password(input_password, stored_hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

# YAML file path
yaml_file = "users.yaml"

# Load existing user data
user_data = load_yaml(yaml_file)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"

# Function to display registration page
def register_page():
    st.title("Register")
    with st.form("register_form"):
        username = st.text_input("Enter a username")
        password = st.text_input("Enter a password", type="password")
        submit = st.form_submit_button("Register")

    if submit:
        if username and password:
            if username in user_data:
                st.error("Username already exists. Please choose another.")
            else:
                hashed_password = hash_password(password)
                user_data[username] = {"password": hashed_password}
                write_yaml(user_data, yaml_file)
                st.success("Registration successful! You can now log in.")
        else:
            st.error("Please fill in all fields.")

# Function to display login page
def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        if username in user_data:
            stored_hashed_password = user_data[username]['password']
            if verify_password(password, stored_hashed_password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")



            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.error("Username not found. Please register first.")

# Main application
if not st.session_state.logged_in:
    st.title("Welcome to the App")

    # Page navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.current_page = "Login"
    with col2:
        if st.button("Register"):
            st.session_state.current_page = "Register"

    # Show selected page
    if st.session_state.current_page == "Login":
        login_page()
    elif st.session_state.current_page == "Register":
        register_page()
else:
    st.title(f"Welcome, {st.session_state.username}!")
    st.write("You are now logged in.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.current_page = "Login"
        #st.experimental_rerun()
