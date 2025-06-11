#to render website in terminal do:
#python -m streamlit run main.py
import streamlit as st 

st.title("FIT APP")
st.write("Nuestra app de ensueño para deportistas")
st.image("unosmates.png",width=300)

with st.form(key="ingreso"):
    name = st.text_input("Usuario",key="user")
    password = st.text_input("Contraseña",key="password")
    log = st.form_submit_button("Login", on_click=Enviar)
    