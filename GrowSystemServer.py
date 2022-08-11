# Runs on a raspberry pi to control lights and read from sensors

import schedule
import time
import datetime
import atexit
import Adafruit_DHT
import websockets
import asyncio
import json

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

LED_PIN = 23
LIGHT_PIN = 25
PUMP_PIN = 12

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

PORT = 7890

lightOnTime = datetime.time(7, 0, 0)
lightOffTime = datetime.time(20, 0, 0)
lightOnDuration = 2

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)

def toggleLight(lightOn):
    if lightOn:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

def checkTime():
	now = datetime.datetime.now().time()
	print("Checking Time. Current time = " + str(now))
	if now > lightOnTime and now < lightOffTime:
		GPIO.output(LIGHT_PIN, GPIO.HIGH)
		print("Light On")
	else:
		GPIO.output(LIGHT_PIN, GPIO.LOW)
		print("Light Off")

def checkTemp():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure, check wiring")
    #time.sleep(3)

def OnExit():
    print("Exiting Python server")
    GPIO.cleanup()

def exitServer(websocket):
    print("Closing server")
    websocket.close()
    exit()

async def echo(websocket, path):
    print("A client just connected")
    try:
        async for message in websocket:

            inJson = json.loads(message)
            
            print("Received message from client: " + message)

            toggleLight(inJson["LED"])
            if inJson["Shutdown"] == "true":
                exitServer(websocket)

            # if inJson["moveUp"] == True:
            #     moveLeftMotor(1)
            #     moveRightMotor(1)

            # elif inJson["moveDown"] == True:
            #     moveLeftMotor(-1)
            #     moveRightMotor(-1)

            # elif inJson["moveLeft"] == True:
            #     moveLeftMotor(-1)
            #     moveRightMotor(1)

            # elif inJson["moveRight"] == True:
            #     moveLeftMotor(1)
            #     moveRightMotor(-1)

            # else:
            #     moveLeftMotor(0)
            #     moveRightMotor(0)

            await websocket.send("Pong: " + message)
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

atexit.register(OnExit)

schedule.every().minute.at(":17").do(checkTime)
schedule.every().second.do(checkTemp)

def init():
    print('This is a server')

if __name__ == "__main__":
    init()

    start_server = websockets.serve(echo, "192.168.0.117", PORT)
    print("Server listening on Port " + str(PORT))

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


