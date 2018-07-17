import pygame as pg


class Platform(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()  # Конструировани базового класса
		self.image = pg.image.load("./images/brick.png")  # Загрузка изображения кирпича
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.x = x  # Задание начальной координаты X из параметра
		self.rect.y = y  # Задание начальной координаты Y из параметра
