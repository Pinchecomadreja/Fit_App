import streamlit as st
from xlwings.mistune import markdown

import funciones as fn
import clases

def hacer_login():
    fn.login(apellido,password)
def hacer_registro():
    fn.registrar(apellido,password)
def page_registro():
    st.switch_page("pages/RegistroPagina_1.py")

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
if st.button("Registrarse"):
    st.switch_page("pages/RegistroPagina_1.py")

