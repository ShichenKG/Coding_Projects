# Author    : Jared Tauler
# Date      : 4/21/21
# Class     : AM
# Year      : Jr
# Assignment: 0042 - Finished Game

import math
import random
import pygame as pg
from pygame.locals import (
	RLEACCEL,
	K_w,
	K_s,
	K_a,
	K_d,
	K_SPACE,
	K_DOWN,
	MOUSEBUTTONDOWN,
	KEYDOWN,
	KEYUP,
	QUIT
)


class ClassPlayer(pg.sprite.Sprite):
	class ClassTurret(pg.sprite.Sprite):
		def __init__(self):
			pg.sprite.Sprite.__init__(self)

			self.Sprite = pg.image.load("image/gun1.png")
			self.Sprite = pg.transform.scale(self.Sprite, (120, 480))

			self.surf = self.Sprite
			self.rect = self.surf.get_rect()

			self.Target = 0

			self.rad = 0

			self.Tip = (0,0)


		def Refresh(self):
			self.rad = PointsToRad(pg.mouse.get_pos(), self.rect.center)
			self.surf = pg.transform.rotate(
				self.Sprite,
				RadToAngle(self.rad),
			)

			self.rect = self.surf.get_rect()

			# turret is not mounted at center of ship,
			# set the turrets center to be 21 pixels back from the center, taking the angle of the ship into account.
			d = -21
			self.rect.centerx = Player.rect.centerx + d*(math.cos(Player.Angle * (math.pi / 180)))
			self.rect.centery = Player.rect.centery + d*(math.sin(Player.Angle * (math.pi / 180)) * -1)

			# find tip of laser
			rad = self.rad
			d = -100
			x = self.rect.centerx + (d * math.sin(rad))
			y = self.rect.centery + (d * math.cos(rad))
			self.Tip = (x, y)


	def __init__(self):
		pg.sprite.Sprite.__init__(self)

		self.Sprite = pg.image.load("image/ship.png")
		self.Sprite = pg.transform.scale(self.Sprite, (86, 82))

		self.surf = self.Sprite
		self.rect = self.surf.get_rect()

		self.Score = 0

		self.Status = {"power": []}

		# Keep track of what keys are doing. Cant check for key being held because only get the event of key changing states.
		# This also holds {Key: State}.
		self.KeyState = {"order": []}

		self.Turret = False

		# Laser object
		self.Laser = pg.sprite.Sprite()
		self.Laser.state = 0
		self.Laser.surf = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)
		self.Laser.rect = self.Laser.surf.get_rect()
		self.Laser.points = [] # Points to draw laser


		self.Angle = 0

		self.rect.center = (100,100)

		self.Dead = False


	def InputHandle(self, event):
		# Keys
		if list(event.__dict__)[0] == "unicode":
			Key = event.key
			State = event.type
			# Keep track of what keys are pressed. Their order in the list is important.
			for i,j in enumerate(self.KeyState["order"]):
				if j==Key:
					self.KeyState["order"].pop(i)

			if State == KEYDOWN:
				self.KeyState[Key] = True
				self.KeyState["order"].append(Key)

			else:
				self.KeyState[Key] = False

		# Mouse
		elif list(event.__dict__)[0] == "pos":
			if self.Laser.state == -10: # Only fire if not firing.
				self.Laser.state = 5

				d = -10000  # distance laser will go, 10000 isnt used for any particular reason.
				rad = self.Turret.rad
				a = Cursor.rect.center
				x = a[0] + (d * math.sin(rad))
				y = a[1] + (d * math.cos(rad))

				self.Laser.points = [self.Turret.Tip, (x, y)]


	def Refresh(self):
		Speed = 5
		Dir = {"x": 0, "y": 0}

		# Direction Keys that were pressed last override keys before it.
		# If you push 2 opposing direction keys, you will go in direction last pushed.
		for i in self.KeyState["order"]:
			if i == KEYS["left"] and self.KeyState[KEYS["left"]]: Dir["x"] = 1
			elif i == KEYS["right"] and self.KeyState[KEYS["right"]]: Dir["x"] = -1
			elif i == KEYS["up"] and self.KeyState[KEYS["up"]]: Dir["y"] = 1
			elif i == KEYS["down"] and self.KeyState[KEYS["down"]]: Dir["y"] = -1


		if self.Dead:
			if self.KeyState["order"] != []:
				self.Dead = False
			else: return
		for i in [self, self.Turret, Cursor]: screen.blit(i.surf, i.rect)

		# Turn
		if Dir["x"] != 0:
			self.Angle += Dir["x"] * 2
			self.surf, self.rect = rot_center(self.Sprite, self.Angle, self.rect)
			if self.Angle > 360: self.Angle -= 360
			elif self.Angle < 0: self.Angle += 360

		# Move
		if Dir["y"] != 0:
			if Dir["y"] == 1: Speed = 5
			elif Dir["y"] == -1: Speed = -3

			x = Speed*math.cos(self.Angle*(math.pi/180))
			y = Speed*(math.sin(self.Angle*(math.pi/180))*-1)

			# Check if center of player will go out of bound before moving.
			if self.rect.centerx + x >= 0 and \
			self.rect.centerx + x <= screen.get_size()[0]:
				self.rect.x += x

			if self.rect.centery + y >= 0 and \
			self.rect.centery + y <= screen.get_size()[1]:
				self.rect.y += y

		# Enemy collision
		if self.rect.collidelist([i for i in GroupENEMY.sprites()]) > -1: # Check if overlapping any enemy rects
			# create a mask of self. constantly rotating so no need to make a mask unless checking collision.
			self.mask = pg.mask.from_surface(self.surf)

			for i in self.rect.collidelistall([i for i in GroupENEMY.sprites()]): # For every colliding enemy,

				# pg.sprite.collide_mask returns where collision happens. if none, no collision
				if pg.sprite.collide_mask(self, GroupENEMY.sprites()[i]) is not None:
					self.rect.center = [i/2 for i in pg.display.get_window_size()] # send to center of screen
					self.Laser.state = 0

					for i in GroupENEMY: i.kill() # kill all enemies

					# Write high score
					if self.Score != 0: ScoreWrite(self.Score)
					self.Score = 0

					self.Dead = True
					self.KeyState["order"] = [] # Clear input
					self.ScoreSurf = ScoreSurfMake()

					break


		# Turret stuff
		if self.Turret is not False:
			self.Turret.Refresh()

			if self.Laser.state > 0:
				self.Laser.surf = pg.surface.Surface(pg.display.get_window_size(), pg.SRCALPHA)

				a = self.Laser.points # remember points laser goes across
				pg.draw.line(
					self.Laser.surf, (255, 255, 255),a[0], a[1], self.Laser.state
				)
				screen.blit(self.Laser.surf, (0,0))
				self.Laser.mask = pg.mask.from_surface(self.Laser.surf)


				self.Laser.state -= 1
				net = 0
				for i in GroupENEMY:
					if pg.sprite.collide_mask(self.Laser, i) is not None:
						# More enemies killed with one laser gives exponentially more points.
						if net == 0: net += 1
						else: net *= 2
						i.kill()

				self.Score += net

			elif self.Laser.state == -10: pass
			else: self.Laser.state -= 1


	def Event(self, event):
		if event == "turret":
			if "turret" not in self.Status["power"]:
				self.Turret = self.ClassTurret()
				GroupALL.add(self.Turret)
				self.Status["power"].append("turret")


class ClassCursor(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)

		self.Sprite = {}
		self.Sprite["None"] = pg.image.load("image/cursor.png")
		self.Sprite["None"] = pg.transform.scale(self.Sprite["None"], (100, 100))

		self.Sprite["laser"] = pg.image.load("image/cursor_laser.png")
		self.Sprite["laser"] = pg.transform.scale(self.Sprite["laser"], (80, 80))

		self.Sprite["no"] = pg.image.load("image/cursor_no.png")
		self.Sprite["no"] = pg.transform.scale(self.Sprite["no"], (80, 80))

		self.surf = self.Sprite["None"]

		self.rect = self.surf.get_rect()

		self.angle = 0

		self.Type = None

		self.ChangeType("laser")

	def rot_center(self, image, angle, x, y):

		rotated_image = pg.transform.rotate(image, angle)
		new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

		return rotated_image, new_rect

	def Refresh(self):
		self.rect.center = pg.mouse.get_pos()
		if self.Type == "laser":
			# Try to mitigate the cursor having seizure when too close to player
			for i in [Player.Turret.Tip, Player.rect.center]:
				x = pg.mouse.get_pos()[0] - i[0]
				y = pg.mouse.get_pos()[1] - i[1]

				# make not negative if negative
				if x < 0: x *= -1
				if y < 0: y *= -1

				if x < 50 and y < 50:
					self.surf = self.Sprite["no"]
					return # exit refresh if too close

				else:
					if self.surf is not self.Sprite["no"]: self.surf = self.Sprite["laser"]

			self.angle = RadToAngle(
				PointsToRad(
					Player.Turret.Tip, pg.mouse.get_pos()
				),
			)

			self.surf, self.rect = rot_center(self.surf, self.angle, self.rect)


		else:
			self.angle += 2.2

			self.surf, self.rect = rot_center(self.Sprite["None"], self.angle, self.rect)

			if self.angle > 360: self.angle -= 360 # feel like it might explode if i let number get too high.

	def ChangeType(self, type):
		if type == "laser":
			self.Type = "laser"
			self.surf = self.Sprite["laser"]

		if type == None:
			self.Type = None


class ClassUFO(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)

		self.Costume = []
		self.Costume.append(pg.transform.scale(
			pg.image.load("image/ufo1-1.png"), (86, 56))
		)
		self.Costume.append(pg.transform.scale(
			pg.image.load("image/ufo1-2.png"), (86, 56))
		)

		self.surf = self.Costume[0]
		self.mask = pg.mask.from_surface(self.surf)
		self.rect = self.surf.get_rect()

		self.MoveRelY = 1
		self.MoveDir = 1
		self.MoveCount = 1

		self.negative = random.choice([True, False])

		self.Speed = random.randint(2, 3) * (-1 if self.negative else 1)

		if self.negative: self.rect.x = 0 - self.surf.get_rect()[2]
		else: self.rect.x = pg.display.get_window_size()[0] + self.surf.get_rect()[2]

		self.rect.y = random.randint(
			0,
			pg.display.get_window_size()[1] - self.surf.get_rect()[3]
		)

		# Remember the UFO's y value in which it revolves around, y=0 on the wave
		self.true_y = self.rect.y

		# random flight path
		self.ModHeight = random.randint(100,180)
		self.ModSpeed = random.randint(40,80)

	def Refresh(self):
		# Change costume whenever tick is even or odd
		if TICK % 2 == 0: x = 0
		else: x = 1

		if self.surf != self.Costume[x]:
			self.surf = self.Costume[x]

		# Calculate UFO's Y value.
		a=self.ModHeight # wave height, how high up UFO goes up and down
		h=self.rect.x # displaces wave on X axis, cant think of a better way to describe.
		b=self.ModSpeed # closeness of waves, speed in which UFO goes up and down
		k= self.true_y # "line" in which UFO revolves around
		self.rect.y = a*(math.sin(h/b))+k

		self.rect.x -= self.Speed

		if self.rect.x < 0 - self.surf.get_size()[0]: self.kill()
		elif self.rect.x > self.surf.get_size()[0] + pg.display.get_window_size()[0]: self.kill()


# Background is a surface i draw to
class ClassBG:
	class Body: # Celestial bodies
		def __init__(self, sprite, angle=None, startY=None, startX=None, speed=0,):
			self.Speed = speed

			if angle is None: angle = random.randint(0, 360)
			else: self.angle = angle

			#change size relative to speed
			a = sprite
			b = speed*2
			a = pg.transform.scale(a, (b,b))
			self.surf = pg.transform.rotate(a, angle)

			if startX is None:
				# Dont start too far right by subtracting height of rectangle from places available to go start at
				startX = random.randint(
					0,
					pg.display.get_window_size()[0] - self.surf.get_rect()[2]
				)

			# Start at bottom of screen, + the Y dimension of the body.
			if startY is None: startY = pg.display.get_window_size()[1]
			else: startY = startY # dont make if a startY is given.

			self.Pos = [startX, startY]

		def Refresh(self, surf):
			self.Pos[1] -= self.Speed
			surf.blit(self.surf, self.Pos)


		# Check if the object can be deleted.
		def Dead(self):
			# Check against 0 - the Y dimension of the rectangle.
			# This is so it is destroyed as soon as it's out of view, rather than when it's Y position = 0.
			if self.Pos[1] <= 0 - self.surf.get_rect()[3]: return True


	def __init__(self):
		self.surf_BG = pg.Surface(pg.display.get_window_size())
		# Draw background same size as window rectangle and color it.

		self.surf_Star = pg.image.load("image/star1.png")
		self.Bodies = []


	def Refresh(self):
		if random.randint(0, 20) == 1 and len(self.Bodies) < 20:
			self.Bodies.append(self.Body(self.surf_Star, speed=random.randint(5,30)))

		# Draw a new rectangle to put all the stars on
		pg.draw.rect(
			self.surf_BG, (0, 0, 50), pg.Rect(
				self.surf_BG.get_rect()
			)
		)

		# Update every body before checking what needs to be deleted.
		# Order will get messed up if refresh and kill are in same loop.
		dead = []
		for i in self.Bodies:
			i.Refresh(self.surf_BG)
			if i.Dead(): dead.append(i)

		for i in dead: self.Bodies.remove(i)


# Find radian from 2 points.
def PointsToRad(x, y):
	a = y[0] - x[0]
	b = y[1] - x[1]

	# Find radian from difference
	rad = math.atan2(a, b)

	return rad


# Radian to angle.
def RadToAngle(rad): return (rad / math.pi * 180) + (0 if rad > 0 else 360)


# rotate an image around its center.
def rot_center(image, angle, rect):
	surf = pg.transform.rotate(image, angle)
	rect = surf.get_rect(center=image.get_rect(center=rect.center).center)
	return surf, rect


# Read highscore files
def ScoreRead():
	try: f = open("score.txt", "r")
	except: f = open("score.txt", "w+")

	l = []
	for i in f.readlines():
		# Get rid of breaks.
		string = ""
		for j in i:
			if j.isnumeric(): string += str(j)

		l.append(int(string))

	f.close()
	print(l)
	return l


# update list of hihgscores
def ScoreWrite(new):
	score = ScoreRead()
	broke = False
	for i, j in enumerate(score):
		if new >= j:
			score.insert(i, new)
			broke = True
			break
	if not broke: score.append(new)

	score = [i for i in score[0:5]]
	f = open("score.txt", "w+")
	f.writelines([str(i)+"\n" for i in score])
	f.close() #update


# make highscore surf
def ScoreSurfMake():
	a = ScoreRead()
	if a == []:
		score = FONT.render(
			"No high scores",
			True,
			(255, 255, 255)
		)
		a = pg.display.get_window_size()
		x = (a[0] / 2) - (score.get_width() / 2)
		y = (a[1] / 2) - (score.get_height() / 2)
		return {"surf": score, "dest": (x, y)}

	score = FONT.render(
		"High scores",
		True,
		(255, 255, 255)
	)

	for i in a: # for every high score
		# generate surf with font
		b = FONT.render(
			str(i),
			True,
			(255, 255, 255)
		)

		# find how big (last surf + just made surf) will be
		surf = pg.Surface((score.get_width(), score.get_height() + b.get_height()), pg.SRCALPHA)

		surf.blit(score, (0, 0)) # blit last surf
		surf.blit(b, (score.get_width() / 2 - b.get_width() / 2, score.get_height())) #blit next surf

		score = surf

	a = pg.display.get_window_size()
	x = (a[0] / 2) - (surf.get_width() / 2)
	y = (a[1] / 2) - (surf.get_height() / 2)

	return {"surf": surf, "dest": (x, y)}


#### Main Program ####
running = True

# Controls
KEYS = {
	"left": K_a,
	"right": K_d,
	"up": K_w,
	"down": K_s,
	# "event": K_SPACE, #temporary
}

pg.init()

clock = pg.time.Clock()
screen= pg.display.set_mode((1200, 800))
pg.time.set_timer(pg.USEREVENT, 500)

warndown = pg.transform.scale(pg.image.load("image/warndown.png"), (78, 68))
warnup = pg.transform.scale(pg.image.load("image/warnup.png"), (78, 68))
FONT = pg.font.SysFont("comicsans", 30)

pg.mouse.set_visible(False)

BG = ClassBG()

Player = ClassPlayer()
Cursor = ClassCursor()

GroupALL = pg.sprite.Group()
GroupENEMY = pg.sprite.Group()
GroupUFO = pg.sprite.Group()
GroupPARTICLE = pg.sprite.Group()

GroupALL.add(Player, Cursor)

Player.Event("turret") # temporary

TICK = 0

while running:
	# Input
	for event in pg.event.get():
		if event.type == pg.USEREVENT:
			TICK += 1
		elif event.type in [KEYDOWN, KEYUP] and event.key in KEYS.values() or event.type == MOUSEBUTTONDOWN:
			Player.InputHandle(event)
		elif event.type == QUIT: quit()

	keys = pg.key.get_pressed() # checking pressed keys

	# BG
	BG.Refresh()
	screen.blit(BG.surf_BG, (0, 0))

	# Sprites
	if Player.Dead is False:
		if len(GroupENEMY) <= 20:
			if random.randint(0, 50) == 0:
				x = ClassUFO()
				for i in [GroupUFO,GroupENEMY,GroupALL]: i.add(x)


	for i in GroupENEMY.sprites():
		i.Refresh()

	for i in [Cursor, Player]: i.Refresh() # Refresh,

	# If any enemies are out of screen view, blit a warning icon.
	for i in GroupENEMY:
		y = i.rect.y
		x = i.rect.x

		if y < (0 - i.surf.get_rect()[3]):  # check for above
			screen.blit(
				warnup,
				(
					i.rect.centerx - warnup.get_rect().centerx,
					0
				)
			)

			# Number isnt meant to be thought about by player, the color of it is.
			distance = abs(y - (0 - i.surf.get_rect()[3]))  # calculate distance

			# change color
			if distance < 60: color = (255, 0, 0)
			elif distance > 120: color = (0, 255, 0)
			else: color = (255, 255, 255)

			x = str(distance * 137)
			x = "".join("0" for i in range(len(x), 5)) + x
			text = FONT.render(
				x,
				True, color
			)

			screen.blit(
				text,
				(
					i.rect.centerx - warndown.get_rect().centerx,
					warndown.get_rect()[3]
				)
			)

		elif y > (pg.display.get_window_size()[1]):
			screen.blit(
				warndown,
				(
					i.rect.centerx - warndown.get_rect().centerx,
					pg.display.get_window_size()[1] - warndown.get_rect()[3]
				)
			)
			distance = y - pg.display.get_window_size()[1]

			if distance < 60: color = (255, 0, 0)
			elif distance > 120: color = (0, 255, 0)
			else: color = (255, 255, 255)

			x = str(distance * 137)
			x = "".join("0" for i in range(len(x), 5)) + x
			text = FONT.render(
				x,
				True, color
			)

			screen.blit(
				text,
				(
					i.rect.centerx - warndown.get_rect().centerx,
					pg.display.get_window_size()[1] - (warndown.get_rect()[3] + text.get_rect()[3])
				)
			)

	for entity in GroupUFO: screen.blit(entity.surf, entity.rect) # Blit

	# SCORE
	if Player.Dead is False:
		screen.blit(
			FONT.render("SCORE: " + str(Player.Score),
						True,
						(255,255,255)
						),
			(0,0)
		)

	# Show high scores
	else: screen.blit(Player.ScoreSurf["surf"], Player.ScoreSurf["dest"])

	pg.display.update()

	clock.tick(60)
