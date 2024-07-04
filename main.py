import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Розміри вікна
screen_width = 800
screen_height = 600

# Налаштування екрану
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Гонка")

# Кольори
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Годинник для контролю FPS
clock = pygame.time.Clock()

# Завантаження зображень
car_img = pygame.image.load('car.png')  # Використайте свій шлях до зображення автомобіля
car_width = car_img.get_width()

# Функція відображення автомобіля
def car(x, y):
    screen.blit(car_img, (x, y))

# Функція відображення перешкод
def obstacles(obst_list):
    for obst in obst_list:
        pygame.draw.rect(screen, black, [obst[0], obst[1], obst[2], obst[3]])

# Функція відображення тексту
def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((screen_width / 2), (screen_height / 2))
    screen.blit(text_surf, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def crash():
    message_display('Ви врізалися!')

# Основна гра
def game_loop():
    x = (screen_width * 0.45)
    y = (screen_height * 0.8)
    x_change = 0

    obst_starty = -600
    initial_speed = 7
    obst_speed = initial_speed
    obst_width = 100
    obst_height = 100
    num_of_obstacles = 5

    obst_list = []
    for i in range(num_of_obstacles):
        obst_x = random.randrange(0, screen_width)
        obst_y = obst_starty - i * (obst_height + 200)  # Розставляємо перешкоди з інтервалом
        obst_list.append([obst_x, obst_y, obst_width, obst_height])

    score = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        screen.fill(white)

        for obst in obst_list:
            obst[1] += obst_speed
            if obst[1] > screen_height:
                obst[1] = obst_starty
                obst[0] = random.randrange(0, screen_width)
                score += 1
                obst_speed += 0.5  # Збільшуємо швидкість з кожною пройденою перешкодою

        obstacles(obst_list)
        car(x, y)

        if x > screen_width - car_width or x < 0:
            crash()
            obst_speed = initial_speed  # Скидання швидкості після зіткнення
            score -= 5  # Втрата очок після зіткнення

        for obst in obst_list:
            if y < obst[1] + obst[3]:
                if x > obst[0] and x < obst[0] + obst[2] or x + car_width > obst[0] and x + car_width < obst[0] + obst[2]:
                    crash()
                    obst_speed = initial_speed  # Скидання швидкості після зіткнення
                    score -= 5  # Втрата очок після зіткнення

        # Відображення очок
        font = pygame.font.SysFont(None, 25)
        text = font.render("Очки: " + str(score), True, black)
        screen.blit(text, (0, 0))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

game_loop()