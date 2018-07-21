import pygame as pg  # Подключение pygame с именем pg
from player import Player  # Подключение игрока
from settings import *  # Подключение файла с настройками
from platform import Platform  # Подключение платформ
import levels  # Подключение уровней
from saw import Saw

class Game:
	def __init__(self):  # Конструктор
		pg.init()  # Запуск pygame
		self.screen = pg.display.set_mode(WINDOW_SIZE)  # Создание окна с размером из настроек
		pg.display.set_caption("GeekSchool Platformer")  # Заголовок окна
		self.clock = pg.time.Clock()  # Объект для отслеживания времени (тактов)
		self.running = True  # Флаг продолжения работы программы
	
	def new(self):  # Создание нового уровня
		self.all_sprites = pg.sprite.Group()  # Создание группы для всех спрайтов
		self.platforms = pg.sprite.Group()  # Создание группы для платформ
		self.saws = pg.sprite.Group()  # Создание группы для пил
		# Взятие двумерного кортежа настроек платформ и кортежа настроек игрока
		plts_conf, sws_cong, plr_conf = self.create_level(levels.level1)
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
		
		self.run()  # Запускаем уровень
	
	def create_level(self, lvl):  # Получение настроек объектов из схемы уровня
		x = y = 0  # Начало считывания схемы начинаем с (0; 0)
		player_config = (0, 0)  # Кортеж из координат появления игрока
		platforms_config = []  # Список для кортежей из координат платформ
		saws_config = []  # Список для кортежей из координат пил
		for row in lvl:  # Для каждой строки в схеме
			for cell in row:  # Для каждой ячейки в строке
				if cell == "-":  # Если в ячейке схемы символ платформы
					platforms_config.append((x, y))  # Добавляем кортеж из соответствующих координат платформы в список настроек
				if cell == "o":  # Если в ячейке схемы символ игрока
					player_config = (x, y)  # Сохранить соответсвующие координаты в кортеж настроек игрока
				if cell == "*":  # Если в ячейке схемы символ пилы
					saws_config.append((x, y))  # Добавляем кортеж из соответствующих координат пилы в список настроек
				x += PLATFORM_WIDTH  # После каждой ячейки сдвигаемся на ширину платформы
			y += PLATFORM_HEIGHT  # В конце строки смещаемся вниз на высоту платформы
			x = 0  # а X смещаем в начало
		return tuple(platforms_config), tuple(saws_config), player_config  # Возвращаем кортежи с настройками
	
	def events(self):  # Цикл обработки событий
		for event in pg.event.get():  # Берем события на текущем такте
			if event.type == pg.QUIT:  # Если пришло событие о выходе (нажатие на крестик или Alt+F4)
				self.playing = False  # Останавливаем уровень
				self.running = False  # Останавливаем основной цикл программы
	
	def update(self):  # Обновление состояния игровых объектов
		self.all_sprites.update()  # Обновление всех спрайтов
	
	def draw(self):  # Отрисовка
		self.screen.fill(WHITE)  # Заливка окна белым цветом
		self.all_sprites.draw(self.screen)  # Отрисовка всех спрайтов
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
