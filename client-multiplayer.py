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

	def Send(self, data):
		self.sock.sendall(str(data).encode())

	def Receive(self):
		data = ConvertStringToDict(self.sock.recv(1024).decode())

		self.dataQueue.append(data)



if __name__ == "__main__":
	pass