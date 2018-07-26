import pygame as pg


class Portal(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pg.image.load("./images/portal0.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
