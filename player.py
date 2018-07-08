import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):  # Наследование от спрайта pygame
	def __init__(self, x, y):  # Параметры: начальное местоположение по осям X и Y
		super().__init__()  # Конструирование базового класса
		self.image = pg.Surface(PLAYER_SIZE)  # Создание прямоугольного изображения
		self.image.fill(RED)  # Заливка изображения
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.center = (x, y)  # Задание координат центра
