import socket
import datetime as dt
import threading
import sys
import time


import os

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from General import *



from multiplayerServer import ConvertStringToDict




class Client:
	def __init__(self, serverIP="127.0.0.1", port=65432, details={}):
		self.IP = serverIP
		self.port = port

		self.details = details
		self.serverDetails = {}

		self.dataQueue = []

	def Open(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def Connect(self):
		self.sock.connect((self.IP, self.port))

		self.sock.sendall(str(self.details).encode())

		self.serverDetails = ConvertStringToDict(self.sock.recv(1024).decode())

		print(f"Connected to {self.serverDetails['name']} with IP: {self.serverDetails['IP']} on port: {self.serverDetails['port']}")

	def Start(self):
		self.Open()
		self.Connect()

	def Send(self, msg):
		data = {
			"name": self.details["name"],
			"data": msg
		}

		self.sock.send(str(data).encode())

	def Receive(self):
		msg = self.sock.recv(1024).decode()
		print(f"Received message from server: {msg}")
		data = ConvertStringToDict(msg)

		self.dataQueue.append(data)

		return data



if __name__ == "__main__":
	c = Client(details={"name": "Ben"})
	c.Start()

	def Send():
		while True:
			time.sleep(0.1)
			c.Send(input("Input: "))
		
		sys.exit(0)

	def Receive():
		while True:
			c.Receive()


	threading._start_new_thread(Send, ())
	Receive()
