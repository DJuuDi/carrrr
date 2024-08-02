from random import choice, randint
from pygame import *
import pygame_menu
import sys

init()
font.init()
font1 = font.SysFont("Impact", 100)
font2 = font.SysFont("Impact", 50)
game_over_text = font1.render("Гра закіньченна", True, (150, 0, 0))

screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
FPS = 90
clock = time.Clock()

bg = image.load('road.jpg')
bg = transform.scale(bg, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

player_img = image.load("car.png")
enemy_img = image.load("enemy.png")
enemy_img2 = image.load("klipartz.com.png")

all_sprites = sprite.Group()

line_x = [120, 550, 1030]

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)


class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.score = 0
        self.speed = 8
        self.bg_speed = 2
        self.max_speed = 30

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_UP]:
            if self.rect.y > 300:
                self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.3

        if key_pressed[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            if self.bg_speed > 2:
                self.bg_speed -= 0.2

        if key_pressed[K_LEFT] and self.rect.x > 50:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.right < WIDTH - 50:
            self.rect.x += self.speed

        enemy_collide = sprite.spritecollide(
            self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100


class Enemy(Sprite):
    def __init__(self, sprite_img, width, height):
        rand_x = randint(0, 2)
        super().__init__(sprite_img, width, height, line_x[rand_x], -200)
        self.damage = 100
        self.speed = 4
        enemys.add(self)

    def update(self):
        self.rect.y += player.bg_speed + 2
        if self.rect.y > HEIGHT:
            self.kill()

player = Player(player_img, 200, 300, 300, 300)
enemys = sprite.Group()

def save_max_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def read_max_score():
    try:
        with open("score.txt", "r") as file:
            score = float(file.read())
            return score
    except:
        return 0

score_text = font2.render(f"Score:{player.score}", True, (255, 255, 255))
max_score = read_max_score()
max_score_text = font2.render(f"Max Score:{max_score}", True, (255, 255, 255))

start_time = time.get_ticks()
enemy_spawn_time = time.get_ticks()
enemy2_spawn_time = time.get_ticks()
spawn_interval = randint(500, 3500)
spawn2_interval = randint(500, 3500)



def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')

def start_the_game():
    # Do the job here !
    global run
    run = True
    menu.disable()

#завантажуємо картинку
myimage = pygame_menu.baseimage.BaseImage(
    image_path='road.jpg',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)
#створюємо власну тему - копію стандартної
mytheme = pygame_menu.themes.THEME_DARK.copy()
# колір верхньої панелі (останній параметр - 0 робить її прозорою)
mytheme.title_background_color=(255, 255, 255, 0) 
#задаємо картинку для фону
mytheme.background_color = myimage
menu = pygame_menu.Menu('a lOng rOad', WIDTH, HEIGHT,
                       theme=mytheme)   

user_name = menu.add.text_input("Ім'я :", default='Анонім')
menu.add.selector('Складність :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Грати', start_the_game)
menu.add.button('Вийти', pygame_menu.events.EXIT)
menu.mainloop(window)

run = True
finish = False

start_screen = True
start_text = font2.render(f"НАЖМИ ЛЮБУ КНОПКУ", True, (255, 255, 255))
restart_text = font2.render(f"НАЖМИ R щоб переграти", True, (255, 255, 255))



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if start_screen:
                start_screen = False
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)
            if finish and e.key == K_r:
                finish = False
                for s in all_sprites:
                    s.kill()
                player = Player(player_img,  200, 300, 300, 300)
                score_text = font2.render(f"Score:{player.score}", True, (255, 255, 255))


    window.blit(bg, (0, bg_y1))
    window.blit(bg, (0, bg_y2))

    if start_screen:
        window.blit(start_text, (WIDTH/2 - start_text.get_width()/2,
                                 HEIGHT/2 - start_text.get_height()/2))
    else:
        if not finish:
            bg_y1 += player.bg_speed
            bg_y2 += player.bg_speed

            if bg_y1 > HEIGHT:
                bg_y1 = -HEIGHT
            if bg_y2 > HEIGHT:
                bg_y2 = -HEIGHT
            player.score += 0.3
            score_text = font2.render(f"Score:{int(player.score)}", True, (255, 255, 255))

            if player.hp <= 0:
                finish = True

            now = time.get_ticks()  # отримуємо поточний час
            if now - enemy_spawn_time > spawn_interval:  # якщо від появи останнього ворога пройшло більше 1с
                rand_k = randint(1, 1)
                for i in range(rand_k):
                    enemy1 = Enemy(enemy_img, 200, 150)  # створюємо нового ворога
                enemy_spawn_time = time.get_ticks()  # оновлюємо час появи ворога
                spawn_interval = randint(2000, 5000)

            if now - enemy2_spawn_time > spawn2_interval:  
                rand_k = randint(1, 3)
                for i in range(rand_k):
                    enemy2 = Enemy(enemy_img2, 150, 200)  
                enemy2_spawn_time = time.get_ticks()  
                spawn2_interval = randint(3000, 8000)


            collide_list = sprite.spritecollide(
                player, enemys, True, sprite.collide_mask)
            if len(collide_list) > 0:
                finish = True
                if player.score > max_score:
                    max_score = player.score
                    save_max_score(max_score)
            all_sprites.update()
        
        all_sprites.draw(window)
        window.blit(score_text, (30, 30))
        window.blit(max_score_text, (30, 100))
        max_score_text = font2.render(f"Max Score:{int(max_score)}", True, (255, 255, 255))

        if finish:
            window.blit(game_over_text,
                        (WIDTH/2 - game_over_text.get_width()/2,
                         HEIGHT/2 - game_over_text.get_height()/2))

            window.blit(restart_text,
                        (WIDTH/2 - restart_text.get_width()/2,
                        HEIGHT/2 - restart_text.get_height()/2 + 100))
            
    display.update()
    clock.tick(FPS)