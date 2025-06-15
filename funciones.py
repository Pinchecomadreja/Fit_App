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
            datos=dict(json.load(archivo))
            key=datos.keys()
            value=datos.values()

            if apellido in key and password in value:
                st.session_state.login = True
                st.success("Bienvenido al usuario " + apellido)
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            st.error("No se ha podido registrarse")
            pass


def registrar(apellido,password):
    st.session_state.registrar = True
    datos [apellido]=password

    try:
        with open("datos_usuarios.json","a") as archivo:
            json.dump(datos,archivo)
            st.success("Registro Exitoso")
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        st.error("ALGO SALIO MAL")
        return




