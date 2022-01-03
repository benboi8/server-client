import socket
import datetime as dt
import random
import threading
import sys
import time

import os

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from General import *


class Server:
	def __init__(self, host="127.0.0.1", port=65432, maxNumConnectedClients=100, name=""):
		self.host = host
		self.port = port
		self.name = name

		self.logFolder = "logs/"	

		self.threadCount = 0
		self.clientsConnected = []

		self.clientID = 0
		self.maxNumConnectedClients = maxNumConnectedClients

		CreateFile(f"log - {NowFormatted('%d-%m-%Y-%H-%M-%S-%f')}.txt", self.logFolder)

	def Open(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		print("Server started.")

	def Listen(self):
		self.sock.listen()

	def Accept(self):
		while len(self.clientsConnected) < self.maxNumConnectedClients:
			# accept new clients
			connection, address = self.sock.accept()

			self.Log(f"Client {address[0]}:{address[1]} connected at date {NowFormatted('%d/%m/%Y')} at time {NowFormatted('%H:%M:%S:%f')}")

			self.clientID += 1
			name = connection.recv(1024).decode()
			self.clientsConnected.append(Client(connection, address, self, name))
			self.clientsConnected[-1].connection.send(f"serverName-{self.name}-".encode())
			
			# create new thread
			threading._start_new_thread(self.clientsConnected[-1].Receive, ())
			self.threadCount = len(self.clientsConnected)
			print(f"Thread number: {self.threadCount}")

			self.UpdateActiveUsers()

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

	def Log(self, message):
		print(message)




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


class ChatServer(Server):
	def __init__(self, host="127.0.0.1", port=65432, maxNumConnectedClients=100, name=""):
		super().__init__(host, port, maxNumConnectedClients, name)

	def UpdateActiveUsers(self):
		names = ""
		for client in self.clientsConnected:
			names += f"▷ {client.name}\n"
		for client in self.clientsConnected:
			client.connection.send(f"SERVER-ActiveUsers-{names}".encode())


# s = ChatServer(host="192.168.0.2", port=5001, name="Chatroom 1")
# s.Open()
# s.Listen()
# s.Accept()



s = Server(name="Server")
s.Open()
s.Listen()
s.Accept()

