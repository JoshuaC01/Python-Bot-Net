class NewConnection:
	def __init__(self, port):
		self.port = port
		self.active = False
		self.conn = None
		self.hostname = ""
		self.os = ""
		self.shellOpen = False
		self.shell = None
		self.configOpen = False
		self.config = None