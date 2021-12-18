import config
import sys
import pygame
import random
import copy


def drawGame_Grid(config, screen): # Функция для рисования сетки игры
    """

    :param config: базовый файл со всеми настройками - размер экрана, частотой, музыкой
    :param screen: рабочий экран
    """
    color = (40, 40, 40)  # Устанавливаем цвет линий

    # Рисуем сетку из линий
    for x in range(0, config.SCREENSIZE[0], config.BLOCK_SIZE):
        pygame.draw.line(screen, color, (x, 0), (x, config.SCREENSIZE[1]))

    for y in range(0, config.SCREENSIZE[1], config.BLOCK_SIZE):
        pygame.draw.line(screen, color, (0, y), (config.SCREENSIZE[0], y))


def drawScore(config, score, screen):  # Функция вывода счёта на экран
    """

    :param config:  базовый файл со всеми настройками - размер экрана, частотой, музыкой
    :param score: переменная с количеством набранных очков
    :param screen: рабочий экран
    :return:
    """
    color = (255, 255, 255)  # Цвет текста

    # Вывод текста
    font = pygame.font.Font(config.FONTPATH, 30)
    text = font.render(F'Счёт: {score}', True, color)
    rect = text.get_rect()
    rect.topleft = (10, 10)
    screen.blit(text, rect)


class Apple(pygame.sprite.Sprite):  # Класс "Яблока"
    """
    Базовый класс Яблоко, отрисовываем нашу цель, используем спрайты
    """
    # Настройка класса
    def __init__(self, config, snake_coords):
        pygame.sprite.Sprite.__init__(self)
        self.config = config

        self.color = (255, 0, 0)  # Цвет яблока
        self.color_ = (240, 224, 0)  # Цвет обводки яблока

        while True:
            # Выбираем коородинаты яблока
            self.coord = [random.randint(0, config.GAME_MATRIX_SIZE[0] - 1),
                          random.randint(0, config.GAME_MATRIX_SIZE[1] - 1)]
            if self.coord not in snake_coords:
                break

    def draw_apple(self, screen): # Функция отрисовки яблока
        """

        :param screen: рабочий экран
        Отрисовываем само яблоко на экране
        """
        # Коородинаты отрисовки
        cx = int((self.coord[0] + 0.5) * self.config.BLOCK_SIZE)
        cy = int((self.coord[1] + 0.5) * self.config.BLOCK_SIZE)
        

        # Отрисовка
        pygame.draw.circle(screen, self.color_, (cx, cy), self.config.BLOCK_SIZE // 2 - 2)
        pygame.draw.circle(screen, self.color, (cx, cy), self.config.BLOCK_SIZE // 2 - 3)


class Snake(pygame.sprite.Sprite):  # Класс змеи
    """
        Базовый класс Змеи - главного игрока, отрисовываем нашу цель, используем спрайты
        """

    # Настройка класса
    def __init__(self, config):
        pygame.sprite.Sprite.__init__(self)
        self.config = config

        self.direction = 'right'  # Начальное направление движения
        self.head_colors = [(0, 80, 255), (0, 255, 255)]  # Цвет головы
        self.tail_colors = [(0, 155, 0), (0, 255, 0)]  # Цвет хвоста

        # Выбираем координаты головы (случайно)
        self.head_coord = [random.randint(5, config.GAME_MATRIX_SIZE[0] - 6),
                           random.randint(5, config.GAME_MATRIX_SIZE[1] - 6)]
        self.tail_coord = []  # Здесь будем хранить координаты хвоста

        # Заполним мервые две части хвоста на основе координать головы
        for i in range(1, 3):
            self.tail_coord.append([self.head_coord[0] - i, self.head_coord[1]])

    def set_Direction_travl(self, direction): # Функция изменения (установки) направления движения по командам
        """

        :param direction: переменная задающая направление движения Змейки на экране

        """
        if direction == 'up':
            if self.head_coord[1] - 1 != self.tail_coord[0][1]:
                self.direction = direction
        elif direction == 'down':
            if self.head_coord[1] + 1 != self.tail_coord[0][1]:
                self.direction = direction
        elif direction == 'right':
            if self.head_coord[0] + 1 != self.tail_coord[0][0]:
                self.direction = direction
        elif direction == 'left':
            if self.head_coord[0] - 1 != self.tail_coord[0][0]:
                self.direction = direction

    def update(self, apple):  # Обновление змейки
        """

        :param apple: переменная класса apple, задающая характеристики нашей цели

        """
        self.tail_coord.insert(0, copy.deepcopy(
            self.head_coord))  # Помещаем на 0 место списка хвоста старое положение головы
        # В зависилости от направления движения изменяем координату головы
        if self.direction == 'up':
            self.head_coord[1] -= 1
        elif self.direction == 'down':
            self.head_coord[1] += 1
        elif self.direction == 'left':
            self.head_coord[0] -= 1
        elif self.direction == 'right':
            self.head_coord[0] += 1

        # Определяем было ли съедено яблоко
        if self.head_coord == apple.coord:
            return True  # Если да - возвращаем True
        else:
            self.tail_coord = self.tail_coord[:-1]  # Иначе убераем последний элемент списка хвоста
            return False  # и возвращаем False

    def draw(self, screen):  # Функция отрисовки змейки
        # Координаты головы
        head_x = self.head_coord[0] * self.config.BLOCK_SIZE
        head_y = self.head_coord[1] * self.config.BLOCK_SIZE

        # Отрисовка головы
        rect = pygame.Rect(head_x, head_y, self.config.BLOCK_SIZE, self.config.BLOCK_SIZE)
        pygame.draw.rect(screen, self.head_colors[0], rect)
        rect = pygame.Rect(head_x + 4, head_y + 4, self.config.BLOCK_SIZE - 8, self.config.BLOCK_SIZE - 8)
        pygame.draw.rect(screen, self.head_colors[1], rect)

        for coord in self.tail_coord:  # Беребираем все элементы хвоста
            # Координаты n-го элементы списка координат хвоста
            x = coord[0] * self.config.BLOCK_SIZE
            y = coord[1] * self.config.BLOCK_SIZE

            # Отрисовка n-го элемента хвоста
            rect = pygame.Rect(x, y, self.config.BLOCK_SIZE, self.config.BLOCK_SIZE)
            pygame.draw.rect(screen, self.tail_colors[0], rect)
            rect = pygame.Rect(x + 4, y + 4, self.config.BLOCK_SIZE - 8, self.config.BLOCK_SIZE - 8)
            pygame.draw.rect(screen, self.tail_colors[1], rect)

    def coords(self):  # Функция для получения полной матрицы змейки
        """

        Получаем в этой функции список координат каждой части змейки
        """
        return [self.head_coord] + self.tail_coord

    def isgameover(self):  # Функция проверяет условия, при которых игра считается проигранной
        # Проверка на пересечение границ игрового поля
        if (self.head_coord[0] < 0) or (self.head_coord[1] < 0) or \
                (self.head_coord[0] >= self.config.GAME_MATRIX_SIZE[0]) or \
                (self.head_coord[1] >= self.config.GAME_MATRIX_SIZE[1]):
            return True

        # Проверка на пересечения самой себя
        if self.head_coord in self.tail_coord:
            return True
        return False


def end_menu(screen, cfg, score):  # Функция вывода меню при окончании игры
    """

    :param screen:  рабочий экран
    :param cfg: задает размер окна и фон
    :param score: число очков которое набрал игрок
    
    """
    # Задаём шрифты
    font_size_big = 70
    font_size_small = 23
    font_size_med = 50

    font_big = pygame.font.Font(cfg.FONTPATH, font_size_big)
    font_small = pygame.font.Font(cfg.FONTPATH, font_size_small)
    font_med = pygame.font.Font(cfg.FONTPATH, font_size_med)

    # Задаём цвета
    font_color = (255, 255, 255)
    over_color = (57, 255, 20)

    # Задаём поверхность
    surface = screen.convert_alpha()
    surface.fill((0, 0, 0, 5))

    # Отрисовываем надпись 'Игра окончена!'
    text = font_big.render('Игра окончена!', True, over_color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2 - 50 - 70
    surface.blit(text, text_rect)

    # Отрисовываем надпись 'Ваш счёт {score}', где score - счёт на конец игры
    text = font_med.render(F'Ваш счёт {score}', True, over_color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2 - 50
    surface.blit(text, text_rect)

    # Задаём положение кнопок
    button_width, button_height = 100, 40
    button_start_x_left = cfg.SCREENSIZE[0] / 2 - button_width - 20
    button_start_x_right = cfg.SCREENSIZE[0] / 2 + 20
    button_start_y = cfg.SCREENSIZE[1] / 2 - button_height / 2 + 20

    # Отрисовываем надпись 'Рестарт'
    pygame.draw.rect(surface, (128, 128, 128), (button_start_x_left, button_start_y, button_width, button_height))
    text_restart = font_small.render('Рестарт', True, font_color)
    text_restart_rect = text_restart.get_rect()
    text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_restart, text_restart_rect)

    # Отрисовываем надпись 'Выход'
    pygame.draw.rect(surface, (128, 128, 128), (button_start_x_right, button_start_y, button_width, button_height))
    text_quit = font_small.render('Выход', True, font_color)
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_quit, text_quit_rect)

    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():  # Перебираем эвенты
            if event.type == pygame.QUIT:  # При нажатии на кнопку закрыть выходим из приложения
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_quit_rect.collidepoint(
                        pygame.mouse.get_pos()):  # Проверка на нахождение клика внутри квадрата "выход"
                    return False  # Возвращаем False если игрок захотел выйти
                if text_restart_rect.collidepoint(
                        pygame.mouse.get_pos()):  # Проверка на нахождение клика внутри квадрата "рестарт"
                    return True  # Возвращаем True если игрок захотел перезапустить игру
        pygame.display.update()  # Обновляем экран


def main(config):  # Основная функция игры
    """

    :param config: базовый файл со всеми настройками - размер экрана, частотой, музыкой

    """
    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode(config.SCREENSIZE)  # Передаём размер экрана
    pygame.display.set_caption('Змейка')  # Устанавливаем название окна
    clock = pygame.time.Clock()  # Создаём объект часов
    # Воспроизведение фоновой музыки
    pygame.mixer.music.load(config.MUSIC)
    pygame.mixer.music.play(-1)

    # Основной цикл игры
    snake = Snake(config)
    apple = Apple(config, snake.coords())
    score = 0
    while True:
        screen.fill((0, 0, 0))  # Закрашиваем экран чёрным цветом
        for event in pygame.event.get():  # Перебираем эвенты
            if event.type == pygame.QUIT:  # При нажатии на кнопку закрыть выходим из приложения
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Если нажита одно из кнопок - стрелок -- отправляем команду на изменение направления движения, команда выберается согласно словарю
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.set_Direction_travl(
                        {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[
                            event.key])
        # Обновляем змейку и проверяем не съела ли она яблоко, если съела -- добавляем очко игроку
        if snake.update(apple):
            apple = Apple(config, snake.coords())  # Изменяем положение яблока, если оно съедено
            score += 1  # Добавляем очко игроку

        if snake.isgameover():  # Проверяем условий на окончание игры
            break  # Если условие выболняется выходим из конструкции while

        drawGame_Grid(config, screen)  # Отрисовываем игровую сетку

        snake.draw(screen)  # Отрисовываем змейку

        apple.draw_apple(screen)  # Отрисовываем яблоко

        drawScore(config, score, screen)  # Отрисовываем счёт

        pygame.display.update()  # Обновляем экран

        clock.tick(config.FPS)  # Устанавливаем частоту обновления экрана
    return end_menu(screen, config,
                    score)  # При окончании игры выводим меню концовки, которая в случае если игрок захочет переиграть вернёт True, в ином случае вернёт False


# ЗАПУСК ИГРЫ 

if __name__ == '__main__':
    while True:
        if not main(config):  # Запуск игры и обработка меню концовки
            break
