import streamlit as st
import register
import product
import bill

# Set wide mode and page configuration
st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide",  # Enable wide mode
    initial_sidebar_state="expanded"  # Optional: Start with sidebar expanded
)


# Main app logic
def main():
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

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Login"

    # Navigation between pages
    if st.session_state.current_page == "Login":
        register.login_page()
    elif st.session_state.current_page == "Register":
        register.register_page()
    elif st.session_state.current_page == "Dashboard":
        register.dashboard_page()
    elif st.session_state.current_page == "Product":
        product.product_page()
    elif st.session_state.current_page == "Bulk_Upload":
        product.bulk_upload_page()
    elif st.session_state.current_page == "Single_Product":
        product.single_product_page()
    elif st.session_state.current_page == "Category":
        product.product_page()
    elif st.session_state.current_page == "Billing":
        bill.billing_page()
    elif st.session_state.current_page == "Analytics":
        register.analytics_page()



if __name__ == "__main__":
    main()
