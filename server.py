import socket
import datetime as dt
import random
import threading
import sys
import time

class Server:
	def __init__(self, host="127.0.0.1", port=65432, name=""):
		self.host = host
		self.port = port
		self.name = name

	def Open(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		print("Server started.")

	def Listen(self):
		self.sock.listen()

	def Accept(self):
		self.connection, self.address = self.sock.accept()
		return self.connection, self.address

	def Receive(self, waitTime=None, msgMax=None):
		self.startTime = dt.datetime.now()

		msgCount = 0

		timePassed = dt.datetime.now() - self.startTime

		with self.connection:
			print(f"Connection with {self.address}")

			self.closeCode = random.randint(0, 10000000)

			self.connection.sendall(str(self.closeCode).encode())

			while (timePassed.seconds < waitTime if waitTime != None else True) or (msgCount < msgMax if msgMax != None else True):
				timePassed = dt.datetime.now() - self.startTime

				data = self.connection.recv(1024).decode()

				if data:
					msgCount += 1
					print(f"Data received: {data}")

				if data == f"Close-Auth-Code-{self.closeCode}":
					print("Closed")
					break


class Client:
	def __init__(self, connection, address, ID, server, name):
		self.connection = connection
		self.address = address
		self.ID = ID
		self.server = server
		self.name = name

		self.commands = {
			"close": self.Close,
			"chat": self.Chat,
			"whisper": self.Whisper
		}

	def SplitCommand(self, text):
		return text.split(" ")[0][1:], text[len(text.split(" ")[0]) + 1:]

	def Receive(self):
		self.connection.send(f"Connected to {self.server.name}.".encode())

		while True:
			data = self.connection.recv(1024).decode()

			if not data:
				break

			if "/" in data:
				command, msg = self.SplitCommand(data)
				self.commands.get(command, self.Error)(msg, command)
			else:
				msg = self.SplitCommand(data)
				self.Chat(data)

			for client in self.server.clients:
				client.connection.sendall(f"{self.name}: {data}".encode())

		self.connection.close()

	def Error(self, msg, command):
		print(f"There was an error in the command: {command} {msg}")

	def Close(self, msg="", command=""):
		self.connection.sendall(f"CloseServer-{self.name}".encode())
		if self in self.server.clients:
			self.server.clients.remove(self)
		self.server.UpdateActiveUsers()
		sys.exit(0)

	def Chat(self, msg, command=""):
		print(f"{self.name}: {msg}")

	def Whisper(self, msg, command=""):
		pass


class MultiServer(Server):
	def __init__(self, host="127.0.0.1", port=65432, maxClientNum=100, name=""):
		super().__init__(host, port, name)

		self.threadCount = 0
		self.clients = []
		self.maxID = 0
		self.maxClientNum = maxClientNum

	def Accept(self):
		while len(self.clients) < self.maxClientNum:
			# accept new clients
			connection, address = self.sock.accept()
			print(f"Connected to {address[0]}:{address[1]}")
			name = connection.recv(1024).decode()

			print(name)
			# create new client
			self.clients.append(Client(connection, address, self.maxID, self, name))
			self.clients[-1].connection.sendall(str(self.clients[-1].ID).encode())
			self.maxID += 1
			self.clients[-1].connection.send(f"serverName-{self.name}-".encode())

			# create new thread
			threading._start_new_thread(self.clients[-1].Receive, ())
			self.threadCount = len(self.clients)
			print(f"Thread number: {self.threadCount}")

			self.UpdateActiveUsers()

	def UpdateActiveUsers(self):
		names = ""
		for client in self.clients:
			names += f"▷ {client.name}\n"
		for client in self.clients:
			client.connection.send(f"SERVER-ActiveUsers-{names}".encode())


s = MultiServer(host="103.47.59.130", port=5001, name="Chatroom 1")
s.Open()
s.Listen()
s.Accept()
