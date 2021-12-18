#Импорт бибилиотек необходимых для запуска данного файла
import pygame, sys, random
from pygame import *
from os import path


#Зададим пути к файлам, которые будем использовать
img_dir = path.join(path.dirname(__file__), 'images')
sound_dir = path.join(path.dirname(__file__), 'sounds')

#Размеры экрана
WINDOWWIDTH = 480
WINDOWHEIGHT = 500
#Частота смены кадров
FPS = 30


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

#Запуск модулей для игры
pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('HIT THE BALL')

FPSCLOCK = pygame.time.Clock()

#Зададим класс препятствий
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, enemy_image, bullet_image, sprites_list, bullet_list, bullet_sound, boost_anim):
        super().__init__()
        #Выбор размера и изображения объекта
        self.image = pygame.transform.scale(enemy_image, (60, 60))
        self.rect = self.image.get_rect()

        self.sprites = sprites_list
        self.boost_anim = boost_anim

        self.rect.centerx = random.randrange(90, WINDOWWIDTH - 90)
        self.rect.bottom = random.randrange(-150, -20)

        self.bullet_image = bullet_image
        self.bullet_sound = bullet_sound
        self.bullets = bullet_list
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.num_of_shots = 2
        #Настройка скорости
        self.speedy = 30
    #Обновление экрана с изменением функций
    def update(self):
        if self.rect.bottom > 50 and self.rect.bottom < 130:
            for i in range(self.num_of_shots):
                self.shoot()
        #Обновление экрана с изменением функций
        if self.rect.bottom <= 120:
            self.rect.bottom += 4
        if self.rect.bottom > 120 and self.rect.bottom < 140:
            self.rect.bottom += 1
        if self.rect.bottom >= 140:
            self.divebomb()

        if (self.rect.top > WINDOWHEIGHT):
            self.rect.centerx = random.randrange(50, WINDOWWIDTH - 50)
            self.rect.y = random.randrange(-200, -50)
    def shoot(self):
        #Функция выстрела со звуком
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet = EnemyBullet(self.bullet_image, self.rect.centerx, self.rect.bottom)
            self.sprites.add(bullet)
            self.bullets.add(bullet)
            self.bullet_sound.play()
            self.bullet_sound.set_volume(0.2)

    def divebomb(self):
        boost = Boost(self.rect.center, 'boost', self.boost_anim)
        self.sprites.add(boost)
        self.rect.bottom += self.speedy

#Зададим класс бустеров
class Boost(pygame.sprite.Sprite):
    def __init__(self, center, b_type, boost_anim):
        super().__init__()
        self.b_type = b_type
        self.boost_anim = boost_anim
        self.image = boost_anim[self.b_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 35
    #Обновление экрана с изменением функций
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.boost_anim[self.b_type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.boost_anim[self.b_type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.midtop = center


#Зададим класс лазера, который будет стрелять
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (8, 23))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -15
  #Обновление экрана с изменением функций
    def update(self):
        self.rect.y += self.speedy
        #Если ослаб - удаляем
        if self.rect.bottom < 35:
            self.kill()

#Зададим спрайт для лазера - пули
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (8, 23))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 15
#Обновление экрана с изменением функций
    def update(self):
        self.rect.y += self.speedy
        #Если пропал - удаляем
        if self.rect.bottom > WINDOWHEIGHT:
            self.kill()



#Зададим класс препятсвий - шариков
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, asteroid_img, all_sprites, asteroid_sprites):
        super().__init__()
        self.image_orig = random.choice(asteroid_img)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)

        self.rect.x = random.randrange(-25, WINDOWWIDTH + 25)
        self.rect.y = random.randrange(-200, -100)

        self.speedy = random.randrange(5, 8)
        self.speedx = random.randrange(-2, 2)

        self.angle = 0
        self.rotation_speed = random.randrange(-7, 5)
        self.last_update = pygame.time.get_ticks()

   #Обновление экрана с изменением функций     
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if (self.rect.top > WINDOWHEIGHT + 10) or (self.rect.left < -self.rect.width) or (
                self.rect.right > WINDOWWIDTH + self.rect.width):
            self.rect.x = random.randrange(0, WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -20)
            self.speedy = random.randrange(3, 8)

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > 50:
            self.last_update = current_time
            self.angle = (self.angle + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.angle)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

#
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, ex_type, explosion_anim):
        super().__init__()
        self.ex_type = ex_type
        self.explosion_anim = explosion_anim
        self.image = explosion_anim[self.ex_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        
#Обновление экрана с изменением функций
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.ex_type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.ex_type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#Зададим класс увелечения силы при получении аптечки
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, powerup_images):
        super().__init__()
        self.type = random.choice(['shield'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4
        
#Обновление экрана с изменением функций
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT + 10:
            self.kill()

#Зададим класс аптечки
class Shield(pygame.sprite.Sprite):
    def __init__(self, image, center, player):
        super().__init__()
        self.image = pygame.transform.scale(image, (85, 85))
        self.center = center
        self.rect = self.image.get_rect(center=(self.center))
        self.player = player

 #Обновление экрана с изменением функций       
    def update(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

        if self.player.shield <= 30:
            self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 115)
        elif self.player.shield > 30:
            self.rect.centerx = self.player.rect.centerx
            self.rect.centery = self.player.rect.centery


#Основной класс игрока - джойстика
class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, bullet_image, missile_image, sprites_list, bullet_list, bullet_sound, missile_sound):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.sprites = sprites_list

        self.rect.centerx = WINDOWWIDTH / 2
        self.rect.bottom = WINDOWHEIGHT - 10

        self.speedx = 0
        self.speedy = 0

        self.bullet_image = bullet_image
        self.missile_image = missile_image
        self.bullets = bullet_list
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        self.bullet_sound = bullet_sound

        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.upgrade = 1
        self.upgrade_timer = pygame.time.get_ticks()

#Обновление экрана с изменением функций        
    def update(self):
        if self.hidden and (pygame.time.get_ticks() - self.hide_timer > 1500):
            self.hidden = False
            self.rect.centerx = WINDOWWIDTH / 2
            self.rect.bottom = WINDOWHEIGHT - 10

        if self.upgrade >= 2 and pygame.time.get_ticks() - self.upgrade_timer > 4500:
            self.upgrade -= 1
            self.upgrade_timer = pygame.time.get_ticks()

        self.speedx = 0 
        self.speedy = 0 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -9
        if keys[pygame.K_RIGHT]:
            self.speedx = +9
        if keys[pygame.K_UP]:
            self.speedy = -9
        if keys[pygame.K_DOWN]:
            self.speedy = +9

        if keys[pygame.K_SPACE] and not(self.rect.top > WINDOWHEIGHT):
            self.shoot()

        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 200:
            self.rect.top = 200
        if self.rect.bottom > WINDOWHEIGHT - 10 and self.rect.bottom < WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT - 10

        if self.rect.bottom > WINDOWHEIGHT + 10:
            self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 100)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
    #Функция выстрела - как стреляем в зависимости от того, насколько попали
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            if self.upgrade == 1:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                self.bullet_sound.play()
            if self.upgrade == 2:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
                self.bullet_sound.play()
                self.missile_sound.play()
            if self.upgrade == 3:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
                missile2 = Missile(self.missile_image, self.rect.right, self.rect.centery)
                self.sprites.add(missile2)
                self.bullets.add(missile2)
                self.bullet_sound.play()
                self.missile_sound.play()
                
#Обновление силы с изменением функций
    def upgrade_power(self):
        if self.upgrade >= 3:
            self.upgrade = 3
        elif self.upgrade < 3:
            self.upgrade += 1
        self.upgrade_timer = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 100)
        self.hide_timer = pygame.time.get_ticks()


#Задаем окно - меню 
def menu():
    #Дизайн экрана и формы
    background = pygame.image.load('images/stars_bg.jpeg').convert()
    background_rect = background.get_rect()

    arrow_keys = pygame.image.load(path.join(img_dir, 'arrowkeys.png')).convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
    spacebar = pygame.image.load(path.join(img_dir, 'spacebar.png')).convert_alpha()
    spacebar = pygame.transform.scale(spacebar, (180, 70))

    DISPLAYSURF.blit(background, background_rect)
    DISPLAYSURF.blit(arrow_keys, (225, 400))
    DISPLAYSURF.blit(spacebar, (250, 500))
    draw_text(DISPLAYSURF, "НАЖМИТЕ ENTER, ЧТОБЫ НАЧАТЬ", 30, 250, 180, BLACK)
    draw_text(DISPLAYSURF, "НАЖМИТЕ Q, ЧТОБЫ ВЫЙТИ", 30, 250, 220, WHITE)
    draw_text(DISPLAYSURF, "HIT THE BALL", 44, 250, 60, WHITE)
    draw_text(DISPLAYSURF, "ПЕРЕМЕЩЕНИЕ:", 30, 120, 440, BLACK)
    draw_text(DISPLAYSURF, "SHOOT:", 35, 101, 516, WHITE)

    pygame.display.update()
    #Запуск самой игры и считывание кнопок
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()    

#Изображение жизни в панельке меню
def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(image, img_rect)

#Сохраняем формат текста единым
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
#Цвет ползунка жизни
def shield_bar(surface, player_shield):
    if player_shield > 100:
        player_shield_color = GREEN
        player_shield = 100
    elif player_shield > 75:
        player_shield_color = GREEN
    elif player_shield > 50:
        player_shield_color = YELLOW
    else:
        player_shield_color = RED
#Рисовка ползунка
    pygame.draw.rect(surface, GREY, (5, 5, 104, 24), 3)
    pygame.draw.rect(surface, player_shield_color, (7, 7, player_shield, 20))

#Функция для тестирования алгоритма
def shield_bar1(surface, player_shield):
    if player_shield > 100:
        player_shield_color = GREEN
        player_shield = 100
    elif player_shield > 75:
        player_shield_color = GREEN
    elif player_shield > 50:
        player_shield_color = YELLOW
    else:
        player_shield_color = RED


#Основная функция запуска
def main():
    #Настраиваем фон главного меню
    background = pygame.image.load('images/stars_bg.jpeg').convert()
    background_rect = background.get_rect()
    
    
    black_bar = pygame.Surface((WINDOWWIDTH, 35))
    
    #Связываем нашего игрока с картинкой, а также другие эелементы игры
    player_img = pygame.image.load('images/spaceship.png').convert()

    life_player_image = pygame.transform.scale(player_img, (25, 25))
    life_player_image.set_colorkey(BLACK)
    
    bullet_img = pygame.image.load('images/laser_red.png').convert()
    
    missile_img = pygame.image.load('images/missile.png').convert_alpha()
    energy_shield = pygame.image.load('images/energy_shield.png').convert_alpha()

    
    #Список возможных препятсвий
    asteroid_images = []
    asteroid_list = [
        'asteroid_medium.png',
        'asteroid_big.png',
        'asteroid_tiny.png'   
    ]

    for image in asteroid_list:
        asteroid_images.append(pygame.image.load(path.join(img_dir, image)).convert_alpha())

    explosion_anim = {}
    explosion_anim['large'] = []
    explosion_anim['small'] = []
    explosion_anim['ship'] = []
    for i in range(5):
        filename = 'explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        image_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['large'].append(image_lg)
        image_sm = pygame.transform.scale(img, (45, 45))
        explosion_anim['small'].append(image_sm)
    
    for i in range(10):
        filename = 'ship_explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        image_player = pygame.transform.scale(img, (100, 100))
        explosion_anim['ship'].append(image_player)

    boost_anim = {}
    boost_anim['boost'] = []
    
        
        
    powerup_images = {}
    powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert_alpha()
    powerup_images['shield'] = pygame.transform.scale(powerup_images['shield'], (35, 35)) 
    

    bullet_sound = pygame.mixer.Sound(path.join(sound_dir, 'laser.mp3'))
    bullet_sound.set_volume(0.25)
    enemy_bullet_sound = pygame.mixer.Sound(path.join(sound_dir, 'laser.mp3'))
    missile_sound = pygame.mixer.Sound(path.join(sound_dir, 'explosion_ship.mp3'))
    missile_sound.set_volume(0.15)
    small_expl = pygame.mixer.Sound(path.join(sound_dir, 'explosion_ship.mp3'))
    ship_expl = pygame.mixer.Sound(path.join(sound_dir, 'explosion_ship.mp3'))
    ship_expl.set_volume(0.4)

    running = True
    show_menu = True
    while running:
        if show_menu:
            menu()
            pygame.time.delay(1500)

            pygame.mixer.music.fadeout(1500)

            show_menu = False

            all_active_sprites = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            
            asteroids = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            enemy_ships = pygame.sprite.Group()

            player = Player(player_img, bullet_img, missile_img, all_active_sprites, 
                            bullets, bullet_sound, missile_sound)
            shield = Shield(energy_shield, player.rect.center, player)
            all_active_sprites.add(player, shield)

            
            
            for i in range(7):
                new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
                all_active_sprites.add(new_asteroid)
                asteroids.add(new_asteroid)   

            score = 0
        #Пока идет игра - запускаем функции
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        #Обновляем все элементы при изменении одного
        all_active_sprites.update()
        #Обновление экрана с изменением функций 
        asteroid_hit = pygame.sprite.groupcollide(asteroids, bullets, True, pygame.sprite.collide_circle)
        for hit in asteroid_hit:
            score += 50 - hit.radius
            small_expl.play()
            small_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'large', explosion_anim)
            all_active_sprites.add(expl)
            if random.random() > 0.92:
                powerup = PowerUp(hit.rect.center, powerup_images)
                all_active_sprites.add(powerup)
                powerups.add(powerup)
            new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
            all_active_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)



        

        

        player_hit = pygame.sprite.spritecollide(player, asteroids, True)

        for hit in player_hit:
            player.shield -= random.randint(10, 25)
            small_expl.play()
            small_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'small', explosion_anim)
            all_active_sprites.add(expl)
            new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
            all_active_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)
            if player.shield <= 0:
                ship_expl.play()
                expl_ship = Explosion(player.rect.center, 'ship', explosion_anim)
                all_active_sprites.add(expl_ship)
                player.hide()
                player.lives -= 1
                player.shield = 100

        player_hit_by_ship = pygame.sprite.spritecollide(player, enemy_ships, True)
        
        for hit in player_hit_by_ship:
            player.shield -= 35
            ship_expl.play()
            ship_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'ship', explosion_anim)
            all_active_sprites.add(expl)
            new_ship = EnemyShip(enemy_img, enemy_bullet_img, all_active_sprites, enemy_bullets, 
                                 enemy_bullet_sound, boost_anim)
            all_active_sprites.add(new_ship)
            enemy_ships.add(new_ship)
            if player.shield <= 0:
                ship_expl.play()
                expl_ship = Explosion(player.rect.center, 'ship', explosion_anim)
                all_active_sprites.add(expl_ship)
                player.hide()
                player.lives -= 1
                player.shield = 100

        powerup_hit = pygame.sprite.spritecollide(player, powerups, True)

        for hit in powerup_hit:
            if hit.type == 'shield':
                score += 100
                player.shield += 20
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'missile':
                score += 50
                player.upgrade_power()
       #Пропишем проигрыш
        if player.lives == 0 and not expl_ship.alive():
            pygame.mixer.music.stop()
            show_menu = True
        #Настройки верхнего меню для отображения очков 
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(background, background_rect)
        all_active_sprites.draw(DISPLAYSURF)
        DISPLAYSURF.blit(black_bar, (0,0))
        pygame.draw.rect(DISPLAYSURF, GREY, (0, 0, WINDOWWIDTH, 35), 3)
        shield_bar(DISPLAYSURF, player.shield)
        # Добавим 
        draw_text(DISPLAYSURF, "ОЧКИ", 12, WINDOWWIDTH / 2, 2, WHITE)
        draw_text(DISPLAYSURF, str(score), 23, WINDOWWIDTH / 2, 12, WHITE)

        draw_lives(DISPLAYSURF, WINDOWWIDTH - 100, 5, player.lives, life_player_image)

        FPSCLOCK.tick(FPS)
        pygame.display.flip()

        
#ЗАПУСК ИГРЫ
if __name__ == "__main__":
    main()
