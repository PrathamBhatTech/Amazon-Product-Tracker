import sys
import streamlit as st

st.set_page_config(
    page_title="Login",
    page_icon=":lock:",
)

# import the database class
from OtherFunctions.SQL_Functions import Database

db = Database()

user = st.text_input('Username')
passwd = st.text_input('Password',type='password')
email = st.text_input('Email')
number = st.text_input('Phone Number')
checkfreq = st.text_input('Check Frequency')

if st.button('SignUp'):
    db.get_user_data(user, email, number, checkfreq)
    st.success("You have successfully created an account.Go to the Login Menu to login")