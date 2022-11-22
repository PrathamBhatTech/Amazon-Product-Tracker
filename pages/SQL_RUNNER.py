import streamlit as st
st.set_page_config(
    page_title="SQL Runner",
    page_icon=":lock:",
)

# import the database class
from OtherFunctions.SQL_Functions import Database

import pandas as pd

db = Database()

query = st.text_area("SQL Query", height=200)

if st.button('Run Query'):
    res = db.run_query(query)
    df = pd.DataFrame(res)
    st.write(df)