import streamlit as st
from streamlit_card import card

st.title("Amazon Product Tracker")
left_column, right_column = st.columns(2)

def print(id, title, data):
    card(title=id, text=data)
