import socket
import datetime as dt
import threading
import sys
import time

import os

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from General import *



def ConvertStringToDict(dictString):
	dictString = dictString.strip("{}")

	returnDict = {}

	for txt in dictString.split(","):
		key, value = txt.split(":")

		key = key.strip(" '")
		value = value.strip(" '")

		try:
			try:
				returnDict[key] = int(value)
			except:
				returnDict[key] = bool(value)
		except:
			returnDict[key] = value


	return returnDict



class Server:

	def __init__(self, serverIP="127.0.0.1", port=65432, maxNumOfClients=4, serverDetails={}):
		self.IP = serverIP
		self.port = port
		self.maxNumOfClients = maxNumOfClients

		self.clientsConnected = []
		self.nextID = 0

		self.serverDetails = serverDetails

		self.threadCount = 0


	def Open(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.IP, self.port))

	def Listen(self):
		self.sock.listen()

	def Accept(self):
		t = Timer()
		while len(self.clientsConnected) < self.maxNumOfClients:
			# accept new clients
			connection, address = self.sock.accept()


			# log


			t.Start()
			client = ConvertStringToDict(connection.recv(1024).decode())
			self.clientsConnected.append(Client(connection, address, self, client["name"], self.nextID, client))
			self.UpdateServerDetails()
			connection.send(str(self.serverDetails).encode())
			self.nextID += 1
			_, _, diff = t.Stop()
			print(f"Client {address[0]}:{address[1]} connected at - {NowFormatted()} - in {diff}.")

			# create a new thread
			threading._start_new_thread(self.clientsConnected[-1].Receive, ())
			self.threadCount += 1
			print(f"New thread created for client:{self.clientsConnected[-1].ID}. Thread count: {self.threadCount}")
	
	def UpdateServerDetails(self):
		self.serverDetails["activeUsers"] = self.clientsConnected

	def Start(self):
		t = Timer()
		t.Start()
		self.Open()
		_, _, diff = t.Stop(printResult=False)
		print(f"Server started at - {NowFormatted()} - in {diff}.")
		self.Listen()
		self.Accept()

	def UpdateClients(self, data):
		for client in self.clientsConnected:
			client.connection.sendall(str(data).encode())

	def Remove(self, client):
		if client in self.clientsConnected:
			self.clientsConnected.remove(client)

		self.UpdateServerDetails()
		self.UpdateClients(str(self.serverDetails))

		self.threadCount -= 1

		print(f"Client: {client.ID} disconnected at - {NowFormatted()}.")



class Client:
	def __init__(self, connection, address, server, name, ID, details):
		self.connection = connection
		self.address = address
		self.server = server
		self.name = name
		self.ID = ID
		self.details = details

	def Receive(self):
		self.connection.send("Connection-Confirmed".encode())

		while True:
			txt = self.connection.recv(1024).decode()

			if not txt:
				break

			data = ConvertStringToDict(txt)

			if data["close"]:
				break

			self.server.UpdateClients()

		self.Close()

	def Close(self):
		self.server.Remove(self)

		self.connection.close()
		sys.exit(0)



if __name__ == "__main__":
	s = Server(serverDetails={"name": "Server 1"})
	s.Start()
