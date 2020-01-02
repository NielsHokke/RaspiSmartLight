import zmq
import cgi

# Move this file to your www dir.


URL = "tcp://127.0.0.1:5555"

data = cgi.FieldStorage()



command = str(data.getvalue('cmd'))
print(command)

#  Socket to talk to server
ctx = zmq.Context.instance()
s1 = ctx.socket(zmq.PUB)
s1.bind(URL)
s1.send_string(command)
s1.close()

ctx = zmq.Context.instance()
s2 = ctx.socket(zmq.SUB)
s2.setsockopt_string(zmq.SUBSCRIBE, '')
s2.connect(URL)

print(s2.recv_string())

s2.close()
