import streamlit as st
import pandas as pd
import datetime
import bulk_entry  # Ensure this module is properly implemented

# Initialize session state for button clicks and navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Category"

if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "prod_name": "",
        "prod_id": "",
        "batch_id": "",
        "prod_rate": 0.0,
        "prod_mrp": 0.0,
        "prod_stock": 0
    }
if 'save_clicked' not in st.session_state:
    st.session_state.save_clicked = False
# Dashboard page
def dashboard_page():
    st.title("Dashboard")
    st.write("Welcome to the Dashboard!")
    if st.button("Go to Product Management"):
        st.session_state.current_page = "Dashboard"
        st.session_state.save_clicked = False

# Category page
def product_page():
    st.title("Product Management")
    col_bulk, col_single, col_dashboard = st.columns(3)

    if col_bulk.button("Bulk Upload"):
        #bulk_upload_page()
        st.session_state.current_page = "Bulk_Upload"

    if col_single.button("Single Product"):
        #single_product_page()
        st.session_state.current_page = "Single_Product"

    if col_dashboard.button("Back to Dashboard"):
        st.session_state.current_page = "Dashboard"


# Bulk upload page
def bulk_upload_page():
    st.title("Bulk Upload")
    try:
        bulk_entry.bulk_upload()  # Replace with actual bulk upload logic
    except AttributeError:
        st.error("Bulk upload module or function is not implemented.")

    if st.button("Back to Product Management"):
        st.session_state.current_page = "Category"
        #st.session_state.save_clicked = False

# Single product entry page
def single_product_page():
    st.title("Single Product Entry")
    with st.form("product_register"):
        prod_name = st.text_input("Enter a Product Name", value=st.session_state.form_data["prod_name"])
        prod_id = st.text_input("Enter a Product ID", value=st.session_state.form_data["prod_id"])
        batch_id = st.text_input("Enter a Batch ID", value=st.session_state.form_data["batch_id"])
        prod_rate = st.number_input("Enter a Product Rate", min_value=0.0, step=0.1, value=st.session_state.form_data["prod_rate"])
        prod_mrp = st.number_input("Enter a Product MRP", min_value=0.0, step=0.1, value=st.session_state.form_data["prod_mrp"])
        prod_stock = st.number_input("Enter Product Stock", min_value=0, step=1, format="%d", value=st.session_state.form_data["prod_stock"])

        # Save form data
        submit = st.form_submit_button("Save")
        if submit:
            if not prod_name or not prod_id:
                st.error("Product name and product ID cannot be empty.")
            elif prod_rate >= prod_mrp:
                st.error("Product rate must be less than MRP.")
            elif prod_stock == 0:
                st.error("Stock must be greater than zero.")
            else:
                entry(prod_name, prod_id, prod_rate, prod_mrp, prod_stock, batch_id)
                st.success(f"Product '{prod_name}' saved successfully!")
                st.session_state.form_data = {  # Reset form data
                    "prod_name": "",
                    "prod_id": "",
                    "batch_id": "",
                    "prod_rate": 0.0,
                    "prod_mrp": 0.0,
                    "prod_stock": 0
                }

    if st.button("Back to Product Management"):
        st.session_state.current_page = "Category"
        st.session_state.save_clicked = False

# Entry function to save product data
def entry(prod_name, prod_id, prod_rate, prod_mrp, prod_stock, batch_id):
    file_path = "C:\\Users\\dell\\vj\\invetory\\bill.csv"
    try:
        prod_df = pd.read_csv(file_path)
    except FileNotFoundError:
        prod_df = pd.DataFrame(columns=["prod_name", "prod_id", "batch_id", "prod_rate", "prod_mrp", "prod_stock", "date"])

    new_data = {
        "prod_name": [prod_name],
        "prod_id": [prod_id],
        "batch_id": [batch_id],
        "prod_rate": [prod_rate],
        "prod_mrp": [prod_mrp],
        "prod_stock": [prod_stock],
        "date": [datetime.datetime.now()]
    }
    prod_df = pd.concat([prod_df, pd.DataFrame(new_data)], ignore_index=True)
    prod_df.to_csv(file_path, index=False)

# Main application logic
def main():
    if st.session_state.current_page == "Category":
        product_page()
    elif st.session_state.current_page == "Bulk_Upload":
        bulk_upload_page()
    elif st.session_state.current_page == "Single_Product":
        single_product_page()
    elif st.session_state.current_page == "Dashboard":
        dashboard_page()

# Run the app
if __name__ == "__main__":
    main()
