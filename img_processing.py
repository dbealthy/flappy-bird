import pygame as pg
from constants import *
import os


class SpriteSheet:
	def __init__(self, file_name):
		self.spritesheet = pg.image.load(file_name).convert()

	def get_image_from_sheet(self, x, y, width, height, **kwargs):
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		size = kwargs.get('size', None)
		colorkey = kwargs.get('colorkey', None)
		if size:
			image = pg.transform.scale(image, size)
		if colorkey:
			image.set_colorkey(colorkey)

		return image

	@staticmethod	
	def get_frames(width, height, raws, columns):
		Swidth = width / columns
		Sheight = height / raws
		x = 0
		y = 0
		result = []
		for i in range(raws):
			y = i*Sheight
			for j in range(columns):
				x = j*Swidth
				result.append(tuple((x, y, Swidth, Sheight)))
		return result
	


class Images:
	def __init__(self, directory, img_list):
		self.images = {}
		for pic_name in img_list:
			full_path = os.path.join(directory, pic_name)
			pic_load = pg.image.load(full_path).convert()
			self.images.update({os.path.basename(pic_name) : pic_load})

	def get_image(self, name, **kwargs):
		img = self.images[str(name)]

		# adjust colorkey
		colorkey = kwargs.get('colorkey', WHITE)
		img.set_colorkey(colorkey)


		# adjust scale
		size = kwargs.get('size', None)
		if size:
			img = pg.transform.scale(img, size)
		return img


	def change_size(self, name, size):
		img = self.images[str(name)]
		pg.transform.scale(img, size)
