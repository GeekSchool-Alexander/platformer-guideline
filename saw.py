import pygame as pg
from settings import *
from vector import Vec2d as vec

class Saw(pg.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.frames = (
		pg.image.load("./images/saw0.png"),
		pg.image.load("./images/saw1.png"),
		pg.image.load("./images/saw2.png"),
		pg.image.load("./images/saw3.png"),
		pg.image.load("./images/saw4.png"),
		pg.image.load("./images/saw5.png"),
		pg.image.load("./images/saw6.png"),
		pg.image.load("./images/saw7.png"))  # Загружаем в кортеж с кадрами все изображения для анимации
		self.current_frame = 0  # Индекс текущего кадра анимации
		self.last_update = pg.time.get_ticks()  # Время последней смены кадра; Изначально равен моменту создания пилы
		self.image = self.frames[self.current_frame]  # Текущее изображение из кортежа кадров по текущему индексу
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.x = x  # Задание начальной координаты X из параметра
		self.rect.y = y  # Задание начальной координаты Y из параметра
	
	def update(self):
		self.animate()
	
	def animate(self):  # Анимация движения
		now = pg.time.get_ticks()  # Берем текущее время
		if now - self.last_update >= SAW_ANIMATE_DELAY:  # Если с последней смены кадра прошла длительность периода
			self.last_update = now  # Временем последней смены кадра будет текущий момент
			self.current_frame += 1  # Индекс кадра сменяем на следующий
			# Кадры сменяются циклично:
			if self.current_frame >= len(self.frames):  # Если вышли за границу кортежа с кадрами
				self.current_frame = 0  # Возвращаемся в начало кортежа
			# По расчитаному индексу достаем кадр и используем как изображение для текущего такта
			self.image = self.frames[self.current_frame]


class FlyingSaw(Saw):
	def __init__(self, x, y, direction):
		super().__init__(x, y)
		self.vel = self.generate_speed(direction)  # Задание скорости движения
	
	def generate_speed(self, direction):  # Генерация скорости движения на основе направления
		if isinstance(direction, str):  # Проверяем что направление - строка
			vel = vec(0, 0)  # Заготовка вектора скорости
			if direction == "up":
				vel = vec(0, -SAW_SPEED)
			elif direction == "down":
				vel = vec(0, SAW_SPEED)
			elif direction == "left":
				vel = vec(-SAW_SPEED, 0)
			elif direction == "right":
				vel = vec(SAW_SPEED, 0)
			else:  # Если направление не одно и четырёх, оно неверное; ValueError
				raise ValueError("Invalid direction")
			return vel  # Возвращаем полученную скорость
		else:  # Иначе TypeError
			raise TypeError("Direction must be str")
	
	def update(self):
		self.animate()  # Анимация
		# Перемещение
		self.rect.x += self.vel.x
		self.rect.y += self.vel.y
