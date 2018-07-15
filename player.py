import pygame as pg
from settings import *
from vector import Vec2d as vec  # Подключение вектора


class Player(pg.sprite.Sprite):  # Наследование от спрайта pygame
	def __init__(self, x, y):  # Параметры: начальное местоположение по осям X и Y
		super().__init__()  # Конструирование базового класса
		self.image = pg.Surface(PLAYER_SIZE)  # Создание прямоугольного изображения
		self.image.fill(RED)  # Заливка изображения
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.center = (x, y)  # Задание координат центра
		self.vel = vec(0, 0)  # Вектор скоростей
		self.acc = vec(0, 0)  # Вектор ускорений
		self.pos = vec(x, y)  # Вектор местоположения игрока
	
	def update(self):
		self.acc = vec(0, 0)  # Задание ускорения вначале такта
		
		self.control_processing()
		
		self.physical_calculations()
		self.rect.center = self.pos  # Перемещение изображения в местоположение игрока

		self.wall_processing()

	def control_processing(self):  # Обработка нажатия клавиш управления
		keys = pg.key.get_pressed()  # Взятие словаря нажатых клавиш
		if keys[pg.K_LEFT]:  # Если нажато Влево
			self.acc.x = -PLAYER_ACC  # Задать ускорение по оси Х влево
		if keys[pg.K_RIGHT]:  # Если нажато Вправо
			self.acc.x = PLAYER_ACC  # Задать ускорение по оси Y вправо
			
	def physical_calculations(self):  # Физические расчеты
		self.acc -= self.vel * PLAYER_FRICTION  # Расчет ускорения от скорости и коэффициента трения
		self.vel += self.acc  # Усвеличение скорости от ускорения (v = v0 + a*t)
		self.pos += self.vel + self.acc / 2  # Перемещение от скорости и ускорения (x = x0 + v + a/2)
		
	def wall_processing(self):  # Отскакивание от стен
		if (self.pos.x - PLAYER_WIDTH/2) < 0:  # Если левая часть игрока за левой стенкой
			self.pos.x = 0 + PLAYER_WIDTH/2  # Переместить левую часть в левый край
		elif (self.pos.x + PLAYER_WIDTH/2) > WINDOW_WIDTH:  # Если правая часть игрока за правой стенкой
			self.pos.x = WINDOW_WIDTH - PLAYER_WIDTH/2  # Переместить правую часть игрока в правый край
		
		if (self.pos.y - PLAYER_HEIGHT/2) < 0:  # Если верхня часть игрока за верхней стенкой
			self.pos.y = 0 + PLAYER_HEIGHT/2  # Переместить верхнюю часть в верхний край
		elif (self.pos.y + PLAYER_HEIGHT/2) > WINDOW_HEIGHT:  # Если нижняя часть игрока за нижней стенкой
			self.pos.y = WINDOW_HEIGHT - PLAYER_HEIGHT/2  # Переместить нижнюю часть в нижний край
