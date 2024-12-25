import streamlit as st

options = ["Apple", "Banana", "Cherry", "Date"]

# Multiselect allows typing to search
selected_options = st.multiselect("Choose fruits", options)

st.write(f"You selected: {selected_options}")
