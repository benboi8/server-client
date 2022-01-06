import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


class Dot:
	def __init__(self, pos, radius, colors, spacing):
		self.pos = pos
		self.radius = radius
		self.backgroundColor = colors[0]
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]
		self.lineColor = colors[3]

		self.spacing = spacing

		self.currentColor = self.inactiveColor

		self.lines = {"top": False, "bottom": False, "left": False, "right": False}

		self.active = False

	def Draw(self):
		pg.draw.circle(screen, self.currentColor, self.pos, self.radius)
		pg.draw.circle(screen, self.backgroundColor, self.pos, self.radius / 1.3)

		if self.active:
			pg.draw.aaline(screen, self.currentColor, self.pos, pg.mouse.get_pos())

	def DrawLines(self):
		if self.lines["top"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1], self.radius, -self.spacing[1]), (self.lineColor, self.lineColor), roundness=3)

		if self.lines["bottom"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1], self.radius, self.spacing[1]), (self.lineColor, self.lineColor), roundness=3)

		if self.lines["left"]:
			DrawRoundedRect((self.pos[0], self.pos[1] - self.radius // 2, -self.spacing[0], self.radius), (self.lineColor, self.lineColor), roundness=3)

		if self.lines["right"]:
			DrawRoundedRect((self.pos[0], self.pos[1] - self.radius // 2, self.spacing[0], self.radius), (self.lineColor, self.lineColor), roundness=3)


		if self.lines["top"] and self.lines["bottom"]:
			pg.draw.rect(screen, self.lineColor, (self.pos[0] - self.radius / 1.9, self.pos[1] - self.radius // 2, self.radius * 1.1, self.radius))

		if self.lines["left"] and self.lines["right"]:
			pg.draw.rect(screen, self.lineColor, (self.pos[0] - self.radius // 2, self.pos[1] - self.radius / 1.9, self.radius, self.radius * 1.1))


		if self.lines["top"] and self.lines["right"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1] - self.radius // 2, self.radius, self.radius), (self.lineColor, self.lineColor), roundness=1)

		if self.lines["top"] and self.lines["left"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1] - self.radius // 2, self.radius, self.radius), (self.lineColor, self.lineColor), roundness=1)

		if self.lines["bottom"] and self.lines["right"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1] - self.radius // 2, self.radius, self.radius), (self.lineColor, self.lineColor), roundness=1)

		if self.lines["bottom"] and self.lines["left"]:
			DrawRoundedRect((self.pos[0] - self.radius // 2, self.pos[1] - self.radius // 2, self.radius, self.radius), (self.lineColor, self.lineColor), roundness=1)

	def HandleEvent(self, event):
		if self.IsPointColliding(pg.mouse.get_pos()):
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.active = True
					self.currentColor = self.activeColor

		if event.type == pg.MOUSEBUTTONUP:
			if event.button == 1:
				self.active = False
				self.currentColor = self.inactiveColor
				return True

		return False
				
	def IsPointColliding(self, point):
		pos = Vec2(self.pos[0], self.pos[1])
		return pos.GetEuclideanDistance(point) <= self.radius


class Player:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.moves = 1
		self.boxes = []


class Board:
	def __init__(self, rect, colors, numOfDots, players, radius=20):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]
		self.dotColors = colors[2]
		self.numOfDots = numOfDots

		self.radius = radius
		self.activeDot = None

		self.boxes = []

		self.players = []
		self.playerNumOfBoxs = []
		for i, p in enumerate(players):
			self.players.append(Player(p["name"], p["color"]))
			self.playerNumOfBoxs.append((Label((10, (i + 1) * 60, 260, 50), (self.backgroundColor, self.borderColor), text=f"Player {p['name']}: 0"), self.players[-1]))

		self.player = self.players[0]

		self.playerLabel = Label((10, 10, 260, 50), (self.backgroundColor, self.borderColor), text=f"If is player: {self.player.name}, turn.")

		self.CreateGrid()

	def CreateGrid(self):
		self.dots = [[Dot((self.rect.x + (((j + 1) * self.rect.w // self.numOfDots[0]) - (self.rect.w // self.numOfDots[0]) // 2), self.rect.y + (((i + 1) * self.rect.h // self.numOfDots[1]) - (self.rect.h // self.numOfDots[1]) // 2)), self.radius, (self.dotColors[0], self.player.color, self.dotColors[1], self.dotColors[2]), [self.rect.w // self.numOfDots[0], self.rect.h// self.numOfDots[1]]) for j in range(self.numOfDots[0])] for i in range(self.numOfDots[1])]

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 4)

		self.activeDot = None
		for row in self.dots:
			for dot in row:
				dot.inactiveColor = self.player.color
				if not dot.active:
					dot.currentColor = dot.inactiveColor
				dot.Draw()
				if dot.active:
					self.activeDot = dot
		
		if self.activeDot != None:
			self.activeDot.Draw()
		
		for row in self.dots:
			for dot in row:
				dot.DrawLines()

		for box in self.boxes:
			box.Draw()

		self.CheckForBoxes()

		if self.player.moves == 0:
			index = self.players.index(self.player) + 1
			if index != len(self.players):
				self.player = self.players[index]
			else:
				self.player = self.players[0]

			self.playerLabel.UpdateText(f"If is player: {self.player.name}, turn.")

			self.player.moves = 1

		for l in self.playerNumOfBoxs:
			l[0].UpdateText(f"Player {l[1].name}: {len(l[1].boxes)}")

	def HandleEvent(self, event):
		for row in self.dots:
			for dot in row:
				dot.HandleEvent(event)

		if self.activeDot != None:
			if self.activeDot.HandleEvent(event):
				for row in self.dots:
					for dot in row:
						if self.activeDot != dot:
							if dot.IsPointColliding(pg.mouse.get_pos()):
								if self.player.moves - 1 >= 0:
									if self.activeDot.pos[1] == dot.pos[1]:
										if Vec2(dot.pos[0], dot.pos[1]).GetEuclideanDistance(self.activeDot.pos) == self.activeDot.spacing[0]:					
											if self.activeDot.pos[0] < dot.pos[0]:
												self.activeDot.lines["right"] = True
												dot.lines["left"] = True
												self.player.moves -= 1
											
											elif self.activeDot.pos[0] > dot.pos[0]:
												self.activeDot.lines["left"] = True
												dot.lines["right"] = True
												self.player.moves -= 1

									elif self.activeDot.pos[0] == dot.pos[0]:
										if Vec2(dot.pos[0], dot.pos[1]).GetEuclideanDistance(self.activeDot.pos) == self.activeDot.spacing[1]:
											if self.activeDot.pos[1] < dot.pos[1]:
												self.activeDot.lines["bottom"] = True
												dot.lines["top"] = True
												self.player.moves -= 1
											elif self.activeDot.pos[1] > dot.pos[1]:
												self.activeDot.lines["top"] = True
												dot.lines["bottom"] = True
												self.player.moves -= 1

	def CheckForBoxes(self):
		for i, row in enumerate(self.dots):
			for j, dot in enumerate(row):
				if i + 1 != len(self.dots) and j + 1 != len(row):
					dot2 = self.dots[i + 1][j + 1]
					if dot.lines["right"] and dot.lines["bottom"] and dot2.lines["top"] and dot2.lines["left"]:
						box = Label((dot.pos[0], dot.pos[1], dot.spacing[0], dot.spacing[1]), (self.player.color, dot.lineColor), text=self.player.name, lists=[])
						inList = False
						for b in self.boxes:
							if box.rect.x == b.rect.x and box.rect.y == b.rect.y:
								inList = True

						if not inList:
							self.boxes.append(box)
							self.player.boxes.append(box)
							self.player.moves += 1


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	b.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	b.HandleEvent(event)



b = Board((width // 2 - height // 2, 0, height, height), (lightBlack, darkWhite, (black, white, white)), [10, 10], [{"name": "1", "color": red}, {"name": "2", "color": blue}, {"name": "3", "color": green}, {"name": "4", "color": orange}])


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
