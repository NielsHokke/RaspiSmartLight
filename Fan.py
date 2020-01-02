import RPi.GPIO as GPIO
import time

# Strip Pins
FanSpeedLowPin = 21		# groen
FanSpeedMediumPin = 20	# geel
FanSpeedHighPin = 16	# rood

stopThreadFan = False


# Intialise GPIO
def setup():
	global stopThreadFan

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(FanSpeedLowPin, GPIO.OUT)
	GPIO.setup(FanSpeedMediumPin, GPIO.OUT)
	GPIO.setup(FanSpeedHighPin, GPIO.OUT)

	GPIO.output(FanSpeedLowPin, GPIO.HIGH)
	GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
	GPIO.output(FanSpeedHighPin, GPIO.HIGH)


# Called on exit
def cleanup():
	GPIO.output(FanSpeedLowPin, GPIO.HIGH)
	GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
	GPIO.output(FanSpeedHighPin, GPIO.HIGH)

	GPIO.cleanup()


def setFan(speed="low", minutes=30):
	global stopThreadFan
	stopThreadFan = False

	if "high" in speed:
		GPIO.output(FanSpeedLowPin, GPIO.HIGH)
		GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
		GPIO.output(FanSpeedHighPin, GPIO.LOW)
	elif "medium" in speed:
		GPIO.output(FanSpeedLowPin, GPIO.HIGH)
		GPIO.output(FanSpeedMediumPin, GPIO.LOW)
		GPIO.output(FanSpeedHighPin, GPIO.HIGH)
	elif "low" in speed:
		GPIO.output(FanSpeedLowPin, GPIO.LOW)
		GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
		GPIO.output(FanSpeedHighPin, GPIO.HIGH)
	else:
		print("ERROR: non valid fan speed setting!")
		return

	startTime = time.time()

	while startTime + minutes * 60 > time.time():
		if stopThreadFan:
			GPIO.output(FanSpeedLowPin, GPIO.HIGH)
			GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
			GPIO.output(FanSpeedHighPin, GPIO.HIGH)
			break
		time.sleep(5)

	GPIO.output(FanSpeedLowPin, GPIO.HIGH)
	GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
	GPIO.output(FanSpeedHighPin, GPIO.HIGH)

def setFanOff():
	global stopThreadFan
	stopThreadFan = False

	GPIO.output(FanSpeedLowPin, GPIO.HIGH)
	GPIO.output(FanSpeedMediumPin, GPIO.HIGH)
	GPIO.output(FanSpeedHighPin, GPIO.HIGH)

if __name__ == "__main__":
	print("Starting FanScript")
	setup()

	minutes = 1
	print(f"Fan in low speed for {minutes} minute(s)")
	setFan("low", minutes)

	cleanup()
	print("Clean exit!")
