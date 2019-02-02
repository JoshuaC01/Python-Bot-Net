import socket, os, sys, time, base64, extra, platform

data = [os.environ['COMPUTERNAME'], platform.system()]

def connect(host, port):
	notConnected = True
	while notConnected:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			s.connect((host, port))
			#print("Connected: Sending Data:", "Stuff")
			#str(os.environ['COMPUTERNAME']) + ',' + platform.system()
			#s.send("PC 1,Windows")
			notConnected = False

		except:
			pass


	s.send((str(data[0]) + "," + str(data[1])).encode("utf8"))
	return s

port = int(input("Port: "))

conn = connect('localhost', port)

active = True

while active:
	try:
		data = conn.recv(1024).decode()
		if data == "":
			continue

		if data == "Checking If Alive":
			print("Telling Server Im Alive")
			conn.send("Client Is Alive".encode("utf8"))
			continue

		if data == "disconnect":
			active = False
			print("Disconnecting Client")
			continue

		print(data)
	except:
		active = False