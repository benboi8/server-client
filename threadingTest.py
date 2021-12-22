import threading


def p():
	print(1)

dataReceiver = threading.Thread(target=p)
dataReceiver.start()
dataReceiver = threading.Thread(target=p)
dataReceiver.start()
