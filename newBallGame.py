import pygame
import random
import math
from time import sleep

SMILE = None

#-----Constants-----

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)

SMILE_SIZE = None
BALL_RADIUS = 30

MOUSE_SPEED = 5


#-----Classes-----
class Ball():
	def __init__(self, pygame, gameDisplay):
		self.posx = 0
		self.posy = 0
		self.speedx = randSpdCalc()
		self.speedy = randSpdCalc()
		self.pygame = pygame
		self.gameDisplay = gameDisplay

	def update(self):
		# if the ball is past the sreen, it reverses direction
		if self.posx > DISPLAY_WIDTH or self.posx < 0:
			self.speedx = self.speedx * (-1)
		if self.posy > DISPLAY_HEIGHT or self.posy < 0:
			self.speedy = self.speedy * (-1)
		# updating positions with speed
		self.posx += self.speedx
		self.posy += self.speedy
		#drawing ball after update
		self.pygame.draw.circle(self.gameDisplay, WHITE, (self.posx, self.posy), BALL_RADIUS)

	def removeFromScreen(self):
		# moves ball off screen
		self.posx = DISPLAY_WIDTH + 100
		self.posy = DISPLAY_HEIGHT + 100
		self.pygame.draw.circle(self.gameDisplay, WHITE, (self.posx, self.posy), BALL_RADIUS)

	def getPos(self):
		return [self.posx, self.posy]

class BallList():
	def __init__(self, pygame, gameDisplay):
		self.pygame = pygame
		self.gameDisplay = gameDisplay
		self.numRuns = 0
		self.ball_list = []

	def addBall(self, _time):
		if (_time % 3 == 0 or _time == 0) and self.numRuns == 0:
			self.numRuns += 1
			self.ball_list.append(Ball(self.pygame, self.gameDisplay))
		elif _time % 3 != 0 and self.numRuns == 1:
			self.numRuns = 0

	def getBallList(self):
		return self.ball_list

class Time():
	def __init__(self, pygame):
		self.pygame = pygame
		self.time = self.pygame.time.get_ticks()/1000

	def update(self):
		self.time = self.pygame.time.get_ticks()/1000

	def getTime(self):
		return self.time

class Console():
	def __init__(self, pygame, bg_surface, gameDisplay):
		global SMILE
		global SMILE_SIZE

		self.pygame = pygame
		self.bg_surface = bg_surface
		self.gameDisplay = gameDisplay
		SMILE = self.pygame.image.load("./assets/smile.png") # smile.png from https://textfac.es
                SMILE_SIZE = SMILE.get_rect().size # creates rectangle around image and returns (width, height)

		self.mouseX = gameDisplay.get_width()
		self.mouseY = gameDisplay.get_height()
		# mouseXnew = 0
		# mouseYnew = 0
		self.mouseXchange = 0
		self.mouseYchange = 0

		self.ballData = BallList(self.pygame, self.gameDisplay)
		self.timeObject = Time(self.pygame)
		
		self.done = False
		self.clock = self.pygame.time.Clock()
		
	def move_up_event(self):
		self.mouseX = self.mouseX
		self.mouseY = self.mouseY - MOUSE_SPEED
	
	def move_down_event(self):
		self.mouseX = self.mouseX
		self.mouseY = self.mouseY + MOUSE_SPEED
	
	def move_left_event(self):
		self.mouseX = self.mouseX - MOUSE_SPEED
		self.mouseY = self.mouseY
	
	def move_right_event(self):
		self.mouseX = self.mouseX + MOUSE_SPEED
		self.mouseY = self.mouseY

	def update_all(self):
		self.mouseXchange = self.mouseX - SMILE_SIZE[0]/2
		self.mouseYchange = self.mouseY - SMILE_SIZE[1]/2
		self.timeObject.update()
		self.time = self.timeObject.getTime()

		self.ballData.addBall(self.time)

		self.gameDisplay.blit(self.bg_surface, (0,0))
		self.smilePosUpdate(self.mouseXchange, self.mouseYchange)
		self.displayScoreText(self.time, "current")
			
		for ball in self.ballData.getBallList():
			if collisionDetection(ball.getPos(), self.mouseX, self.mouseY) == True:
				#-----Game over-----
                		self.gameDisplay.blit(self.bg_surface, (0,0))
				self.gameOverText()
				self.displayScoreText(self.time, "current")
				self.pygame.display.update()
				self.done = True
				break
			else:
				ball.update()

		self.pygame.display.update()
		self.clock.tick(60)



	def smilePosUpdate(self,x,y):
		self.gameDisplay.blit(SMILE, (x,y))

	def gameOverText(self):
		font = pygame.font.Font(None, 100)
		text_surf = font.render("Game Over!", True, RED)
		self.gameDisplay.blit(text_surf, (220, 250))
		
	def displayScoreText(self, time, high_or_current):
		text_str = "Score: " + str(time)
		position = (DISPLAY_WIDTH - 125, 20)
		font = self.pygame.font.Font(None, 30)
		text_surf = font.render(text_str, True, WHITE)
		self.gameDisplay.blit(text_surf, position)
		
	# #-----Main function-----
	# def ball_game_run():


				# elif event.type == pygame.MOUSEMOTION:
				# 	(mouseXnew, mouseYnew) = pygame.mouse.get_pos()
				# 	mouseXchange = mouseXnew - mouseX - SMILE_SIZE[0]/2
				# 	mouseYchange = mouseYnew - mouseY - SMILE_SIZE[1]/2
#-----Global Methods-----
def randSpdCalc():
	speed = random.randint(7,17)
	if random.randint(1,2) == 1:
		speed *= -1
	return speed

def collisionDetection(ball_data, smile_x, smile_y):
	ball_x = ball_data[0]
	ball_y = ball_data[1]
	smile_radius = SMILE_SIZE[0]
	distance = math.sqrt((ball_x - smile_x)**2 + (ball_y - smile_y)**2)
	if distance <= (smile_radius + BALL_RADIUS):
		return True

#-----Calling main and quitting pygame-----
# ball_game_run()

# pygame.quit()
# quit()
