import zmq
import threading
import json
from rpi_ws281x import Color
from datetime import datetime

import MainLight
import RGBLight
import Fan



# Connect to webSocket
ctx = zmq.Context()
socket = ctx.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE,'')
socket.connect("tcp://127.0.0.1:5555")

# Initialise MainLight
MainLight.setup()

# Initialise RGBLight
RGBLight.setup()

# Initialise Fan
Fan.setup()


# Thread variables
threadHandleM = threading.Thread()
threadHandleR = threading.Thread()
threadHandleLB = threading.Thread()
threadHandleLO = threading.Thread()

threadHandleRGB = threading.Thread()

threadHandleFAN = threading.Thread()

# Stops selected threads
def stopThreads(M, R, LB, LO, RGB=False, FAN=False):
	global threadHandleM
	global threadHandleR
	global threadHandleLB
	global threadHandleLO

	global threadHandleRGB

	global threadHandleFAN

	MainLight.stopThreadM = M
	MainLight.stopThreadR = R
	MainLight.stopThreadLB = LB
	MainLight.stopThreadLO = LO

	RGBLight.stopThreadRGB = RGB

	Fan.stopThreadFan = FAN

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

	if FAN and threadHandleFAN.isAlive():
		threadHandleFAN.join()


# Main Command listener
try:
	print("listening for commands...")
	while True:
		message = socket.recv_string()
		print("Received request: %s" % message)

# MAIN LIGHT CMD's

		if "all" in message:
			stopThreads(True, True, True, True)

			status = MainLight.status()

			time = 0.5

			if 'toggle' in message:
				if status['Midden'] == 0.0 and status['Rechts'] == 0.0 and status['LinksBoven'] == 0.0 and status[
					'LinksOnder'] == 0.0:
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
				print("Error: unable to start all threads")

			status = {'Midden': M, 'Rechts': M, 'LinksBoven': M, 'LinksOnder': M}
			reply = json.dumps(status)
			socket.send_string(reply)

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
				print("Error: unable to start all threads")

			status = MainLight.status()
			status['Midden'] = M
			reply = json.dumps(status)
			socket.send_string(reply)

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
				print("Error: unable to start all threads")
			status = MainLight.status()
			status['Rechts'] = M
			reply = json.dumps(status)
			socket.send_string(reply)

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
				print("Error: unable to start all threads")
			status = MainLight.status()
			status['LinksBoven'] = M
			reply = json.dumps(status)
			socket.send_string(reply)


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
				print("Error: unable to start all threads")
			status = MainLight.status()
			status['LinksOnder'] = M
			reply = json.dumps(status)
			socket.send_string(reply)

		elif message == "status":
			reply = json.dumps(MainLight.status())
			socket.send_string(reply)
			print(reply)

# RGB LIGHT CMD's

		elif "set_temp" in message:
			stopThreads(False, False, False, False, True)

			a, b, value = message.split('_')
			if "day" in value:
				# try:
				#     threadHandleRGB = threading.Thread(name='setTempDay', target=RGBLight.setTempDay, args=(10, 5, True))
				#     threadHandleRGB.daemon = True
				#     threadHandleRGB.start()
				# except:
				#     print("Error: unable to start all threads")
				pass
			else:
				RGBLight.setTemp(int(value))

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

		elif "clear" in message:
			stopThreads(False, False, False, False, True)

			RGBLight.setColor(Color(0, 0, 0))

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

		elif "set_color" in message:
			stopThreads(False, False, False, False, True)

			a, b, R, G, B = message.split('_')
			RGBLight.setColor(Color(int(R), int(G), int(B)))

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

		elif "rainbow" in message:
			stopThreads(False, False, False, False, True)

			try:
				threadHandleRGB = threading.Thread(name='rainbow', target=RGBLight.rainbowCycle, args=(10, 5, True))
				threadHandleRGB.daemon = True
				threadHandleRGB.start()
			except:
				print("Error: unable to start all threads")

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

		elif "fade_to_color" in message:
			stopThreads(False, False, False, False, True)

			try:
				a, b, c, R, G, B, time = message.split('_')

				threadHandleRGB = threading.Thread(name='fadetocolor', target=RGBLight.fadeToColor,
												   args=(Color(int(R), int(G), int(B)), float(time), True))
				threadHandleRGB.daemon = True
				threadHandleRGB.start()
			except:
				print("Error: unable to start all threads")

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

# FAN CMD's

		elif "set_fan_off" in message:
			stopThreads(False, False, False, False, False, True)

			try:
				threadHandleFAN = threading.Thread(name='setfan', target=Fan.setFanOff)
				threadHandleFAN.daemon = True
				threadHandleFAN.start()
			except:
				print("Error: unable to start all threads")

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)

		elif "set_fan" in message:
			stopThreads(False, False, False, False, False, True)

			try:
				# set_fan_low_30
				a, b, speed, minutes = message.split('_')

				threadHandleFAN = threading.Thread(name='setfan', target=Fan.setFan, args=(speed, int(minutes)))
				threadHandleFAN.daemon = True
				threadHandleFAN.start()
			except:
				print("Error: unable to start all threads")

			reply = json.dumps(MainLight.status())
			socket.send_string(reply)



# OTHER CMD's

		elif "test" in message:
			time = str(datetime.now())
			print(time + " " + message)
			socket.send_string(time)

		else:
			socket.send_string("Error: unknown command: " + message)
			print("Error: unknown command: " + message)

except KeyboardInterrupt:
	pass

print("\nclean exit!")
stopThreads(True, True, True, True)
MainLight.cleanup()
RGBLight.cleanup()
