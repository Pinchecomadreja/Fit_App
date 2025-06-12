#to render website in terminal do:
#python -m streamlit run main.py
import streamlit as st 
import pandas as pd


#import matplotlib.pyplot as plt
#import numpy as np

#fig, ax = plt.subplots()             # Create a figure containing a single Axes.
#ax.plot(semana,peso)  # Plot some data on the Axes.
#plt.show()   

st.title("FIT APP")
st.write("Nuestra app de ensueño para deportistas")
st.image("unosmates.png",width=300)



if "attendance" not in st.session_state:
    st.session_state.attendance = set()


def take_attendance():
    if st.session_state.name in st.session_state.attendance:
        st.info(f"{st.session_state.name} has already been counted.")
        st.info(f"{st.session_state.age} has already been counted.")
    else:
        st.session_state.attendance.add(st.session_state.name)
        st.session_state.attendance.add(st.session_state.age)


with st.form(key="my_form"):
    st.text_input("Name", key="name")
    st.text_input("Age", key="age")
    st.form_submit_button("I'm here!", on_click=take_attendance)
    