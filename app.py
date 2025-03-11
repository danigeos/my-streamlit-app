import streamlit as st

st.title("My Simple Python Web App")
st.write("This is a web-based app running Python!")

user_input = st.text_input("Enter something:")
if user_input:
    st.write(f"You entered: {user_input}")
