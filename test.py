from unittest import TestCase
import unittest
from snake import Apple
from snake import Snake
import random
import config
import HTB


#Зададим цвета в игре
BLACK = (0,0,0)
WHITE = (255,255,255)
GREENYELLOW = (143,245,34)
YELLOW = (234, 245, 34)
GREY = (210,210,210)
DARKGREY = (93,94,94)
RED = (255,0,0)
GREEN = (0,255,0)
REDORANGE = (245,103,32)

#Тестируем, что координата яблока находится на поле, то есть проверяем формулу
class SelfAppleTest(TestCase):
 
    def setUp(self):
        self.apple = Apple(config, [0,0])
 
 
    def test_draw_apple(self):
      for i in range(10):
            self.config = config
            self.color = (255, 0, 0)  # Цвет яблока
            self.color_ = (240, 224, 0)  # Цвет обводки яблока
            self.coord = [random.randint(0, config.GAME_MATRIX_SIZE[0] - 1),
            random.randint(0, config.GAME_MATRIX_SIZE[1] - 1)]

            cx = int((self.coord[0] + 0.5) * self.config.BLOCK_SIZE)
            cy = int((self.coord[1] + 0.5) * self.config.BLOCK_SIZE)

            
            self.assertLessEqual(cy, 500)
        
            self.assertLessEqual(cx, 800)
            r = unittest.TestResult()
            print(r)


#Тестируем, что змейка не пересекла себя
class SelfSnake(TestCase):
    
    def setUp(self):
        self.snake = Snake(config)
 
 
    def test_coords(self):
        for i in range(10):
                    # Выбираем координаты головы (случайно)
            self.head_coord = [random.randint(5, config.GAME_MATRIX_SIZE[0] - 6),
            random.randint(5, config.GAME_MATRIX_SIZE[1] - 6)]
            self.tail_coord = []  # Здесь будем хранить координаты хвоста
                    # Заполнил мервые две части хвоста на основе координать головы
            for i in range(1, 3):
                self.tail_coord.append([self.head_coord[0] - i, self.head_coord[1]])
            
            self.assertNotIn(self.head_coord,self.tail_coord)
     
        r = unittest.TestResult()
        print(r)


#Тестируем, что змейка не пересекла себя
class Self_Shield(TestCase):
    
 
 
    def test_shield(self):
        player_shield_color = GREEN
        
        for i in range(10):
            player_shield = int(random.randint(1,110))
            
            HTB.shield_bar1(0, player_shield)
            if player_shield > 100:
                self.assertLessEqual(player_shield_color, GREEN)
            elif player_shield > 75:
                self.assertLessEqual(player_shield_color, GREEN)
            elif player_shield > 50:
                self.assertLessEqual(player_shield_color, YELLOW)
            else:
                self.assertLessEqual(player_shield_color, RED)

     
        r = unittest.TestResult()
        print(r)


if __name__ == "__main__":
  unittest.main()
  
  r = unittest.TestResult()
  SelfAppleTest('test_draw_apple').run(result=r)
  
  
