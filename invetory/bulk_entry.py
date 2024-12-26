import streamlit as st
import pandas as pd
import datetime

def bulk_upload():
# File uploader for Excel/CSV
    data = st.file_uploader("Upload your Excel or CSV file:", type=['xlsx', 'csv'])

    if data:  # Proceed only if a file is uploaded
        file_type = data.name.split('.')[-1]
        st.write(f"Uploaded file type: {file_type.upper()}")

        if st.button("Upload"):
            try:
                # Read the uploaded file
                if file_type == 'xlsx':
                    prod_list = pd.read_excel(data)
                elif file_type == 'csv':
                    prod_list = pd.read_csv(data)
                else:
                    st.error("Unsupported file type.")
                    st.stop()

                # Read the existing CSV
                try:
                    prod_df = pd.read_csv("data\\bill.csv")
                except FileNotFoundError:
                    st.warning("Existing bill file not found. Creating a new one.")
                    prod_df = pd.DataFrame(columns=["prod_name", "prod_id", "batch_id", "prod_rate", "prod_mrp", "prod_stock", "date"])

                # Ensure required columns exist in uploaded data
                required_columns = ["prod_name", "prod_id", "batch_id", "prod_rate", "prod_mrp", "prod_stock"]
                if not all(col in prod_list.columns for col in required_columns):
                    st.error(f"Uploaded file must contain the following columns: {', '.join(required_columns)}")
                    st.stop()

                # Add timestamp to the uploaded data
                prod_list['date'] = datetime.datetime.now()

                # Insert new data next to the last inserted row
                # Concatenate new data to the bottom of the existing DataFrame
                prod_df = pd.concat([prod_df, prod_list[required_columns + ['date']]], ignore_index=True)

                # Save to the same CSV
                prod_df.to_csv("C:\\Users\\dell\\vj\\invetory\\bill.csv", index=False)

                # Display success and updated DataFrame
                st.success("Products uploaded and inserted successfully!")
                st.write(prod_df)

            except Exception as e:
                st.error(f"An error occurred: {e}")

bulk_upload()
