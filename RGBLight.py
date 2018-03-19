import time
from neopixel import *
from PIL import Image
import MainLight


# LED strip configuration:
LED_COUNT = 240  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering WS2811_STRIP_GRB

# Strip object
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

# Thread variable
stopThreadRGB = False

# Fade Variables
StepsPerSec = 100

tempOn = True
middenTemp = 255
rechtsTemp = 255
linksbovenTemp = 255

def setup():
	global strip
	strip.begin()

# Called on exit
def cleanup():
	setColor(Color(0,0,0))

def setColor(color):
	global strip
	global tempOn
	tempOn = False

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()


# Define functions which animate LEDs in various ways.
def colorWipe(color, wait_ms=50):
	global strip
	global tempOn
	tempOn = False

	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms / 1000.0)


def theaterChase(color, wait_ms=50, iterations=10):
	global strip
	global tempOn
	tempOn = False

	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, color)
			strip.show()
			time.sleep(wait_ms / 1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, 0)


def rainbow(wait_ms=20, iterations=1):
	global strip
	global tempOn
	tempOn = False

	for j in range(256 * iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i + j) & 255))
		strip.show()
		time.sleep(wait_ms / 1000.0)


def rainbowCycle(wait_ms=20, iterations=5):
	global strip
	global tempOn
	tempOn = False

	for j in range(256 * iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(wait_ms=50):
	global strip
	global tempOn
	tempOn = False

	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, wheel((i + j) % 255))
			strip.show()
			time.sleep(wait_ms / 1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, 0)


def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)


def playImage(imagename, wait_ms=10):
	global strip
	global tempOn
	tempOn = False

	im = Image.open("animations/" + imagename)
	rgb_im = im.convert('RGB')
	width, height = im.size

	for j in range(height):
		for i in range(strip.numPixels()):
			r, g, b = rgb_im.getpixel((i, j))
			strip.setPixelColor(i, Color(r, g, b))
		strip.show()
		time.sleep(wait_ms / 1000.0)


def tempToColor(temp, fade):
	corection = 1 - 0.01568652 * temp + 0.00006151575 * temp**2
	return Color(int((temp/100.0)*fade*corection), 0, int(((255 - temp)/100.0)*fade*corection))


def setMtemp(fade):
	global strip
	if tempOn:
		for i in range(61, 177):
			strip.setPixelColor(i, tempToColor(middenTemp, fade))
		strip.show()


def setRtemp(fade):
	global strip
	if tempOn:
		for i in range(0, 60):
			strip.setPixelColor(i, tempToColor(rechtsTemp, fade))
		strip.show()


def setLBtemp(fade):
	global strip
	if tempOn:
		for i in range(177, strip.numPixels()):
			strip.setPixelColor(i, tempToColor(linksbovenTemp, fade))
		strip.show()


def setTemp(temp):
	global middenTemp
	global rechtsTemp
	global linksbovenTemp

	global tempOn

	middenTemp = temp
	rechtsTemp = temp
	linksbovenTemp = temp

	tempOn = True

	status = MainLight.status()

	setMtemp(status['Midden'])
	setRtemp(status['Rechts'])
	setLBtemp(status['LinksBoven'])


# def fadeToTemp(M, R, LB, LO, tempf, tempt, TotalTime):
# 	global strip
#
# 	TotalSteps = int(StepsPerSec * TotalTime)
# 	if TotalSteps == 0: TotalSteps = 1
# 	TimeStep = (TotalTime * 1.0) / TotalSteps
#
# 	tempStep = (tempt - tempf * 1.0) / TotalSteps
#
# 	for j in range(0, TotalSteps):
# 		if M:
# 			for i in range(61, 177):
# 				strip.setPixelColor(i, tempToColor(tempt, (j/TotalSteps) * 100))
# 		if R:
# 			for i in range(60):
# 				strip.setPixelColor(i, tempToColor(tempt, (j/TotalSteps) * 100))
# 		if LB:
# 			for i in range(178, strip.numPixels()):
# 				strip.setPixelColor(i, tempToColor(tempt, (j/TotalSteps) * 100))
#
#
#
#
# 		for i in range(strip.numPixels()):
#
# 		strip.show()
#
#
# 		time.sleep(TimeStep)





# setup()
#
# try:
# 	while True:
# 		# colorWipe(Color(255, 0, 0), 10)  # Red wipe
# 		# colorWipe(Color(0, 255, 0), 10)  # Green wipe
# 		# colorWipe(Color(0, 0, 255), 10)  # Blue wipe
#
# 		# theaterChase(Color(255, 0, 0), 50)  # Red theaterChase
# 		# theaterChase(Color(0, 255, 0), 50)  # Green theaterChase
# 		# theaterChase(Color(0, 0, 255), 50)  # Blue theaterChase
#
# 		# rainbow(10)
#
# 		# rainbowCycle(10)
#
# 		# theaterChaseRainbow(50)
#
# 		playImage('dubbelwave.png')
# 		pass
#
#
# except KeyboardInterrupt:
# 	pass
#
# print "clean exit!"
# setColor(Color(0, 0, 0))