import zmq
import threading
import MainLight
import RGBLight
import json
from neopixel import Color

# Connect to webSocket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

# Initialise MainLight
MainLight.setup()

# Initialise RGBLight
RGBLight.setup()

# Thread variables
threadHandleM = threading.Thread()
threadHandleR = threading.Thread()
threadHandleLB = threading.Thread()
threadHandleLO = threading.Thread()

threadHandleRGB = threading.Thread()


# Stops selected threads
def stopThreads(M, R, LB, LO, RGB=False):
	global threadHandleM
	global threadHandleR
	global threadHandleLB
	global threadHandleLO
	global threadHandleRGB
	
	MainLight.stopThreadM = M
	MainLight.stopThreadR = R
	MainLight.stopThreadLB = LB
	MainLight.stopThreadLO = LO

	RGBLight.stopThreadRGB = RGB

	if M and threadHandleM.isAlive():
		threadHandleM.join()
	if R and threadHandleR.isAlive():
		threadHandleR.join()
	if LB and threadHandleLB.isAlive():
		threadHandleLB.join()
	if LO and threadHandleLO.isAlive():
		threadHandleLO.join()

	if RGB and threadHandleRGB.isAlive():
		threadHandleRGB.join()

# Main Command listener
try:
	print "listening for commands..."
	while True:
		message = socket.recv()
		print("Received request: %s" % message)

		if "all" in message:
			stopThreads(True, True, True, True)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				if status['Midden'] == 0.0 and status['Rechts'] == 0.0 and status['LinksBoven'] == 0.0 and status['LinksOnder'] == 0.0:
					M = 100
				else:
					M = 0
			elif 'aan' in message:
				M = 100
			elif 'fade' in message:
				lamp, fade, Mstring, timestring = message.split('_')
				M = float(Mstring)
				time = float(timestring)
			else:
				M = 0

			try:
				threadHandleM = threading.Thread(name='fade_all_to', target=MainLight.fade_M_to, args=(M, time))
				threadHandleR = threading.Thread(name='fade_all_to', target=MainLight.fade_R_to, args=(M, time))
				threadHandleLB = threading.Thread(name='fade_all_to', target=MainLight.fade_LB_to, args=(M, time))
				threadHandleLO = threading.Thread(name='fade_all_to', target=MainLight.fade_LO_to, args=(M, time))

				threadHandleM.daemon = True
				threadHandleR.daemon = True
				threadHandleLB.daemon = True
				threadHandleLO.daemon = True

				threadHandleM.start()
				threadHandleR.start()
				threadHandleLB.start()
				threadHandleLO.start()
			except:
				print "Error: unable to start all threads"

			status = {'Midden': M, 'Rechts': M, 'LinksBoven': M, 'LinksOnder': M}
			reply = json.dumps(status)
			socket.send(reply)

		elif "midden" in message:
			stopThreads(True, False, False, False)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				M = 100 if status['Midden'] == 0.0 else 0
			elif 'aan' in message:
				M = 100
			elif 'fade' in message:
				lamp, fade, Mstring, timestring = message.split('_')
				M = float(Mstring)
				time = float(timestring)
			else:
				M = 0

			try:
				threadHandleM = threading.Thread(name='fade_M_to', target=MainLight.fade_M_to, args=(M, time))
				threadHandleM.daemon = True
				threadHandleM.start()
			except:
				print "Error: unable to start all threads"

			status = MainLight.status()
			status['Midden'] = M
			reply = json.dumps(status)
			socket.send(reply)

		elif "rechts" in message:
			stopThreads(False, True, False, False)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				M = 100 if status['Rechts'] == 0.0 else 0
			elif 'aan' in message:
				M = 100
			elif 'fade' in message:
				lamp, fade, Mstring, timestring = message.split('_')
				M = float(Mstring)
				time = float(timestring)
			else:
				M = 0

			try:
				threadHandleR = threading.Thread(name='fade_R_to', target=MainLight.fade_R_to, args=(M, time))
				threadHandleR.daemon = True
				threadHandleR.start()
			except:
				print "Error: unable to start all threads"
			status = MainLight.status()
			status['Rechts'] = M
			reply = json.dumps(status)
			socket.send(reply)

		elif "links_boven" in message:
			stopThreads(False, False, True, False)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				M = 100 if status['LinksBoven'] == 0.0 else 0
			elif 'aan' in message:
				M = 100
			elif 'fade' in message:
				lamp, fade, Mstring, timestring = message.split('_')
				M = float(Mstring)
				time = float(timestring)
			else:
				M = 0

			try:
				threadHandleLB = threading.Thread(name='fade_LB_to', target=MainLight.fade_LB_to, args=(M, time))
				threadHandleLB.daemon = True
				threadHandleLB.start()

			except:
				print "Error: unable to start all threads"
			status = MainLight.status()
			status['LinksBoven'] = M
			reply = json.dumps(status)
			socket.send(reply)


		elif "links_onder" in message:
			stopThreads(False, False, False, True)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				M = 100 if status['LinksOnder'] == 0.0 else 0
			elif 'aan' in message:
				M = 100
			elif 'fade' in message:
				lamp, fade, Mstring, timestring = message.split('_')
				M = float(Mstring)
				time = float(timestring)
			else:
				M = 0

			try:
				threadHandleLO = threading.Thread(name='fade_LO_to', target=MainLight.fade_LO_to, args=(M, time))
				threadHandleLO.daemon = True
				threadHandleLO.start()
			except:
				print "Error: unable to start all threads"
			status = MainLight.status()
			status['LinksOnder'] = M
			reply = json.dumps(status)
			socket.send(reply)

		elif message == "status":
			reply = json.dumps(MainLight.status())
			socket.send(reply)
			print(reply)

		elif "set_temp" in message:
			stopThreads(False, False, False, False, True)

			a, b, value = message.split('_')
			RGBLight.setTemp(int(value))

			reply = json.dumps(MainLight.status())
			socket.send(reply)

		elif "clear" in message:
			stopThreads(False, False, False, False, True)

			RGBLight.setColor(Color(0, 0, 0))

			reply = json.dumps(MainLight.status())
			socket.send(reply)

		elif "set_color" in message:
			stopThreads(False, False, False, False, True)

			a, b, R, G, B = message.split('_')
			RGBLight.setColor(Color(int(R), int(G), int(B)))

			reply = json.dumps(MainLight.status())
			socket.send(reply)

		elif "rainbow" in message:
			stopThreads(False, False, False, False, True)

			try:
				threadHandleRGB = threading.Thread(name='rainbow', target=RGBLight.rainbowCycle, args=(10, 5, True))
				threadHandleRGB.daemon = True
				threadHandleRGB.start()
			except:
				print "Error: unable to start all threads"

			reply = json.dumps(MainLight.status())
			socket.send(reply)

		elif "fade_to_color" in message:
			stopThreads(False, False, False, False, True)

			a, b, c, R, G, B, time = message.split('_')

			try:
				threadHandleRGB = threading.Thread(name='fadetocolor', target=RGBLight.fadeToColor, args=(Color(int(R), int(G), int(B)), float(time), True))
				threadHandleRGB.daemon = True
				threadHandleRGB.start()
			except:
				print "Error: unable to start all threads"

			reply = json.dumps(MainLight.status())
			socket.send(reply)


		else:
			socket.send("Error: unknown command: " + message)
			print("Error: unknown command: " + message)

except KeyboardInterrupt:
	pass

print "\nclean exit!"
stopThreads(True, True, True, True)
MainLight.cleanup()
RGBLight.cleanup()
