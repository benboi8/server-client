import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from General import *

import client
import threading


names = OpenFile("userNames.txt").split("\n")
userName = names[randint(0, len(names))]

print(0)

# create client
try:
	print("Trying to connect to server...")
	c = client.Client(host="192.168.0.2", port=5001, name=userName)
	c.Open()
	c.Connect()
	print(0.1)

except ConnectionRefusedError:
	print(0.2)
	print("No connection could be made to server.")
	sys.exit(0)

print(1)
def Send(msg):
	c.Send(msg)

	tib.UpdateText(tib.splashText)
	tib.input = ""


def Close():
	c.Send("/close")
	c.Close()



print(2)
from GUI import *
print(3)

ChangeFontName("arial-unicode-ms.ttf")


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	pg.display.update()


print(4)
def HandleEvents(event):
	HandleGui(event)



print(5)
messages = Label((0, 35, width - 250, height - 135), (lightBlack, darkWhite), textData={"alignText": "left-top"})
ScollBar((width - 250, 0, 50, height - 100), (lightBlack, darkWhite), scrollObj=messages, buttonData={"activeColor": lightRed})
serverName = Label((0, 0, width - 250, 35), (lightBlack, darkWhite), textData={"alignText": "left"})
tib = TextInputBox((0, height - 100, width - 100, 100), (lightBlack, darkWhite, lightRed), textData={"fontSize": 40, "alignText": "left"}, inputData={"closeOnMisInput": False})
sendBtn = Button((width - 100, height - 100, 100, 100), (lightBlack, darkWhite, lightRed), text="Send", onClick=Send, onClickArgs=tib.input)
Label((width - 200, 0, 200, 35), (lightBlack, darkWhite), text="Active users", textData={"alignText": "top", "fontSize": 20})
onlineUsers = Label((width - 200, 35, 200, height - 65), (lightBlack, darkWhite), textData={"alignText": "left-top", "fontSize": 25})
print(6)

# c.Receive()
startDay = dt.datetime.now().strftime("%d")
messages.UpdateText(f"{dt.datetime.now().strftime('------------------------------------------------  %d %B  %Y  ------------------------------------------------')}\n")
messages.UpdateText(messages.text + f"{dt.datetime.now().strftime('%H:%M:%S')}: Connected to {c.serverName}\n")

print(7)
while running:
	if c.shutdown:
		Close()
		running = False

	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	sendBtn.onClickArgs = [str(tib.input)]

	threading._start_new_thread(c.Receive, ())
	try:
		data = c.dataQueue[-1]
		messages.UpdateText(messages.text + f"{dt.datetime.now().strftime('%H:%M:%S')}: {data}\n")
		c.dataQueue = []

	except:
		pass

	if startDay != dt.datetime.now().strftime("%d"):
		startDay = dt.datetime.now().strftime("%d")
		messages.UpdateText(messages.text + f"{dt.datetime.now().strftime('------------------------------------------------  %d %B  %Y  ------------------------------------------------')}\n")

	onlineUsers.UpdateText(str(c.activeUsers))
	serverName.UpdateText(str(c.serverName))
	DrawLoop()


print(8)
Close()
