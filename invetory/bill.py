import streamlit as st
import pandas as pd
import datetime

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_products" not in st.session_state:
    st.session_state.show_products = False  # Control visibility of the products table
    st.write("Initialized show_products in session state.")



# Load product data
def load_products():
    try:
        return pd.read_csv("C:\\Users\\dell\\vj\\invetory\\bill.csv")  # Adjust the path as needed
    except FileNotFoundError:
        st.error("Product file not found. Please ensure 'bill.csv' exists in the specified directory.")
        return pd.DataFrame(columns=["prod_id", "prod_name", "prod_rate", "prod_stock"])

# Save the bill to CSV
def save_bill(cart):
    bill_path = "C:\\Users\\dell\\vj\\invetory\\bills.csv"  # Adjust the path as needed
    try:
        existing_data = pd.read_csv(bill_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Append new bill items
    new_bill_df = pd.DataFrame(cart)
    result_df = pd.concat([existing_data, new_bill_df], ignore_index=True)
    result_df.to_csv(bill_path, index=False)

    st.success("Bill saved successfully!")

# Inject custom CSS for styling
def set_custom_css():
    st.markdown(
        """
        <style>
        h1, h2, h3 {
            text-align: center;
            color: #4CAF50;
        }
        .container-box {
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            background-color: #f9f9f9;
            margin-bottom: 1.5rem;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Main billing page
def billing_page():
    set_custom_css()

    st.title("Billing")

    # Available Products Section
    with st.container():
        #st.subheader("Available Products")
        if st.button("Available Products"):
            st.session_state.show_products = True
            st.write("Show Products button clicked. State updated.")
            if st.session_state.show_products:
                products = load_products()
                if not products.empty:
                    st.dataframe(products[["prod_id", "prod_name", "prod_rate", "prod_stock"]])
                    if st.button("Hide Products"):
                        st.session_state.show_products = False
            else:
                st.warning("No products available. Please upload a valid 'bill.csv' file.")

    # Add to Cart and Cart Sections
    with st.container():
        # Adjust column width: Cart section is wider
        col1,col2, col3 = st.columns([1,0.1, 2])

        # Add to Cart Section
        with col1:
            st.subheader("Add to Cart")
            with st.form("add_to_cart_form", clear_on_submit=True):
                products = load_products()
                if products.empty:
                    st.warning("No products available to add to cart.")
                    return

                product_id = st.selectbox(
                    "Select Product",
                    options=products["prod_id"].tolist(),
                    format_func=lambda x: products.loc[products["prod_id"] == x, "prod_name"].values[0],
                )
                quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
                add_to_cart = st.form_submit_button("Add to Cart")

                if add_to_cart:
                    product = products.loc[products["prod_id"] == product_id].iloc[0]
                    existing_item = next((item for item in st.session_state.cart if item["prod_id"] == product_id), None)
                    if existing_item:
                        existing_item["quantity"] += quantity
                        existing_item["total_price"] = existing_item["quantity"] * existing_item["prod_rate"]
                        st.success(f"Updated quantity for {product['prod_name']}. New quantity: {existing_item['quantity']}.")
                    else:
                        st.session_state.cart.append({
                            "prod_id": product["prod_id"],
                            "prod_name": product["prod_name"],
                            "prod_rate": product["prod_rate"],
                            "quantity": quantity,
                            "total_price": product["prod_rate"] * quantity,
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        })
                        st.success(f"Added {quantity} x {product['prod_name']} to cart.")

        # Cart Section (Wider Column)
        with col2:
            st.write(" ")
        with col3:
            st.subheader("Cart")
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)

                # Editable quantities for each item in the cart
                for index, item in enumerate(st.session_state.cart):
                    col_name, col_quantity, col_rate, col_remove = st.columns([3, 2, 2, 1])
                    col_name.write(f"**{item['prod_name']}**")
                    new_quantity = col_quantity.number_input(
                        "",
                        min_value=1,
                        value=item["quantity"],
                        step=1,
                        key=f"quantity_{index}",
                    )
                    col_rate.write(f"₹{item['prod_rate'] * new_quantity:.2f}")
                    if col_remove.button("Remove", key=f"remove_{index}"):
                        st.session_state.cart.pop(index)
                        st.success(f"Removed {item['prod_name']} from cart.")
                        break  # Avoid rendering issues

                    # Update quantity and total price
                    if new_quantity != item["quantity"]:
                        item["quantity"] = new_quantity
                        item["total_price"] = new_quantity * item["prod_rate"]

                # Grand Total
                grand_total = sum(item["total_price"] for item in st.session_state.cart)
                st.write(f"**Grand Total: ₹{grand_total:.2f}**")

                # Save Bill Button
                if st.button("Save Bill"):
                    save_bill(st.session_state.cart)
                    st.session_state.cart = []  # Clear the cart after saving
            else:
                st.write("Your cart is empty.")

# Main app logic
def main():
    billing_page()

if __name__ == "__main__":
    main()
