import pygame as pg
from settings import *
from vector import Vec2d as vec  # Подключение вектора
import time


class Player(pg.sprite.Sprite):  # Наследование от спрайта pygame
	def __init__(self, x, y, game):  #
		"""Параметры:
		Начальное местоположение по осям X и Y
		Cсылка на игру, в которой находится игрок"""
		super().__init__()  # Конструирование базового класса
		self.frames = (
		pg.image.load("./images/ball0.png"),
		pg.image.load("./images/ball1.png"),
		pg.image.load("./images/ball2.png"),
		pg.image.load("./images/ball3.png"),
		pg.image.load("./images/ball4.png"),
		pg.image.load("./images/ball5.png"),
		pg.image.load("./images/ball6.png"),
		pg.image.load("./images/ball7.png"))  # Загружаем в кортеж с кадрами все изображения для анимации
		self.current_frame = 0  # Индекс текущего кадра анимации
		self.last_update = pg.time.get_ticks()  # Время последней смены кадра; Изначально равен моменту создания игрока
		self.image = self.frames[self.current_frame]  # Текущее изображение из кортежа кадров по текущему индексу
		self.rect = self.image.get_rect()  # Взятие прямоугольника
		self.rect.center = (x, y)  # Задание координат центра
		self.vel = vec(0, 0)  # Вектор скоростей
		self.acc = vec(0, 0)  # Вектор ускорений
		self.pos = vec(x, y)  # Вектор местоположения игрока
		self.game = game  # Сохранене ссылки на игру
		self.on_ground = False  # Изначально не на земле
	
	def update(self):
		# Задание ускорения вначале такта
		self.acc = vec(0, PLAYER_GRAVITY)  # По оси Y воздействует ускорение свободного падения
		
		self.control_processing()
		
		self.physical_calculations()
		self.collide_processing()
		self.rect.center = self.pos  # Перемещение изображения в местоположение игрока

		self.wall_processing()
		self.animate()

	def control_processing(self):  # Обработка нажатия клавиш управления
		keys = pg.key.get_pressed()  # Взятие словаря нажатых клавиш
		if keys[pg.K_LEFT]:  # Если нажато Влево
			self.acc.x = -PLAYER_ACC  # Задать ускорение по оси Х влево
		if keys[pg.K_RIGHT]:  # Если нажато Вправо
			self.acc.x = PLAYER_ACC  # Задать ускорение по оси Y вправо
		if keys[pg.K_UP]:  # Если нажато Вверх
			self.jump()  # Прыгнуть
	
	def jump(self):  # Прыжок
		if self.on_ground:  # Если на земле
			self.vel.y = -PLAYER_JUMP  # Дать импульс вверх
	
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
	
	def collide_processing(self):  # Обработка столкновений
		# Столкновение с платформами:
		self.on_ground = False  # Вначале такта не на земле
		# Взятие списка платформ, с которыми произошло столкновение
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits:  # Если столкновение есть
			collides = dict()  # Словарь столкновений;
			for platform in hits:  # Для всех платформ, с которыми проихзошло столкновение
				for side, plat_rect in platform.lines.items():  # Для всех граней платформы из словаря линий
					if self.rect.colliderect(plat_rect):  # Если столкновение именно с этой линией
						collides[side] = plat_rect  # Сохраняем название грани и линию в словарь столкновений
			
			if "top" in collides:  # Если столкновение с верхней линией платформы
				self.vel.y = 0  # Останавливаемся
				self.bottom = collides["top"].top  # Размещаем игрока над платформой
				self.on_ground = True  # Игрок на земле
			elif "bottom" in collides:  # Если столкновение с нижней линией платформы
				self.vel.y = 0  # Останавливаемся
				self.top = collides["bottom"].bottom  # Размещаем игрока под платформу
			elif "left" in collides:  # Если столкновение с левой линией платформы
				self.vel.x = 0  # Останавливаемся
				self.right = collides["left"].left  # Размещаем игрока слева от платформы
			elif "right" in collides:  # Если столкновение с правой линией платформы
				self.vel.x = 0  # Останавливаемся
				self.left = collides["right"].right  # Размещаем игрока справа от платформы
		
		# Столкновение с пилами:
		hits = pg.sprite.spritecollide(self, self.game.saws, False)
		if hits:  # Если есть столкновение с пилами
			time.sleep(1)  # Пауза одна секунда
			self.game.playing = False  # Запуск уровня заново
		
		# Столкновение с порталом:
		hits = self.rect.colliderect(self.game.portal.rect)
		if hits: # Если есть столкновение с порталом
			pg.event.post(pg.event.Event(pg.QUIT))  # Послать событие выхода из игры
		
	def animate(self):  # Анимация движения
		now = pg.time.get_ticks()  # Берем текущее время
		if now - self.last_update >= PLAYER_ANIMATE_DELAY:  # Если с последней смены кадра прошла длительность периода
			self.last_update = now  # Временем последней смены кадра будет текущий момент
			# Сменяем кадр:
			if int(self.vel.x) > 0:  # Если движемся вправо
				self.current_frame += 1  # Индекс кадра сменяем на следующий
				# Кадры сменяются циклично:
				if self.current_frame >= len(self.frames):  # Если вышли за границу кортежа с кадрами
					self.current_frame = 0  # Возвращаемся в начало кортежа
			elif int(self.vel.x) < 0:  # Если движемся влево
				self.current_frame -= 1  # Индекс кадра сменяем на предыдущий
				# Кадры сменяются циклично:
				if self.current_frame < 0:  # Если вышли за границу кортежа с кадрами
					self.current_frame = len(self.frames) - 1  # Возвращаемся в конец кортежа
			# По расчитаному индексу достаем кадр и используем как изображение для текущего такта
			self.image = self.frames[self.current_frame]
	
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
