import pygame as pg
from settings import *


class Platform(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()  # Конструировани базового класса
		self.image = pg.image.load("./images/brick.png")  # Загрузка изображения кирпича
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.x = x  # Задание начальной координаты X из параметра
		self.rect.y = y  # Задание начальной координаты Y из параметра
		self.lines = self.create_lines()
	
	def create_lines(self):  # Создание словаря линий
		# Каждая линия является прямоугольником толщиной в один пиксель и длиной в сторону квадрата, но с учетом пустых углов
		lines = dict(
				# Верхняя линия начинается в левом верхнем углу со сдвигом вправо на пустой угол
				# и имеет длину = сторона квадрата - пустой угол*2,
				# т.е. заканчивается на один пустой угол левее от правого верхнего угла
				# Т.к. толщина прямоугольника = 1, получаем линию.
					top = pg.Rect(self.rect.left + PLATFORM_EMPTY_CORNER, self.rect.top,
		                           PLATFORM_WIDTH - PLATFORM_EMPTY_CORNER * 2, 1),
		        # Следующие линии по аналогии
		            bottom = pg.Rect(self.rect.left + PLATFORM_EMPTY_CORNER, self.rect.bottom,
		                              PLATFORM_WIDTH - PLATFORM_EMPTY_CORNER * 2, 1),
		            left = pg.Rect(self.rect.left, self.rect.top + PLATFORM_EMPTY_CORNER, 1,
		                            PLATFORM_HEIGHT - PLATFORM_EMPTY_CORNER * 2),
		            right = pg.Rect(self.rect.right, self.rect.top + PLATFORM_EMPTY_CORNER, 1,
		                             PLATFORM_HEIGHT - PLATFORM_EMPTY_CORNER * 2))
		return lines
	
	# Свойства платформы
	# Сторона платформы соответствует стороне прямоугольника
	@property
	def right(self):
		return self.rect.right
	
	@property
	def left(self):
		return self.rect.left
	
	@property
	def top(self):
		return self.rect.top
	
	@property
	def bottom(self):
		return self.rect.bottom
