import RPi.GPIO as GPIO
import time
import RGBLight

# Strip Pins
StripMiddenPin = 26
StripRechtsPin = 6
StripLinksBovenPin = 13
StripLinksOnderPin = 19

# Strip DC Status
StripMiddenDC = 0.0
StripRechtsDC = 0.0
StripLinksBovenDC = 0.0
StripLinksOnderDC = 0.0

# Fade Variables
StepsPerSec = 100

# Thread Variables
stopThreadM = False
stopThreadR = False
stopThreadLB = False
stopThreadLO = False


# Intialise GPIO
def setup():
    global stopThreadM
    global stopThreadR
    global stopThreadLB
    global stopThreadLO

    global StripMiddenDC
    global StripRechtsDC
    global StripLinksBovenDC
    global StripLinksOnderDC

    global StripMidden
    global StripRechts
    global StripLinksBoven
    global StripLinksOnder

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(StripMiddenPin, GPIO.OUT)
    GPIO.setup(StripRechtsPin, GPIO.OUT)
    GPIO.setup(StripLinksBovenPin, GPIO.OUT)
    GPIO.setup(StripLinksOnderPin, GPIO.OUT)

    StripMidden = GPIO.PWM(StripMiddenPin, 600)
    StripRechts = GPIO.PWM(StripRechtsPin, 800)
    StripLinksBoven = GPIO.PWM(StripLinksBovenPin, 1000)
    StripLinksOnder = GPIO.PWM(StripLinksOnderPin, 1200)

    StripMidden.start(0)
    StripRechts.start(0)
    StripLinksBoven.start(0)
    StripLinksOnder.start(0)

# Called on exit
def cleanup():
    GPIO.cleanup()


# Fade Midden led strip from current state to new state, interruptable by stopThreadM
def fade_M_to(MiddenDC, TotalTime):
    global stopThreadM
    stopThreadM = False
    global StripMiddenDC
    global StripMidden

    TotalSteps = int(StepsPerSec * TotalTime)
    if TotalSteps == 0: TotalSteps = 1
    TimeStep = (TotalTime*1.0)/TotalSteps
    MiddenStep = (MiddenDC - StripMiddenDC * 1.0)/TotalSteps

    for i in range(0, TotalSteps):

        StripMiddenDC += MiddenStep
        StripMiddenDC = max(min(100.0, StripMiddenDC), 0.0)
        StripMidden.ChangeDutyCycle(StripMiddenDC)

        if stopThreadM:
            return

        time.sleep(TimeStep)

    StripMiddenDC = MiddenDC
    StripMidden.ChangeDutyCycle(StripMiddenDC)
    RGBLight.setMtemp(StripMiddenDC)


# Fade rechts led strip from current state to new state, interruptable by stopThreadR
def fade_R_to(RechtsDC, TotalTime):
    global stopThreadR
    stopThreadR = False
    global StripRechtsDC
    global StripRechts

    TotalSteps = int(StepsPerSec * TotalTime)
    if TotalSteps == 0: TotalSteps = 1
    TimeStep = (TotalTime * 1.0) / TotalSteps
    RechtsStep = (RechtsDC - StripRechtsDC * 1.0) / TotalSteps

    for i in range(0, TotalSteps):

        StripRechtsDC += RechtsStep
        StripRechtsDC = max(min(100.0, StripRechtsDC), 0.0)
        StripRechts.ChangeDutyCycle(StripRechtsDC)

        if stopThreadR:
            return

        time.sleep(TimeStep)

    StripRechtsDC = RechtsDC
    StripRechts.ChangeDutyCycle(StripRechtsDC)
    RGBLight.setRtemp(StripRechtsDC)


# Fade links boven led strip from current state to new state, interruptable by stopThreadLB
def fade_LB_to(LBovenDC, TotalTime):
    global stopThreadLB
    stopThreadLB = False
    global StripLinksBovenDC
    global StripLinksBoven

    TotalSteps = int(StepsPerSec * TotalTime)
    if TotalSteps == 0: TotalSteps = 1
    TimeStep = (TotalTime * 1.0) / TotalSteps
    LBovenStep = (LBovenDC - StripLinksBovenDC * 1.0) / TotalSteps

    for i in range(0, TotalSteps):

        StripLinksBovenDC += LBovenStep
        StripLinksBovenDC = max(min(100.0, StripLinksBovenDC), 0.0)
        StripLinksBoven.ChangeDutyCycle(StripLinksBovenDC)

        if stopThreadLB:
            return

        time.sleep(TimeStep)

    StripLinksBovenDC = LBovenDC
    StripLinksBoven.ChangeDutyCycle(StripLinksBovenDC)
    RGBLight.setLBtemp(StripLinksBovenDC)


# Fade links onder led strip from current state to new state, interruptable by stopThreadLO
def fade_LO_to(LOnderDC, TotalTime):
    global stopThreadLO
    stopThreadLO = False
    global StripLinksOnderDC
    global StripLinksOnder

    TotalSteps = int(StepsPerSec * TotalTime)
    if TotalSteps == 0: TotalSteps = 1
    TimeStep = (TotalTime * 1.0) / TotalSteps
    LOnderStep = (LOnderDC - StripLinksOnderDC * 1.0) / TotalSteps

    for i in range(0, TotalSteps):

        StripLinksOnderDC += LOnderStep
        StripLinksOnderDC = max(min(100.0, StripLinksOnderDC), 0.0)
        StripLinksOnder.ChangeDutyCycle(StripLinksOnderDC)

        if stopThreadLO:
            return

        time.sleep(TimeStep)

    StripLinksOnderDC = LOnderDC
    StripLinksOnder.ChangeDutyCycle(StripLinksOnderDC)


# Returns current status
def status():
    global StripMiddenDC
    global StripRechtsDC
    global StripLinksBovenDC
    global StripLinksOnderDC

    return {'Midden': StripMiddenDC, 'Rechts': StripRechtsDC, 'LinksBoven': StripLinksBovenDC, 'LinksOnder': StripLinksOnderDC}



if __name__ == "__main__":
    import threading

    print("Starting MainLight test")
    setup()

    # Thread variables
    threadHandleM = threading.Thread()
    threadHandleR = threading.Thread()
    threadHandleLB = threading.Thread()
    threadHandleLO = threading.Thread()

    print(f"Turning on all lights")
    threadHandleM = threading.Thread(name='fade_all_to', target=fade_M_to, args=(100, 0.5))
    threadHandleR = threading.Thread(name='fade_all_to', target=fade_R_to, args=(100, 0.5))
    threadHandleLB = threading.Thread(name='fade_all_to', target=fade_LB_to, args=(100, 0.5))
    threadHandleLO = threading.Thread(name='fade_all_to', target=fade_LO_to, args=(100, 0.5))

    print(f"Deamon setting to true")
    threadHandleM.daemon = True
    threadHandleR.daemon = True
    threadHandleLB.daemon = True
    threadHandleLO.daemon = True

    print(f"Start!")
    threadHandleM.start()
    threadHandleR.start()
    threadHandleLB.start()
    threadHandleLO.start()

    time.sleep(10 * 60)

    cleanup()
    print("Clean exit!")



