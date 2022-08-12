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


headerCon = st.container()
dataCon = st.container()
serverCon = st.container()

LEDState = False
ShutDownState  = False

PORT = 7892

with headerCon:
    st.title('Grow System Project')
    st.text('Connect to remote pi\'s')


with dataCon:

    st.write("Crop Type: Lettuce")

    sel_col, disp_col = st.columns(2)
    if sel_col.checkbox('Crop Data'):
        disp_col.write("Crop Type: Lettuce")
        disp_col.write("Seed Source: Burpee")
        disp_col.write("Seed Batch: 43526")

    if sel_col.checkbox('Hardware Description'):
        disp_col.write("Grow Space Type: Tent")
        disp_col.write("Grow Space Size: 4, 4, 6")
        disp_col.write("Light : Mars Hydro")

    if sel_col.checkbox("Events"):
        df = pd.DataFrame({
        'Date': [1, 2, 3, 4],
        'Event Description': ['Started Seeds',
        "Transferred seedlings to rockwool. Germination rate = 50%",
            '30',
            ' 40']
        })

        df

    if sel_col.checkbox('Environmental Data'):
        environmental_data = pd.DataFrame(
            np.random.randn(20, 4),
            columns=['Air Temperature C', 'Water Temperature', 'Humidity', 'VPD'])

        disp_col.line_chart(environmental_data)

    if sel_col.checkbox('Nutrient Data'):
        nut_data = pd.DataFrame(
            np.random.randn(20, 4),
            columns=['EC', 'Nitrogen', 'Potassium', 'Phosphorous'])

        disp_col.line_chart(nut_data)

    LEDState = st.checkbox('LED')

    if st.button('Shutdown'):
        st.write("Exit button pressed")
        ShutDownState = True
        exit()

# with serverCon:
#     async def echo():
#         async with websockets.connect("ws://192.168.0.117:7890") as websocket:
#             msg = { "LED" : LEDState, "Shutdown" : ShutDownState}
#             jsonMsg = json.dumps(msg)
#             await websocket.send(jsonMsg)
#             try:
#                 recmsg = await websocket.recv()
#                 print(recmsg)
#             except:
#                 print('reconnecting')
#                 websocket = await websockets.connect("ws://192.168.0.117:7890")

#     asyncio.run(echo())

async def echo(websocket, path):
    #print("A client just connected")
    try:
        async for message in websocket:

            inJson = json.loads(message)
            
            print("Received message from client: " + message)

           # toggleLight(inJson["LED"])

            if inJson["Shutdown"] == True:
                exit()

            await websocket.send("Pong: " + message)
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

async def main():
    async with websockets.serve(echo, "localhost", PORT):
        print("Server listening on Port " + str(PORT))
        await asyncio.Future()  # run forever


def init():
    print('This is a server')
    asyncio.run(main())

if __name__ == "__main__":
    init()

    # ws_server = websockets.serve(echo, "0.0.0.0", PORT)

    # asyncio.get_event_loop().run_until_complete(ws_server)
    # asyncio.get_event_loop().run_forever()

