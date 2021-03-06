import pygame as pg  # Подключение pygame с именем pg
from player import Player  # Подключение игрока
from settings import *  # Подключение файла с настройками
from platform import Platform  # Подключение платформ
import levels  # Подключение уровней
from saw import Saw, FlyingSaw
from portal import Portal

class Game:
	def __init__(self):  # Конструктор
		pg.init()  # Запуск pygame
		self.screen = pg.display.set_mode(WINDOW_SIZE)  # Создание окна с размером из настроек
		self.background = pg.image.load("./images/background.jpg")  # Загрузка изображения фона
		pg.display.set_caption("GeekSchool Platformer")  # Заголовок окна
		pg.display.set_icon(pg.image.load("./images/icon.jpg"))  # Установка иконки
		self.clock = pg.time.Clock()  # Объект для отслеживания времени (тактов)
		self.running = True  # Флаг продолжения работы программы
		self.font = pg.font.SysFont("timesnewroman", 200)  # Создание шрифта
		self.win_text = self.font.render("YOU WIN", 1, DARK_GREEN)  # Создание победной надписи
		self.player_won = False  # Флаг победы
	
	def new(self):  # Создание нового уровня
		self.all_sprites = pg.sprite.Group()  # Создание группы для всех спрайтов
		self.platforms = pg.sprite.Group()  # Создание группы для платформ
		self.saws = pg.sprite.Group()  # Создание группы для пил
		# Взятие двумерного кортежа настроек платформ и кортежа настроек игрока
		plts_conf, sws_cong, fl_sws_conf, plr_conf, prtl_conf = self.create_level(levels.level1)
		self.player = Player(*plr_conf, self)  # Создание игрока раскрыв кортеж настроек игрока и передав ссылку на игру
		self.all_sprites.add(self.player)  # Добавление игрока в группу
		
		for plt in plts_conf:  # Для каждого кортежа настроек в двумерном кортеже
			p = Platform(*plt)  # Создаем платформу по координатам раскрывая кортеж настроек
			# Добавляем платформу в группы
			self.all_sprites.add(p)
			self.platforms.add(p)
		
		for saw in sws_cong:  # Для каждого кортежа настроек в двумерном кортеже
			s = Saw(*saw)  # Создаем пилу по координатам раскрывая кортеж настроек
			# Добавляем платформу в группы
			self.all_sprites.add(s)
			self.saws.add(s)
		
		for saw in fl_sws_conf:  # Для каждого кортежа настроек в двумерном кортеже
			s = FlyingSaw(*saw, self.platforms)  # Создание летающей пилы
			# Добавляем летающую пилу в группы
			self.all_sprites.add(s)
			self.saws.add(s)
		
		self.portal = Portal(*prtl_conf)
		self.all_sprites.add(self.portal)
		
		self.run()  # Запускаем уровень
	
	def create_level(self, lvl):  # Получение настроек объектов из схемы уровня
		x = y = 0  # Начало считывания схемы начинаем с (0; 0)
		player_config = (0, 0)  # Кортеж из координат появления игрока
		platforms_config = []  # Список для кортежей из координат платформ
		saws_config = []  # Список для кортежей из координат пил
		flying_saws_config = []
		portal_config = (0, 0)
		for row in lvl:  # Для каждой строки в схеме
			for cell in row:  # Для каждой ячейки в строке
				if cell == "-":  # Если в ячейке схемы символ платформы
					platforms_config.append((x, y))  # Добавляем кортеж из соответствующих координат платформы в список настроек
				if cell == "o":  # Если в ячейке схемы символ игрока
					player_config = (x, y)  # Сохранить соответсвующие координаты в кортеж настроек игрока
				if cell == "*":  # Если в ячейке схемы символ пилы
					saws_config.append((x, y))  # Добавляем кортеж из соответствующих координат пилы в список настроек
				if cell == "<":  # Если в ячейке схемы символ пилы, летящей влево
					flying_saws_config.append((x, y, "left"))  # Добавляем кортеж из соответствующих координат и направления
				if cell == ">":  # Если в ячейке схемы символ пилы, летящей вправо
					flying_saws_config.append((x, y, "right"))  # Добавляем кортеж из соответствующих координат и направления
				if cell == "^":  # Если в ячейке схемы символ пилы, летящей вверх
					flying_saws_config.append((x, y, "up"))  # Добавляем кортеж из соответствующих координат и направления
				if cell == "v":  # Если в ячейке схемы символ пилы, летящей вниз
					flying_saws_config.append((x, y, "down"))  # Добавляем кортеж из соответствующих координат и направления
				if cell == "x":  # Если в ячейке схемы символ портала
					portal_config = (x, y)  # Сохранить соответсвующие координаты в кортеж настроек портала
				x += PLATFORM_WIDTH  # После каждой ячейки сдвигаемся на ширину платформы
			y += PLATFORM_HEIGHT  # В конце строки смещаемся вниз на высоту платформы
			x = 0  # а X смещаем в начало
		# Возвращаем кортежи с настройками
		return tuple(platforms_config), tuple(saws_config), tuple(flying_saws_config), player_config, portal_config

	
	def events(self):  # Цикл обработки событий
		for event in pg.event.get():  # Берем события на текущем такте
			if event.type == pg.QUIT:  # Если пришло событие о выходе (нажатие на крестик или Alt+F4)
				self.playing = False  # Останавливаем уровень
				self.running = False  # Останавливаем основной цикл программы
			elif event.type == pg.KEYDOWN:  # Если пришло событие о нажатии клавиши
				if event.key == pg.K_ESCAPE:  # ESC
					self.playing = False  # Останавливаем уровень
					self.running = False  # Останавливаем основной цикл программы
	
	def update(self):  # Обновление состояния игровых объектов
		self.all_sprites.update()  # Обновление всех спрайтов
	
	def draw(self):  # Отрисовка
		self.screen.blit(self.background, (0, 0))  # Отрисовка фона
		self.all_sprites.draw(self.screen)  # Отрисовка всех спрайтов
		if self.player_won:  # Если игрок победил
			self.screen.blit(self.win_text, (75, 150))  # Отобразить победную надпись в необходимых координатах
		pg.display.flip()  # Отображение кадра из буфера на экран
	
	def run(self):  # Основной цикл
		self.playing = True  # Флаг продолжения уровня
		while self.playing:  # Если продолжать уровень
			self.clock.tick(FPS)  # Работа на частоте из настроек
			self.events()  # Обработка событий
			self.update()  # Обновление игровых объектов
			self.draw()  # Отрисовка
	
	def main(self):  # Основная функция
		while self.running:  # Если продолжать программу
			self.new()  # Создать уровень
	
	def __del__(self):  # Деструктор
		pg.quit()  # Завершение работы pygame


g = Game()  # Создание игры
g.main()  # Вызов главной функции
