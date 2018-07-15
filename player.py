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
		if self.left < 0:  # Если левая часть игрока за левой стенкой
			self.left = 0  # Переместить левую часть в левый край
		elif self.right > WINDOW_WIDTH:  # Если правая часть игрока за правой стенкой
			self.right = WINDOW_WIDTH  # Переместить правую часть игрока в правый край
		
		if self.top < 0:  # Если верхня часть игрока за верхней стенкой
			self.top = 0  # Переместить верхнюю часть в верхний край
		elif self.bottom > WINDOW_HEIGHT:  # Если нижняя часть игрока за нижней стенкой
			self.bottom = WINDOW_HEIGHT  # Переместить нижнюю часть в нижний край
	
	@property
	def right(self):  # Правая сторона
		return self.pos.x + PLAYER_WIDTH / 2  # Равна центру + половина ширины
	
	@right.setter
	def right(self, x):  # Для правой стороны
		self.pos.x = x - PLAYER_WIDTH / 2  # Центр левее на половину ширины
	
	@property
	def left(self):  # Левая сторона
		return self.pos.x - PLAYER_WIDTH / 2  # Равна центру - половна ширины
	
	@left.setter
	def left(self, x):  # Для левой стороны
		self.pos.x = x + PLAYER_WIDTH / 2  # Центр правее на половину ширины
	
	@property
	def top(self):  # Верхняя сторона
		return self.pos.y - PLAYER_HEIGHT / 2  # Равна центру - половину высоты
	
	@top.setter
	def top(self, y):  # Для верхней стороны
		self.pos.y = y + PLAYER_HEIGHT / 2  # Центр ниже на половину высоты
	
	@property
	def bottom(self):  # Нижняя сторона
		return self.pos.y + PLAYER_HEIGHT / 2  # Равна центру + половину высоты
	
	@bottom.setter
	def bottom(self, y):  # Для нижней стороны
		self.pos.y = y - PLAYER_HEIGHT / 2  # Центр выше на половину высоты
