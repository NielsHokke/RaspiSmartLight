import RPi.GPIO as GPIO
import time
import zmq

import threading
import MainLight

MainLight.setup()

# Thread variables
threadHandleM = threading.Thread()
threadHandleR = threading.Thread()
threadHandleLB = threading.Thread()
threadHandleLO = threading.Thread()

def light(on):

    if on:
        fadeTo = 100
    else:
        fadeTo = 0

    print(f"Turning on all lights")
    threadHandleM = threading.Thread(name='fade_all_to', target=MainLight.fade_M_to, args=(fadeTo, 0.5))
    threadHandleR = threading.Thread(name='fade_all_to', target=MainLight.fade_R_to, args=(fadeTo, 0.5))
    threadHandleLB = threading.Thread(name='fade_all_to', target=MainLight.fade_LB_to, args=(fadeTo, 0.5))
    threadHandleLO = threading.Thread(name='fade_all_to', target=MainLight.fade_LO_to, args=(fadeTo, 0.5))

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

knopPin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(knopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

# TODO read state as off
toggle = False

try:
    print("waiting for knop...")
    while True:
        one = GPIO.input(knopPin)
        time.sleep(0.1)
        two = GPIO.input(knopPin)
        time.sleep(0.1)
        three = GPIO.input(knopPin)

        if toggle:
            if not (one or two or three):
                print("Toggle")
                # socket.send_string("all_toggle")
                # print(socket.recv())
                toggle = False
                light(toggle)
        else:
            if one and two and three:
                print("Toggle")
                # socket.send_string("all_toggle")
                # print(socket.recv())
                toggle = True
                light(toggle)

except KeyboardInterrupt:
    pass

GPIO.cleanup()  # clean up GPIO on normal exit
print("clean exit")
