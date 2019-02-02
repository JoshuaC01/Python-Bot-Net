import socket, os, sys, time, base64, extra

def createSocket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	return s

def bindSocket(s, port):
	binded = False
	while not binded:
		try:
			s.bind(('', int(port)))
			s.listen(1)
			binded = True
			return s
		except socket.error:
			binded = False

def acceptSocket(s):
	conn, addr = s.accept()
	hostname, os = conn.recv(1024).decode().split(",")
	return (conn, hostname, os)


def createConnection(port):
	return acceptSocket(bindSocket(createSocket(), port))

def updateConns(allConns):
	newConns = []
	oldConns = []   
	for connection in allConns:
		if connection.active == True:
			try:
				connection.conn.send("Checking If Alive".encode("utf8"))
				text = connection.conn.recv(1024).decode()
				#print("Already Connected To: " + str(connection.port))
			except:
				connection.active = False
				connection.conn = None
				oldConns.append(connection)
			continue
		try:
			data = createConnection(connection.port)
			#text = data.recv(1024).decode().split(",")
			#print(text)

			connection.active = True
			connection.conn = data[0]
			connection.hostname = data[1]
			connection.os = data[2]
			newConns.append(connection)
		except socket.timeout:
			pass

	return [allConns, newConns, oldConns]