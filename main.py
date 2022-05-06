# ||FLAPPY BIRD|| - Game

# main file / lounch from here
import pygame as pg
import random, math, os
from constants import *
from sprites import *
from img_processing import *



class Game:

	def __init__(self):
		self.runing = True	

		# initialization pygame sounds and creat a windows
		pg.init()
		pg.mixer.init()
		pg.display.set_caption(GAME_NAME)
		pg.display.set_icon(pg.image.load(os.path.join("assets", "FlappyBird.ico")))
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		self.last_check = pg.time.get_ticks()
		self.font = pg.font.SysFont("monospace", 46)
		self.sprite_list = ['bird.png', 'coin.png', 'pipe.png', 'hoveredplaybut.png', 'playbut.png', 'ratebut.png', 'FBlable.png', 'pipe_mir.png', 'bg.png', 'ground.png', 'type_to.png']
		self.load_data()

		self.game_velocity = 8


	def load_data(self):
		img_dir = 'assets'
		self.dir = os.path.dirname(__file__)
		self.IMG = Images(img_dir, self.sprite_list)
		self.SPR_bird = SpriteSheet(os.path.join(img_dir, 'SprBird.png'))
		self.type_to_start = self.IMG.get_image('type_to.png', size=(200, 160), colorkey=YELLOW)

		



	def new(self):
		# start new game
			self.B = Bird(G, (WIDTH // 3, HEIGHT // 3))
			self.P = PipeSystem(G)
			self.BG = Background(G)
			self.score = 0
			self.game_velocity = 8
			
			self.run()

	def run(self):
		# Main loop
		self.wait_for_tap()

		if self.runing:
			self.playing = True
			while self.playing:
				self.clock.tick(FPS)
				self.events()
				self.update()
				self.draw()
				pg.display.flip()


	def update(self):
		# update sprites
		now = pg.time.get_ticks()
		self.B.update()
		self.P.update()
		self.BG.update()


		# make new pipe every 1000 frames
		if now - self.last_check > PIPE_RATE:
			self.last_check = now
			self.P.new()

		for p in self.P.pipes:
			if not p.riched and p.b_position.x <= self.B.position.x:
				p.riched = True
				self.score += 1


			if self.B.collides(p):
				self.P.stop()
				self.BG.stop()
				self.B.smashed = True



	def wait_for_tap(self):
		move_amplitude = 25
		angle = 0

		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.runing = False
					continue
					
				if event.type == pg.KEYUP:
					waiting = False
					self.B.jump()

			self.B.position.y = int(HEIGHT // 2.75 + math.sin(angle)*move_amplitude)
			angle += 0.125
			self.draw()		
			self.screen.blit(self.type_to_start, (CENTER[0] - 100, CENTER[1] - 80))	
			pg.display.flip()



	def show_gameover_screen(self):
		pass

	def show_score(self, score):
		text = str(score) 
		font_size = self.font.size(text)
		text_rnd = self.font.render(text, 1, WHITE)
		self.screen.blit(text_rnd,  (CENTER[0] - font_size[0] // 2, font_size[1]))
		

	def events(self):
		# Process input
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.runing = False

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE and not self.B.smashed:
					self.B.jump()

	def draw(self):
		# draw sprites
		self.BG.draw(self.screen)
		self.P.draw(self.screen)
		self.show_score(self.score)
		self.B.draw(self.screen)
		self.BG.draw_ground(self.screen)


	def show_start_screen(self):

		# button 
		playbut_size = (65, 30)
		playButton_rect = pg.Rect((WIDTH // 2 - 35 , HEIGHT // 2), playbut_size)
		playbutton_img = self.IMG.get_image('playbut.png', colorkey=RED, size=playbut_size)
		hoveredplaybut = self.IMG.get_image('hoveredplaybut.png', colorkey=BLUE, size=playbut_size)
		playButton = Button(playButton_rect, img=playbutton_img, h_img=hoveredplaybut)

		# lable
		Flappy_Bird_img = self.IMG.get_image('FBlable.png', size=(225, 100), colorkey=RED)
		bg = Background(G)


		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.runing = False
					continue

				if playButton.isHovered(playButton_rect):
					if event.type == pg.MOUSEBUTTONUP:
						waiting = False

					

			bg.update()
			bg.draw(self.screen)
			bg.draw_ground(self.screen)
			self.screen.blit(Flappy_Bird_img, (WIDTH // 2 - Flappy_Bird_img.get_width() // 2, HEIGHT // 2 - Flappy_Bird_img.get_height() * 2))
			playButton.draw(self.screen)
			pg.display.flip()








G = Game()
G.show_start_screen()
while G.runing:
	G.new()
	G.show_gameover_screen()

pg.quit()




