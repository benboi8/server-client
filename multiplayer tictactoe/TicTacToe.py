from clientMultiplayer import *

from GUI import *

import subprocess
import time

class Cell(Button):
	def __init__(self, rect, colors, onClick, onClickArgs):
		super().__init__(rect, colors, onClick=onClick, onClickArgs=onClickArgs, text="", name="", surface=screen, drawData={}, textData={"fontSize": 140}, inputData={}, lists=[])


class Board:
	def __init__(self, rect, colors):
		self.surface = screen
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]
		self.winColor = colors[3]
		self.colors = colors

		self.size = (3, 3)

		self.players = ["X", "O"]
		self.currentPlayer = self.players[0]

		self.score = {"X": 0, "O": 0}

		self.playerName = "Ben"
		self.won = False

		self.client = Client(details={"name": self.playerName})
		try:
			self.client.Start()
			self.connected = True
		except ConnectionRefusedError:
			self.connected = False


		if self.connected:
			self.Start()
		else:
			self.errorLabel = Label((0, 0, width, height), (self.backgroundColor, self.borderColor), text="No connection could be made to the server.")

	def CreateBoard(self):
		self.board = [[Cell(((i * self.rect.w // self.size[0]) + self.rect.x, (j * self.rect.h // self.size[1]) + self.rect.y, self.rect.w // self.size[0], self.rect.h // self.size[1]), self.colors, self.PlaceMove, [i, j]) for j in range(self.size[0])] for i in range(self.size[1])]

	def Start(self):
		self.player = self.players[0]
		self.playerLabel = Label((10, self.rect.y + self.rect.h // 2 - 160, 260, 100), (self.backgroundColor, self.borderColor), text=f"You are {self.player}.")
		
		self.currentPlayerLabel = Label((10, self.rect.y + self.rect.h // 2 - 50, 260, 100), (self.backgroundColor, self.borderColor), text=f"Player {self.currentPlayer} turn.")
		
		self.winnerLabel = Label((10, self.rect.y + self.rect.h // 2 + 60, 260, 100), (self.backgroundColor, self.borderColor), text=f"No winner.")
		
		self.restart = Button((width - 270, self.rect.y + self.rect.h // 2 - 50, 260, 100), self.colors, text="Restart", onClick=self.Restart)
		
		self.errorLabel = None
		
		self.messages = Label((self.rect.x + self.rect.w // 2 - 300, self.rect.y + self.rect.h // 2 - 200, 600, 400), (self.backgroundColor, self.borderColor), text=f"No other player found.\nInvite them to the server by giving them the IP\n\nIP: '{self.client.IP}'", lists=[])
		self.messageButton = Button((self.messages.rect.x + 10, self.messages.rect.y + self.messages.rect.h - 60, self.messages.rect.w - 20, 50), self.colors, text="Copy IP to clipboard.", onClick=self.CopyToClipboard, onClickArgs=[self.client.IP], lists=[])
		
		threading._start_new_thread(self.Receive, ())
		
		self.canPlay = len(self.client.serverDetails["activeUsers"]) == 2
		self.leadPlayer = None
		
		self.playerScore = Label((10, self.rect.y + self.rect.h // 2 - 270, 260, 100), (self.backgroundColor, self.borderColor), text=f"Your score: {self.score[self.player]}")
		self.opponentScore = Label((10, self.rect.y + self.rect.h // 2 + 170, 260, 100), (self.backgroundColor, self.borderColor), text=f"Opponent score: {self.score[self.players[self.players.index(self.player) - 1]]}")

		self.CreateBoard()

	def CopyToClipboard(self, txt):
		cmd = f"echo {txt.strip()} |clip"
		self.messageButton.UpdateText("IP copied to clipboard.")
		subprocess.check_call(cmd, shell=True)
		def ChangeMessageButtonText(self):
			time.sleep(5)
			self.messageButton.UpdateText("Copy IP to clipboard.")
		threading._start_new_thread(ChangeMessageButtonText, (self, ))

	def Draw(self):
		if self.connected:
			for row in self.board:
				for cell in row:
					cell.Draw()

			self.canPlay = len(self.client.serverDetails["activeUsers"]) == 2

			if not self.canPlay:
				self.messages.Draw()
				self.messageButton.Draw()

			else:
				self.Update()

		else:
			self.errorLabel.Draw()
			try:
				self.client.Start()
				self.connected = True
				self.Start()
			except ConnectionRefusedError:
				self.connected = False

		self.CheckWin()

	def Update(self):
		self.playerScore.UpdateText(f"Your score: {self.score[self.player]}")
		self.opponentScore.UpdateText(f"Opponent score: {self.score[self.players[self.players.index(self.player) - 1]]}")

		if self.leadPlayer != None:
			if self.leadPlayer != self.client.ID:
				self.player = self.players[1]
				self.playerLabel.UpdateText(f"You are {self.player}.")
		
		try:
			self.currentPlayer = self.client.data["currentPlayer"]
			self.currentPlayerLabel.UpdateText(f"Player {self.currentPlayer} turn.")

			self.leadPlayer = int(self.client.data["leadPlayer"])
		
		except KeyError:
			pass
		except TypeError:
			pass

		try:
			if self.client.data["restart"]:
				self.Restart(False)
		except KeyError:
			pass
		except TypeError:
			pass

		try:
			for key in self.client.data["boardState"]:
				i, j = key.split("-")

				self.board[int(j)][int(i)].UpdateText(self.client.data["boardState"][key])

			self.client.data["boardState"] = {}
			self.player = self.client.data["player"]

		except KeyError:
			pass
		except TypeError:
			pass

	def HandleEvents(self, event):
		if self.connected:
			if self.canPlay:
				for row in self.board:
					for cell in row:
						cell.HandleEvent(event)
			else:
				self.messageButton.HandleEvent(event)

	def PlaceMove(self, i, j):
		if self.canPlay:
			if not self.won:
				if self.player == self.currentPlayer:
					if self.board[i][j].text not in self.players:
						self.board[i][j].UpdateText(self.player)
						if self.currentPlayer == self.players[0]:
							self.currentPlayer = self.players[1]
						else:
							self.currentPlayer = self.players[0]

						self.UpdateClient()

						self.currentPlayerLabel.UpdateText(f"Player {self.currentPlayer} turn.")

	def Win(self, cells):
		if not self.won:
			self.score[cells[0].text] += 1
		for cell in cells:
			cell.ogBackgroundColor = self.winColor
			cell.backgroundColor = self.winColor
			self.winnerLabel.UpdateText(f"Winner is {cell.text}")
			self.won = True

	def Tie(self):
		self.winnerLabel.UpdateText(f"Tie")
		self.won = True

	def CheckWin(self):
		count = 0
		for row in self.board:
			for cell in row:
				if cell.text in self.players:
					count += 1
		if count == 9:
			self.Tie()

		# check horizontal
		for x in range(self.size[0]):
			cells = []
			if self.board[0][x].text in self.players:
				for y in range(3):
					if self.board[y][x].text == self.board[0][x].text:
						cells.append(self.board[y][x])

			if len(cells) >= 3:
				self.Win(cells)

		# check vertical
		for y in range(self.size[1]):
			cells = []
			if self.board[y][0].text in self.players:
				for x in range(3):
					if self.board[y][x].text == self.board[y][0].text:
						cells.append(self.board[y][x])

			if len(cells) >= 3:
				self.Win(cells)

		# check diagonal
		if self.board[0][0].text in self.players:
			cells = []
			for i in range(3):
				if self.board[i][i].text == self.board[0][0].text:
					cells.append(self.board[i][i])
			
			if len(cells) >= 3:
				self.Win(cells)

		if self.board[2][0].text in self.players:
			cells = []
			j = 0
			for i in range(2, -1, -1):
				if self.board[i][j].text == self.board[2][0].text:
					cells.append(self.board[i][j])
				j += 1					
			
			if len(cells) >= 3:
				self.Win(cells)
	
	def Restart(self, fromButton=True):
		self.currentPlayer = self.players[0]
		self.currentPlayerLabel.UpdateText(f"Player {self.currentPlayer} turn.")
		self.winnerLabel.UpdateText("No winner.")
		self.won = False
		self.CreateBoard()
		self.UpdateClient()
		if self.canPlay:
			if fromButton:
				self.client.RawSend({"restart": True})

	def Receive(self):
		if self.connected:
			while True:
				self.client.Receive()

	def UpdateClient(self):
		if self.connected:
			boardState = {}
			for i in range(self.size[0]):
				for j in range(self.size[1]):
					boardState[f"{i}-{j}"] = self.board[j][i].text

			self.client.RawSend({"name": self.playerName, "boardState": boardState, "leadPlayer": self.client.ID if self.leadPlayer == None else self.leadPlayer, "currentPlayer": self.currentPlayer})


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	b.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	b.HandleEvents(event)


b = Board((width // 2 - height // 2, 0, height, height), (lightBlack, darkWhite, lightRed, lightBlue))

while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	DrawLoop()
