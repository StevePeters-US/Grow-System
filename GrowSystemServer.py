# Runs on a raspberry pi to control lights and read from sensors

import schedule
import time
import datetime
import atexit
import Adafruit_DHT

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

LED_PIN = 23
LIGHT_PIN = 25
PUMP_PIN = 12

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

lightOnTime = datetime.time(7, 0, 0)
lightOffTime = datetime.time(20, 0, 0)
lightOnDuration = 2

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)

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
    time.sleep(3)

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)

schedule.every().minute.at(":17").do(checkTime)
schedule.every().second.do(checkTemp)

def main():
    print('This is a server')

    while True:
        schedule.run_pending()
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)

if __name__ == "__main__":
    main()


