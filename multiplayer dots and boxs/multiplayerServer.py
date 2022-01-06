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
	return eval(dictString)


class Server:
	def __init__(self, serverIP="127.0.0.1", port=65432, maxNumOfClients=4, serverDetails={}):
		self.IP = serverIP
		self.port = port
		self.maxNumOfClients = maxNumOfClients

		self.clientsConnected = []
		self.nextID = 0

		self.serverDetails = serverDetails
		self.UpdateServerDetails()

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
			for client in self.clientsConnected:
				client.connection.send(str({"serverDetails": self.serverDetails, "ID": client.ID}).encode())
			self.nextID += 1
			_, _, diff = t.Stop()
			print(f"Client {address[0]}:{address[1]} connected at - {NowFormatted()} - in {diff}.")

			# create a new thread
			threading._start_new_thread(self.clientsConnected[-1].Receive, ())
			self.threadCount += 1
			print(f"New thread created for client: {self.clientsConnected[-1].ID}. Thread count: {self.threadCount}, number of clients: {len(self.clientsConnected)}")
	
	def UpdateServerDetails(self):
		activeUsers = []
		for client in self.clientsConnected:
			activeUsers.append(client.name)
		self.serverDetails["activeUsers"] = activeUsers
		self.serverDetails["IP"] = self.IP
		self.serverDetails["port"] = self.port

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
		for client in self.clientsConnected:
			client.connection.send(str({"serverDetails": self.serverDetails, "ID": client.ID}).encode())
			
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
		while True:
			try:
				txt = self.connection.recv(1024).decode()

				if not txt:
					break

				data = ConvertStringToDict(txt)

				print(f"Client sent data: {data}")

				if data.get("close", False):
					break

				self.server.UpdateClients(data)
			except ConnectionResetError:
				print(f"Client: {self.ID} was forcibly removed by host.")
				break

		self.Close()

	def Close(self):
		self.server.Remove(self)
		self.connection.close()
		sys.exit(0)



if __name__ == "__main__":
	s = Server(serverDetails={"name": "Server 1"})
	s.Start()
