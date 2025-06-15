import streamlit as st
import funciones as fn

def hacer_login():
    fn.login(apellido,password)
def hacer_registro():
    fn.registrar(apellido,password)


st.set_page_config(
    page_title="Bienveido/a",
    page_icon="👋",
)
st.title("FIT APP")
st.write("Nuestra app de ensueño para deportistas")
#registrar
apellido=st.text_input("Apellido")
password=st.text_input("PASSWORD", type="password")

st.button("Log In",on_click=hacer_login)
st.button("Registrarse", on_click=hacer_registro)

