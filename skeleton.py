import pygame  # Подключение pygame


BLACK = (0, 0, 0)  # Кортеж для черного цвета в палитре RGB

pygame.init()  # Инициализация основной части pygame
screen = pygame.display.set_mode((800, 600))  # Создание окна размером 800х600
pygame.display.set_caption("GeekSchool Platformer")  # Заголовок окна
clock = pygame.time.Clock()  # Объект для отслеживания времени (тактов)

running = True
while running:
	clock.tick(60)  # Цикл выполняется с частотой 60Гц
	
	# Цикл обработки событий
	for event in pygame.event.get():  # Берем события на текущем такте
		if event.type == pygame.QUIT:  # Если пришло событие о выходе (нажатие на крестик или Alt+F4)
			running = False  # Останавливаем цикл
	
	# Обновление состояния игровых объктов
	pass  # Пока пустое
	
	# Отрисовка
	screen.fill(BLACK)  # Заливка окна чёрным цветом
	pygame.display.flip()  # Отображение кадра из буфера на экран

pygame.quit()  # Завершение работы pygame
