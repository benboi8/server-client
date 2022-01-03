import socket
import threading
import time
import sys

class Client:
	def __init__(self, host="127.0.0.1", port=65432, name=""):
		self.host = host
		self.port = port
		self.name = name

		self.shutdown = False
		self.dataQueue = []
		self.serverName = ""
		self.activeUsers = []

	def Open(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def Connect(self):
		self.sock.connect((self.host, self.port))

		print(f"Connection successful")

		self.Send(self.name)

		self.ID = self.sock.recv(1024).decode()

	def Close(self):
		self.shutdown = True

	def Send(self, msg):
		msg = str(msg)
		if "/close" in msg:
			self.Close()
		self.sock.sendall(msg.encode())

	def Receive(self):
		if self.shutdown:
			return
		msg = self.sock.recv(1024).decode()
		if "SERVER-ActiveUsers-" in msg:
			self.activeUsers = msg.split("SERVER-ActiveUsers-")[1]
			self.serverName = msg.split("-")[1]
		else:
			self.dataQueue.append(msg)

	def SR(self):
		self.Send(input(""))
		time.sleep(0.1)
		self.Receive()


if __name__ == "__main__":
	c = Client()
	c.Open()
	c.Connect()

	while True:
		c.SR()