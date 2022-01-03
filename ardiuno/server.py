import pyfirmata as pyfir
import time
import sys

import socket
import threading

try:
	board = pyfir.Arduino("COM4")
	it = pyfir.util.Iterator(board)
	it.start()
except:
	print("No board found")
	sys.exit(0)



host = "192.168.0.2"
port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
print("Server started")

sock.listen()

conn, addr = sock.accept()
print(f"Connection with {addr}")

ledPin = board.get_pin("d:13:o")


def FlashLed():
	time.sleep(1)
	ledPin.write(1)
	time.sleep(1)
	ledPin.write(0)

def Receive():
	msg = conn.recv(1024).decode()

	if msg:
		print(f"msg: {msg}")

while True:
	Receive()
	# threading._start_new_thread(FlashLed, ())
