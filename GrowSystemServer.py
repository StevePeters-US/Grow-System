# Runs on a raspberry pi to control lights and read from sensors

import schedule
import time
import datetime
import atexit

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

LED_PIN = 23
LIGHT_PIN = 25
PUMP_PIN = 12

lightOnTime = datetime.time(7, 0, 0)
lightOffTime = datetime.time(20, 0, 0)
lightOnDuration = 2

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

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)

schedule.every().minute.at(":17").do(checkTime)

def main():
    print('This is a server')
    GPIO.cleanup()

    while True:
        schedule.run_pending()
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)

if __name__ == "__main__":
    main()


