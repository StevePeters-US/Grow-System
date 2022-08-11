# Uses Streamlit as a frontend

from operator import truediv
from unicodedata import name
import streamlit as st
import pandas as pd
import numpy as np
import websockets
import asyncio
import json
import sys


LEDState = False
ShutDownState  = False



st.write("Crop Type: Lettuce")

if st.checkbox('Crop Data'):
    st.write("Crop Type: Lettuce")
    st.write("Seed Source: Burpee")
    st.write("Seed Batch: 43526")

if st.checkbox('Hardware Description'):
    st.write("Grow Space Type: Tent")
    st.write("Grow Space Size: 4, 4, 6")
    st.write("Light : Mars Hydro")

if st.checkbox("Events"):
    df = pd.DataFrame({
    'Date': [1, 2, 3, 4],
    'Event Description': ['Started Seeds',
    "Transferred seedlings to rockwool. Germination rate = 50%",
        '30',
        ' 40']
    })

    df

if st.checkbox('Environmental Data'):
    environmental_data = pd.DataFrame(
        np.random.randn(20, 4),
        columns=['Air Temperature C', 'Water Temperature', 'Humidity', 'VPD'])

    st.line_chart(environmental_data)

if st.checkbox('Nutrient Data'):
    nut_data = pd.DataFrame(
        np.random.randn(20, 4),
        columns=['EC', 'Nitrogen', 'Potassium', 'Phosphorous'])

    st.line_chart(nut_data)

LEDState = st.checkbox('LED')

if st.button('Shutdown'):
     st.write("Exit button pressed")
     ShutDownState = True


async def echo():
    async with websockets.connect("ws://192.168.0.117:7890") as websocket:
        msg = { "LED" : LEDState, "Shutdown" : ShutDownState}
        jsonMsg = json.dumps(msg)
        await websocket.send(jsonMsg)
        await websocket.recv()

asyncio.run(echo())