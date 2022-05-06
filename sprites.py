import pygame as pg
import random, os
from constants import *
from img_processing import SpriteSheet

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

class Bird:
	def __init__(self, game, position):
		# self.radius =  15
		self.session = game
		self.colour = YELLOW
		self.position = pg.Vector2(position)
		self.velocity = pg.Vector2()
		self.size = (40, 25)
		self.curent_frame = 0
		self.spriteSH = SpriteSheet('assets/SprBird.png')
		self.all_frames = SpriteSheet.get_frames(274, 40, 1, 4)
		self.curent_img_org = self.spriteSH.get_image_from_sheet(*self.all_frames[self.curent_frame], colorkey=BLUE,  size=self.size)
		self.curent_img = self.curent_img_org

		# self.original_img = game.IMG.get_image('bird.png', size=self.size, colorkey=WHITE)
		# self.image = self.original_img

		self.gravity = pg.Vector2(0, GRAVITY)
		self.jumpVal = pg.Vector2(0, JUMP)

		self.smashed = False
		self.angle = 0
		self.incr = 1

	def update(self):
		self.position += self.velocity
		self.velocity += self.gravity 
	

		self.velocity.update(0, constrain(self.velocity.y, -11, 18))


		if self.position.y >= self.session.BG.ground_rect.y - self.size[1]:
			self.position.y = self.session.BG.ground_rect.y - self.size[1]
			self.session.playing = False


		if self.smashed:
			self.velocity.update(0, constrain(self.velocity.y, -1, 12))

		# rotating when falling
		if self.velocity.y < 0:
			self.angle += 12

		if self.velocity.y > 0:
			self.angle -= 3.5

		if pg.time.get_ticks() % 8 == 0:
			self.curent_frame += self.incr
			if self.curent_frame == 2:
				self.incr = - self.incr

			if self.incr < 0 and self.curent_frame == 0:
				self.incr = -self.incr

		self.curent_img_org_copy = self.spriteSH.get_image_from_sheet(*self.all_frames[self.curent_frame],  colorkey=BLUE,  size=self.size)
		self.curent_img = self.curent_img_org

		self.angle = constrain(self.angle, - 80 , 30)
		self.curent_img = pg.transform.rotate(self.curent_img_org_copy, self.angle)




	def draw(self, surf): 
		surf.blit(self.curent_img, (int(self.position.x),int(self.position.y)))

	def show_hitBox(self, surf):
		pg.draw.rect(surf, RED, (int(self.position.x),int(self.position.y), self.size[0], self.size[1]), 2)
		
	def jump(self):
		self.velocity += self.jumpVal

	def collides(self, pipe):
		if self.position.y >= pipe.b_position.y - self.size[1] or self.position.y <= pipe.t_position.y + pipe.pipe_height:  # bottom and top
			if self.position.x >= pipe.b_position.x - self.size[0] and self.position.x <= pipe.b_position.x + pipe.w:
				return True
		return False




class Pipe:
	def __init__(self, game):

		self.w = 78
		self.velocity = pg.Vector2( - game.game_velocity, 0)
		self.colour = WHITE
		self.game = game

		self.gap = GAP_SPACE
		self.pipe_height = HEIGHT - 100
		self.pipe_min_edge = 150
		self.pipe_max_edge = HEIGHT - game.BG.ground_rect.height - 50
	
		self.b_position = pg.Vector2(WIDTH + self.w, random.randint(self.pipe_min_edge, self.pipe_max_edge))
		self.t_position = pg.Vector2(WIDTH + self.w, self.b_position.y - self.gap - self.pipe_height)
		
		self.b_image = game.IMG.get_image('pipe.png', size=(self.w, self.pipe_height), colorkey=WHITE) # make
		self.t_image = game.IMG.get_image('pipe_mir.png', size=(self.w, self.pipe_height), colorkey=WHITE)

		# self.richPoint = pg.Rect(self.b_position.x + (self.w/2), self.t_position.y + self.pipe_height, 2, self.gap)
		self.riched = False


	def update(self):
		self.t_position += self.velocity
		self.b_position += self.velocity
		# self.richPoint.x += self.velocity.x
		
	def draw(self, surf):
	
		surf.blit(self.t_image, (int(self.t_position.x), int(self.t_position.y), self.w, self.pipe_height))
		surf.blit(self.b_image,  (int(self.b_position.x), int(self.b_position.y), self.w, self.pipe_height))

	def show_hitBox(self, surf):
		pg.draw.rect(surf, BLUE, (int(self.t_position.x), int(self.t_position.y), self.w, self.pipe_height), 3)
		pg.draw.rect(surf, RED, (int(self.b_position.x), int(self.b_position.y), self.w, self.pipe_height), 3)
		# pg.draw.rect(surf, RED, self.richPoint)
		

				

class PipeSystem:
	def __init__(self, game):
		self.game = game
		self.pipes = []
		self.cur_score = 0
		self.stopped = False

		self.waiting = False
		self.wait_time = 0
		self.last_update = 0

	def new(self):
		if not self.stopped and not self.waiting:
			self.pipes.append(Pipe(self.game))

	def update(self):
		now = pg.time.get_ticks()
		for p in self.pipes:
			p.update()

			if p.t_position.x < 0 - p.w:
				self.pipes.remove(p)

		if self.waiting:
			if now - self.last_update > self.wait_time:
				self.waiting = False
				self.last_update = now



	def draw(self, surf):
		for p in self.pipes:
			p.draw(surf)
			# p.show_hitBox(surf)


	def stop(self):
		self.stopped = True
		for p in self.pipes:
			p.velocity.update(0, 0)

	def wait(self, time):
		self.waiting = True
		self.wait_time = time
		
		



class Background:
	def __init__(self, game):
		self.bg_image = game.IMG.get_image('bg.png', size=(WIDTH, HEIGHT))
		self.speed = 0.1

		self.ground_img = game.IMG.get_image('ground.png', size=(WIDTH, HEIGHT//4))
		self.ground_rect = pg.Rect(0, HEIGHT - HEIGHT//5, self.ground_img.get_width(), HEIGHT//5)
		self.ground_rect2 =  pg.Rect(self.ground_img.get_width(), HEIGHT - HEIGHT//5, self.ground_img.get_width(), HEIGHT//5)
		
		self.velocity = game.game_velocity

	def update(self):
				
		if self.ground_rect.x <= self.ground_rect.width * - 1:
			self.ground_rect.x = self.ground_rect.width

		
		if self.ground_rect2.x <= self.ground_img.get_width() * -1:
			self.ground_rect2.x = self.ground_img.get_width()

		self.ground_rect.x -= self.velocity
		self.ground_rect2.x -= self.velocity


	def draw(self, surf):
		surf.blit(self.bg_image, (0, 0))
		

	def draw_ground(self, surf):
		surf.blit(self.ground_img, self.ground_rect)
		surf.blit(self.ground_img, self.ground_rect2)
		
		

	def stop(self):
		self.velocity = 0


class Button:
	def __init__(self, rect, **kwargs):
		self.rect = rect
		self.surface = pg.Surface((self.rect.width, self.rect.height))
		self.img = kwargs.get('img', None)
		self.h_img = kwargs.get('h_img', None)
		self.hovered = False

		if self.img:
			self.surface.blit(self.img, (0, 0))
		else:
			self.surface.fill(BLUE)


	def isHovered(self, butobj):
			mouse_pos = pg.mouse.get_pos()
			if mouse_pos[0] in range(butobj.x, butobj.x + butobj.width):
				if mouse_pos[1] in range(butobj.y, butobj.y + butobj.height):
					self.hovered = True					
					return True

			self.hovered = False
			return False

	def draw(self, surf):
		surf.blit(self.surface, self.rect)
		if self.hovered:
			if self.h_img:
				self.surface.blit(self.h_img, (0, 0))
		else:		
			if self.img:
				self.surface.blit(self.img, (0, 0))