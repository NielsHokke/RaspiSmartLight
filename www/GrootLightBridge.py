import zmq
import cgi

# Move this file to your www dir.

context = zmq.Context()

data = cgi.FieldStorage()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

command = data.getvalue('cmd')

socket.send(command)
print socket.recv()
