import streamlit as st
import funciones as fn
import clases
from funciones import crear_usuario, guardar, personas

with st.form("Formulario de registro"):
    st.write("Formulario de registro")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    edad=st.number_input("Edad")
    password = st.text_input("<PASSWORD>")
    nacimiento = st.text_input("Nacimiento")

    if st.form_submit_button("Enviar"):
        fn.crear_usuario(nombre,apellido,edad,password,nacimiento)
