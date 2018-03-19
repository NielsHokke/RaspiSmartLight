import RPi.GPIO as GPIO
import time
import zmq

knopPin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(knopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

toggle = False

try:
    print "waiting for knop..."
    while True:
        one = GPIO.input(knopPin)
        time.sleep(0.1)
        two = GPIO.input(knopPin)
        time.sleep(0.1)
        three = GPIO.input(knopPin)

        if toggle :
            if not (one or two or three):
                socket.send("all_toggle")
                print socket.recv()
                toggle = False
        else:
            if one and two and three:
                socket.send("all_toggle")
                print socket.recv()
                toggle = True

except KeyboardInterrupt:
    pass

GPIO.cleanup()  # clean up GPIO on normal exit
print"clean exit"
