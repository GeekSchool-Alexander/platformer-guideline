import pygame as pg  # Подключение pygame с именем pg
from player import Player  # Подключение игрока
from settings import *  # Подключение файла с настройками
from platform import Platform  # Подключение платформ


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
		
		self.player = Player(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)  # Создание игрока
		self.all_sprites.add(self.player)  # Добавление игрока в группу
		
		p = Platform(800, 500)  # Создание тестовой платформы в некоторых координатах
		self.all_sprites.add(p)  # Добавление платформы в группу всех спрайтов
		self.platforms.add(p)  # Добавление платформы в группу платформ
		
		self.run()  # Запускаем уровень
	
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
