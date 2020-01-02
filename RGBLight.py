import time
import board
import neopixel
from PIL import Image
import MainLight


# # LED strip configuration:
# LED_COUNT = 240  # Number of LED pixels.
# LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# # LED_PIN = 10  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
# LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA = 10  # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
# LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering WS2811_STRIP_GRB

# Strip object
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

pixel_pin = board.D18
num_pixels = 240
strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# Thread variable
stopThreadRGB = False

# Fade Variables
StepsPerSec = 100

tempOn = False
middenTemp = 127
rechtsTemp = 127
linksbovenTemp = 127

lastColor = (0, 0, 0)

def setup():
    global strip
    # strip.begin()
    setColor((0, 0, 0))

# Called on exit
def cleanup():
    setColor((0, 0, 0))


def mapColor(Cfrom, Cto, step, totalSteps):

    Rf, Gf, Bf = Cfrom
    Rt, Gt, Bt = Cto

    R = int((step - 0) * (Rt - Rf) / (totalSteps - 0) + Rf)
    G = int((step - 0) * (Gt - Gf) / (totalSteps - 0) + Gf)
    B = int((step - 0) * (Bt - Bf) / (totalSteps - 0) + Bf)

    return (R, G, B)


def setColor(color):
    global strip
    global tempOn
    global lastColor
    tempOn = False

    strip.fill(color)
    strip.show()

    # for i in range(num_pixels):
    #     strip[i] = color
    # strip.show()

    lastColor = color


def fadeToColor(color, TotalTime, thread=False):
    global strip
    global lastColor
    global stopThreadRGB
    global tempOn
    tempOn = False
    stopThreadRGB = False

    TotalSteps = int(StepsPerSec * TotalTime)
    if TotalSteps == 0: TotalSteps = 1
    TimeStep = (TotalTime * 1.0) / TotalSteps

    for j in range(0, TotalSteps):
        c = mapColor(lastColor, color, j, TotalSteps)

        for i in range(num_pixels):
            strip[i] = c
        strip.show()

        if stopThreadRGB and thread:
            lastColor = c
            return

        time.sleep(TimeStep)

    lastColor = c


# Define functions which animate LEDs in various ways.
def colorWipe(color, wait_ms=50):
    global strip
    global tempOn
    tempOn = False

    for i in range(num_pixels):
        strip[i] = color
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(color, wait_ms=50, iterations=10):
    global strip
    global tempOn
    tempOn = False

    for j in range(iterations):
        for q in range(3):
            for i in range(0, num_pixels, 3):
                strip[i + q] = color
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, num_pixels, 3):
                strip[i + q] = (0, 0, 0)


def rainbow(wait_ms=20, iterations=1):
    global strip
    global tempOn
    tempOn = False

    for j in range(256 * iterations):
        for i in range(num_pixels):
            strip[i] = wheel((i + j) & 255)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(wait_ms=20, iterations=5, thread=False):
    global stopThreadRGB
    stopThreadRGB = False
    global strip
    global tempOn
    tempOn = False

    while True:
        for j in range(256 * iterations):
            for i in range(num_pixels):
                strip[i] = wheel((int(i * 256 / num_pixels) + j) & 255)
            strip.show()
            if stopThreadRGB and thread:
                return
            time.sleep(wait_ms / 1000.0)

        if not thread:
            break


def theaterChaseRainbow(wait_ms=50):
    global strip
    global tempOn
    tempOn = False

    for j in range(256):
        for q in range(3):
            for i in range(0, num_pixels, 3):
                strip[i + q] = wheel((i + j) % 255)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, num_pixels, 3):
                strip[i + q] = (0, 0, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def playImage(imagename, wait_ms=10):
    global strip
    global tempOn
    tempOn = False

    im = Image.open("animations/" + imagename)
    rgb_im = im.convert('RGB')
    width, height = im.size

    for j in range(height):
        for i in range(num_pixels):
            r, g, b = rgb_im.getpixel((i, j))
            strip[i] = (r, g, b)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def tempToColor(temp, fade):
    corection = 1 - 0.01568652 * temp + 0.00006151575 * temp**2
    return (int((temp/100.0)*fade*corection), 0, int(((255 - temp)/100.0)*fade*corection))


def setMtemp(fade):
    global strip
    if tempOn:
        for i in range(60, 177):
            strip[i] = tempToColor(middenTemp, fade)
        strip.show()


def setRtemp(fade):
    global strip
    if tempOn:
        for i in range(0, 60):
            strip[i] = tempToColor(rechtsTemp, fade)
        strip.show()


def setLBtemp(fade):
    global strip
    if tempOn:
        for i in range(177, num_pixels):
            strip[i] = tempToColor(linksbovenTemp, fade)
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

# def setTempDay():




if __name__ == "__main__":
    setup()

    try:
        # while False:
        colorWipe((255, 0, 0), 10)  # Red wipe
            # colorWipe(Color(0, 255, 0), 10)  # Green wipe
            # colorWipe(Color(0, 0, 255), 10)  # Blue wipe

            # theaterChase(Color(255, 0, 0), 50)  # Red theaterChase
            # theaterChase(Color(0, 255, 0), 50)  # Green theaterChase
            # theaterChase(Color(0, 0, 255), 50)  # Blue theaterChase

            # rainbow(10)

            # rainbowCycle(10)

            # theaterChaseRainbow(50)

            # playImage('dubbelwave.png')
            # pass

        setColor((255,0,0))
        time.sleep(0.5)
        setColor((254, 0, 0))
        time.sleep(0.5)
        setColor((253, 0, 0))
        time.sleep(0.5)
        # fadeToColor((255, 0, 0), 1)
        # fadeToColor((0, 255, 0), 1)
        # fadeToColor((0, 0, 255), 1)


    except KeyboardInterrupt:
        pass

    print("clean exit!")
    setColor((0, 0, 0))