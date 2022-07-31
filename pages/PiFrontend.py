import streamlit as st

st.write("Pi Server Name: Potato")

piip = st.slider('Pick a number', 0, 255)
st.write("Pi IP: 192.168.0.{}".format(piip))