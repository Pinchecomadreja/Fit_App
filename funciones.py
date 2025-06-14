import json
import streamlit as st
datos = {}

if "login" not in st.session_state:
    st.session_state.login = False


if "registrar" not in st.session_state:
    st.session_state.registrar = False

def login(apellido,password):
    with open("datos_usuarios.json","r") as archivo:
        try:
            datos=json.load(archivo)
            if password in datos and apellido in datos[password]:
                st.session_state.login = True
                st.success("Bienvenido al usuario " + apellido)
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            pass


def registrar(apellido,password):
    st.session_state.registrar = True
    bandera=False
    datos [apellido]=password
    try:
        with open("datos_usuarios.json","a") as archivo:
            json.dump(datos,archivo)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        st.error("ALGO SALIO MAL")
        bandera=True
        return
    if bandera:
        st.error("ALGO SALIO MAL")





