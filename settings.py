# Файл с настройками

# Цвета
WHITE = (255, 255, 255)  # Белый цвет для фона
RED = (255, 0, 0)  # Красный цвет для игрока
DARK_GREEN = (0, 150, 0)  # Тёмно зелёный цвет для победной надписи

# Настройки окна
WINDOW_WIDTH = 1000  # Ширина окна
WINDOW_HEIGHT = 600  # Высота окна
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)  # Кортеж размеров окна
FPS = 60  # Frames per Second; Частота, на которой наботает основной цикл

# Настройки игрока
PLAYER_WIDTH = 30  # Ширина игрока
PLAYER_HEIGHT = 30  # Высота игрока
PLAYER_SIZE = (PLAYER_WIDTH, PLAYER_HEIGHT)  # Размеры игрока
PLAYER_ACC = 1  # Ускорение движения по оси Х
PLAYER_FRICTION = 0.1  # Коэффициент трения
PLAYER_GRAVITY = 1  # Ускорение свободного падения
PLAYER_JUMP = 20  # Импульс прыжка
PLAYER_ANIMATE_DELAY = 75  # Период смены кадров

# Настройки платформ
PLATFORM_WIDTH = 40  # Ширина платформы
PLATFORM_HEIGHT = 40  # Высота платформы
PLATFORM_EMPTY_CORNER = 1  # Размер пустого угла; Применяется для игнорирования случаев касания двух граней

# Настройки пил
SAW_WIDTH = 40  # Ширина пилы
SAW_HEIGHT = 40  # Высота пилы
SAW_ANIMATE_DELAY = 15  # Период смены кадров
SAW_SPEED = 5  # Скорость движения летающей пилы
