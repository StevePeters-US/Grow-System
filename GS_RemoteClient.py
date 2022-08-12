import websockets
import asyncio
import json

LEDState = False
ShutDownState  = False

async def echo():
    async with websockets.connect("ws://0.0.0.0:7890") as websocket:
        msg = { "LED" : LEDState, "Shutdown" : ShutDownState}
        jsonMsg = json.dumps(msg)
        await websocket.send(jsonMsg)
        try:
            recmsg = await websocket.recv()
            print(recmsg)
        except:
            print('reconnecting')
            websocket = await websockets.connect("ws://0.0.0.0:7890")

asyncio.run(echo())