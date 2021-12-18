# Файл с настройками
import os

MUSIC = os.path.join(os.getcwd(), 'resources/music/music.wav')  # Путь к файлу с музыкой
FONTPATH = os.path.join(os.getcwd(), 'resources/font/12243.otf')  # Путь к файлу с шрифтом

SCREENSIZE = (800, 500)  # Размер экрана

FPS = 5  # Частота кадров

BLOCK_SIZE = 20  # Размер клетки
GAME_MATRIX_SIZE = (int(SCREENSIZE[0] / BLOCK_SIZE), int(SCREENSIZE[1] / BLOCK_SIZE))  # Размер игового поля
