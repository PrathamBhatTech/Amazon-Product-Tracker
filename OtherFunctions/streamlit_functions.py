import streamlit as st
from OtherFunctions.SQL_Functions import Database 

db = Database()

st.title("Amazon Product Tracker")
left_column, right_column = st.columns(2)

products = []

options = None

def print(id, title, data):
    products.append(f'Product ID:{id}\n{title}\n{data}')
    # left_column.text(f'Product ID:{id}\n+{title}+{data}')

def complete():
    global options
    options = left_column.checkbox(label='Products Tracked', options=products)

def add_product():
    db.get_product_params(link, maxPrice)

def remove_products(options):
    if options is not None:
        for option in options:
            db.remove_product(option)

link = right_column.text_input("Add Product link")
maxPrice = right_column.number_input("Max Price", 0, 100000, 10000)
right_column.button("Add Product", on_click=add_product)

right_column.button("Remove Product", on_click=remove_products(options))

