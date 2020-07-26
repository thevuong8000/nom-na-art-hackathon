import pygame
import os
import time
import random
import math
import json
import cv2
import god

# Initialize 
pygame.font.init()
pygame.init()

# Create the screen
HIGHEST_SCORE = 0
SCREEN_HEIGHT = 600 
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# define size of objects
longX, longY = 125, 425
floor = 475
ninjas = []
polices = []
score = 0
lastTime = 0

# load images
# pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","pipe.png")).convert_alpha())
background = pygame.transform.scale(pygame.image.load(os.path.join("../images","background.jpg")).convert_alpha(), (800, 600))
pikalong_images = pygame.transform.scale(pygame.image.load(os.path.join("../images","pikalong.png")).convert_alpha(), (128, 100))
pikalong_images = pygame.transform.flip(pikalong_images, True, False)
base_img = pygame.transform.scale(pygame.image.load(os.path.join("../images","base.png")).convert_alpha(), (800, 180))
lead_image = pygame.transform.scale(pygame.image.load(os.path.join("../images","lead.png")).convert_alpha(), (180, 180))
lead_image = pygame.transform.flip(lead_image, True, False)
dictionary = pygame.transform.scale(pygame.image.load(os.path.join("../images","dictionary.png")).convert_alpha(), (64, 64))
dictframe = pygame.transform.scale(pygame.image.load(os.path.join("../images","dictframe.jpg")).convert_alpha(), (500, 500))
police_image = pygame.transform.scale(pygame.image.load(os.path.join("../images","police.png")).convert_alpha(), (80, 80))
MrKien_image = pygame.transform.scale(pygame.image.load(os.path.join("../images","ong_do.png")).convert_alpha(), (80, 80))

# set caption and icon
pygame.display.set_caption("PikaLong adventure")
icon = pygame.image.load('../images/icon.jpg')
icon = pygame.transform.scale(icon, (64, 64))
pygame.display.set_icon(icon)

# text font
OPENNING_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
GEN_FONT = pygame.font.SysFont("comicsans", 40)
WORD = pygame.font.SysFont("./simsun.ttc", 30)

class Obj:
	def __init__(self, Img, x, y):
		self.X = x
		self.Y = y
		self.Img = Img

	def render(self):
		screen.blit(self.Img, (self.X, self.Y))

class PikaLong(Obj):

	def __init__(self, Img, x, y):
		super().__init__(Img, x, y)
		self.VEL = 0

	def jump(self):
		if self.Y < longY:
			return
		self.VEL = 5

	def update(self):
		self.Y -= self.VEL
		if self.Y < longY:
			self.VEL -= 0.1
		if self.Y >= longY:
			self.Y = longY
			self.VEL = 0

class NinjaLead(Obj):
	def __init__(self, Img, x, y):
		super().__init__(Img, x, y)
		self.startTime = time.time()
		self.delay = random.random() * 5
		self.finish = False
		self.VEL = 4

	def move(self):
		if time.time() - self.startTime >= self.delay:
			self.X -= self.VEL 
			if self.X < -200:
				self.finish = True

	def collide(self, PikaLong):
		if self.finish:
			return False;
		x = self.X + 90
		y = self.Y + 90
		# pygame.draw.circle(screen, (0, 0, 0), (x, y), 50)
		pikaX = int(PikaLong.X + 64)
		pikaY = int(PikaLong.Y + 50)
		# pygame.draw.circle(screen, (0, 0, 0), (pikaX, pikaY), 50)
		distance = math.sqrt( ((x - pikaX)**2) + ((y - pikaY)**2) )
		if distance <= 100:
			return True
		return False

class Police(Obj):
	def __init__(self, Img, x, y):
		super().__init__(Img, x, y)
		self.startTime = time.time()
		self.delay = random.random() * 6 + 5
		self.finish = False
		self.VEL = 2

	def move(self):
		if time.time() - self.startTime >= self.delay:
			self.X -= self.VEL 
			if self.X < -200:
				self.finish = True

	def collide(self, PikaLong):
		if self.finish:
			return False;
		x = self.X + 40
		y = self.Y + 40
		# pygame.draw.circle(screen, (0, 0, 0), (self.X, self.Y), 50)
		pikaX = int(PikaLong.X + 64)
		pikaY = int(PikaLong.Y + 50)
		# pygame.draw.circle(screen, (0, 0, 0), (pikaX, pikaY), 50)
		distance = math.sqrt( ((x - pikaX)**2) + ((y - pikaY)**2) )
		return distance <= 60

class Base:
	VEL = 2
	WIDTH = base_img.get_width()
	IMG = base_img

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH - 10

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def render(self):
		screen.blit(self.IMG, (self.x1, self.y))
		screen.blit(self.IMG, (self.x2, self.y))

class ProfHanNom(Obj):
	def __init__(self, Img, x, y):
		super().__init__(Img, x, y)
		self.startTime = time.time()
		self.delay = random.random() * 5 + 10
		self.finish = False
		self.VEL = 2

	def move(self):
		if time.time() - self.startTime >= self.delay:
			self.X -= self.VEL 
			if self.X < -200:
				self.finish = True

	def collide(self, PikaLong):
		if self.finish:
			return False;
		x = self.X + 40
		y = self.Y + 40
		# pygame.draw.circle(screen, (0, 0, 0), (self.X, self.Y), 50)
		pikaX = int(PikaLong.X + 64)
		pikaY = int(PikaLong.Y + 50)
		# pygame.draw.circle(screen, (0, 0, 0), (pikaX, pikaY), 50)
		distance = math.sqrt( ((x - pikaX)**2) + ((y - pikaY)**2) )
		return distance <= 60

def AskQuestion():
	pos = god.getQuestion(knowledge)
	question = pygame.transform.scale(pygame.image.load(os.path.join("./","ques.png")).convert_alpha(), (512, 512))
	# screen.blit(question, (200, 200))
	return (question, pos)
	

def QuitGame():
	pygame.quit()
	quit()

data = god.data

knowledge = data[0:3]
# letters = {"text": '\u7684'}

def get_new_word():
	god.addWord(knowledge)
	render_dictionary()
	time.sleep(4)

def render_dictionary():
	god.getWord(knowledge)
	noti = pygame.transform.scale(pygame.image.load(os.path.join("./","res.png")).convert_alpha(), (512, 512))
	screen.blit(noti, (125, 100))
	pygame.display.update()

def end_screen():
	pikalong = PikaLong(pikalong_images, longX, longY)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False # break the loop
				QuitGame()
			elif event.type == pygame.KEYDOWN:
				if event.key == 27: # ESC press
					QuitGame()
				elif event.key == pygame.K_SPACE:
					main()
					break
		screen.blit(background, (0, 0))
		base = Base(floor)
		base.render()
		pikalong.render()
		text = END_FONT.render("Press SPACE to restart!!!", True, (255, 0, 0))
		screen.blit(text, (125, 300))
		pygame.display.update()


def main():
	global HIGHEST_SCORE

	# reset
	asking = None
	DictOpen = False
	DictRender = False
	ninjas = [NinjaLead(lead_image, SCREEN_WIDTH, 400)]
	polices = [Police(police_image, SCREEN_WIDTH, 400)]
	Mr_Kiens = [ProfHanNom(MrKien_image, SCREEN_WIDTH, 425)]
	threshold = 0.007
	score = 0
	lastTime = time.time()
	pikalong = PikaLong(pikalong_images, longX, longY)
	ans_pos = -1
	base = Base(floor)
	running = True

	ts = time.time()
	while running:
		addword = False
		if asking != None:
			screen.blit(asking, (100, 100))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False # break the loop
					QuitGame()
				elif event.type == pygame.KEYDOWN:
					lost = False
					print(event.key)
					if event.key == 27: # ESC press
						QuitGame()
					elif event.key == 120: # press X
						render_dictionary()
						time.sleep(2)
						continue
					elif event.key == ans_pos + 97:
						text = GEN_FONT.render("Good Job!!!", 1, (0, 0, 255))
					else:
						text = GEN_FONT.render("Game Over!!!", 1, (255, 0, 0))
						lost = True
					screen.blit(text, (400, 300))
					asking = None
					pygame.display.update()
					time.sleep(2)
					if lost:
						end_screen()
						return
						# QuitGame()
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False # break the loop
					QuitGame()
					
				elif event.type == pygame.KEYDOWN:
					if event.key == 27: # ESC press
						QuitGame()
					
					if event.key == pygame.K_SPACE:
						if DictOpen:
							DictOpen = False
							DictRender = False
						else:
							pikalong.jump()
					if event.key == 120: # press X
						if not DictOpen:
							DictOpen = True
							DictRender = False
						else:
							DictOpen = False
						
			# update characters if not stop
			if not DictOpen:
				screen.blit(background, (0, 0))
				if time.time() - lastTime >= 1:
					score += 1
					HIGHEST_SCORE = max(HIGHEST_SCORE, score)
					lastTime = time.time()
				score_text = GEN_FONT.render("SCORE: " + str(score), 1, (0, 0, 255))
				highest_score_text = GEN_FONT.render("HIGHEST SCORE: " + str(HIGHEST_SCORE), 1, (0, 0, 255))
				pikalong.update()
				base.move()
				for ninja in ninjas:
					ninja.move()
					if ninja.finish:
						ninjas.remove(ninja)
						if len(ninjas) == 0:
							ninjas.append(NinjaLead(lead_image, SCREEN_WIDTH, 400))
					if ninja.collide(pikalong) and asking is None:
						(asking, ans_pos) = AskQuestion()
						ninja.finish = True
				if len(ninjas) != 0:
					if ninjas[-1].X < SCREEN_WIDTH // 2:
						x = math.floor(random.random() * 4)
						if x == 0:
							ninjas.append(NinjaLead(lead_image, SCREEN_WIDTH, 400))
				
				for police in polices:
					police.move()
					if police.finish:
						polices.remove(police)
					if police.collide(pikalong) and asking is None:
						(asking, ans_pos) = AskQuestion()
						police.finish = True
					
				if len(polices) == 0:
					polices.append(Police(police_image, SCREEN_WIDTH, 400))

				for Mr_Kien in Mr_Kiens:
					Mr_Kien.move()
					if Mr_Kien.finish:
						Mr_Kiens.remove(Mr_Kien)
					if Mr_Kien.collide(pikalong):
						# knowledge = get_new_word()
						addword = True
						Mr_Kien.finish = True
				if len(Mr_Kiens) == 0:
					Mr_Kiens.append(Police(MrKien_image, SCREEN_WIDTH, 400))


				# render characters
				screen.blit(highest_score_text, (525, 30))
				screen.blit(score_text, (655, 60))
				screen.blit(dictionary, (20, 20))
				base.render()
				pikalong.render()
				for ninja in ninjas:
					ninja.render()
				for police in polices:
					police.render()
				for Mr_Kien in Mr_Kiens:
					Mr_Kien.render()
			if DictOpen and not DictRender:
				DictRender = True
				render_dictionary()

		if addword:
			get_new_word()
		pygame.display.update()	

		# if DictOpen:


		# Minh's intelligence
		while True:
			if time.time() - ts < threshold:
				continue
			ts = time.time()
			break

if __name__ == "__main__":
	main()