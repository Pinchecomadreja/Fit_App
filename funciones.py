import json
import streamlit as st
from altair import value

from clases import Usuario

personas = {}
datos={}
diccionario={}
if "login" not in st.session_state:
    st.session_state.login = False


if "registrar" not in st.session_state:
    st.session_state.registrar = False

def login(nombre,apellido,password):

    with open("datos_usuarios.json", "r") as archivo:
        try:
            datos=dict(json.load(archivo))
            diccionario=datos.get(nombre+apellido)
            value=diccionario.values()
            key=diccionario.keys()
            print(f"{diccionario}\n {value}\n {key}")
            if apellido in key and password in value:
                st.session_state.login = True
                st.success("Bienvenido al usuario " + apellido)

        except (FileNotFoundError,json.decoder.JSONDecodeError):
            st.error("No se ha podido registrarse")
            pass


def guardar(personas):

    try:
        with open("datos_usuarios.json", "a") as archivo:
            json.dump(personas,archivo)
            st.success("Registro Exitoso")
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        st.error("ALGO SALIO MAL")
        return

def crear_usuario( nombre, apellido, edad,password,naciemiento):
    nueva_persona=Usuario( nombre, apellido, edad,password,naciemiento)
    personas={nombre+apellido:nueva_persona.a_dic()}
    st.success("Usuario Creado")
    guardar(personas)

