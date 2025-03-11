#push with 
#git push https://danigeos:<token>@github.com/danigeos/my-streamlit-app.git


import streamlit as st

st.title("Ejemplo de app para Streamlit")
st.write("Hecho en Python para Ignacio!")

user_input = st.text_input("Enter something:")
if user_input:
    st.write(f"You entered: {user_input}")
