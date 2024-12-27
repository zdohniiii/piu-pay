import pygame
import sys
import urllib.request
import io
from pygame import Color
import ssl
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бесконечное поле с бегущим человечком")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Загрузка фонового изображения
try:
    bg_url = "https://cdn.vectorstock.com/i/1000v/29/41/pixel-game-background-vector-12492941.jpg"
    bg_str = urllib.request.urlopen(bg_url).read()
    bg_file = io.BytesIO(bg_str)
    background = pygame.image.load(bg_file).convert()
    # Масштабируем фон до нужной высоты с сохранением пропорций
    bg_height = HEIGHT
    bg_aspect_ratio = background.get_width() / background.get_height()
    bg_width = int(bg_height * bg_aspect_ratio)
    background = pygame.transform.scale(background, (bg_width, bg_height))

    # Определяем границу между небом и землей (примерно 2/3 высоты изображения)
    GROUND_LEVEL = int(HEIGHT * 2 / 3)
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color = (100, 180, 255) if y < HEIGHT * 2 / 3 else (34, 139, 34)
        pygame.draw.line(background, color, (0, y), (WIDTH, y))
    GROUND_LEVEL = int(HEIGHT * 2 / 3)

# Загрузка спрайтов персонажа
sprite_urls = [
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(1)-Cd6xXUa8u9mVL35h2S6Cpt8JZ8IKB9.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(2)-djtOqGsvjndO4Z4d0F8eU1BreDZQeu.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(3)-lCP89xz7u2NtGzw2z54GxATr7qlRm1.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(4)-YWZ8i4JgDKY0S76BkMTW1GHLKRJCI1.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(5)-bOh4jyjyStWi3Yn7E1nvwwY19zseWa.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(6)-trCnFgQsQocs2yEC2PgXGjILCDcWnG.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(7)-Ber3KxmzlTFONBejcWMRUaNstAPWxD.png",
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/running_man(8)-ib3MGxOzd80MtFwd9oPJBrkiwz7CyV.png"
]

# Создаем нестандартный контекст SSL для игнорирования ошибок сертификата
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Загрузка спрайтов
sprites = []
for url in sprite_urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        sprite_str = urllib.request.urlopen(req, context=ssl_context).read()
        sprite_file = io.BytesIO(sprite_str)
        sprite = pygame.image.load(sprite_file).convert_alpha()

        # Удаление белого фона
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                if sprite.get_at((x, y)) == (255, 255, 255, 255):
                    sprite.set_at((x, y), (255, 255, 255, 0))

        # Уменьшаем размер спрайта в 3 раза
        sprite = pygame.transform.scale(sprite, (sprite.get_width() // 3, sprite.get_height() // 3))
        sprites.append(sprite)
    except Exception as e:
        print(f"Ошибка загрузки спрайта: {e}")

# Изменяем порядок спрайтов для более корректной анимации
sprites = [sprites[0], sprites[1], sprites[2], sprites[3], sprites[4], sprites[5], sprites[4], sprites[3], sprites[2],
           sprites[1]]

if not sprites:
    print("Не удалось загрузить ни одного спрайта. Используем заглушку.")
    fallback_sprite = pygame.Surface((40, 50), pygame.SRCALPHA)
    pygame.draw.rect(fallback_sprite, RED, (0, 0, 40, 50))
    sprites = [fallback_sprite]

# Настройки врагов
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50

# Загрузка спрайта врага
enemy_sprite_url = "https://th.bing.com/th/id/OIP.eYe9JC0lzKsvAvyjWjGXMwAAAA?rs=1&pid=ImgDetMain"
try:
    req = urllib.request.Request(enemy_sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
    enemy_sprite_str = urllib.request.urlopen(req, context=ssl_context).read()
    enemy_sprite_file = io.BytesIO(enemy_sprite_str)
    enemy_sprite = pygame.image.load(enemy_sprite_file).convert_alpha()

    # Удаление белого фона
    for x in range(enemy_sprite.get_width()):
        for y in range(enemy_sprite.get_height()):
            if enemy_sprite.get_at((x, y)) == (255, 255, 255, 255):
                enemy_sprite.set_at((x, y), (255, 255, 255, 0))

    enemy_sprite = pygame.transform.scale(enemy_sprite, (ENEMY_WIDTH, ENEMY_HEIGHT))
except Exception as e:
    print(f"Ошибка загрузки спрайта врага: {e}")
    enemy_sprite = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(enemy_sprite, RED, (0, 0, ENEMY_WIDTH, ENEMY_HEIGHT))

# Настройки стрельбы
BULLET_SPEED = 10
BULLET_SIZE = 10
bullets = []  # список для хранения пуль: [x, y, direction]
SHOOT_COOLDOWN = 0.5  # задержка между выстрелами в секундах
shoot_timer = 0

# Создание флага
FLAG_WIDTH = 30
FLAG_HEIGHT = 40
flag_surface = pygame.Surface((FLAG_WIDTH, FLAG_HEIGHT), pygame.SRCALPHA)
pygame.draw.line(flag_surface, BLACK, (5, 0), (5, FLAG_HEIGHT), 2)
pygame.draw.polygon(flag_surface, RED, [(5, 5), (25, 15), (5, 25)])

# Настройки анимации
current_frame = 0
animation_speed = 0.1
animation_time = 0

# Настройки игрока и флага
player_x, player_y = WIDTH // 2, GROUND_LEVEL
flag_x = player_x + 30
PLAYER_SPEED = 4
MAX_SPEED = 6
MIN_SPEED = 2
ACCELERATION = 0.1
current_speed = PLAYER_SPEED
JUMP_HEIGHT = 30
JUMP_SPEED = 2
is_jumping = False
jump_count = 0
facing_left = False

# Настройки камеры
camera_x = 0
camera_y = 0

# Счетчик очков
score = 0
score_started = False
max_player_x = player_x

# Настройки врагов
enemies = []  # список для хранения врагов: [x, y]
ENEMY_SPAWN_RATE = 2
enemy_spawn_timer = 0

# Основной игровой цикл
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                jump_count = JUMP_HEIGHT
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                if shoot_timer <= 0:
                    # Создаем пулю из центра персонажа
                    bullet_x = player_x 
                    bullet_y = player_y - sprites[current_frame].get_height() // 2
                    direction = -1 if facing_left else 1
                    bullets.append([bullet_x, bullet_y, direction])
                    shoot_timer = SHOOT_COOLDOWN

    # Обновление таймера стрельбы
    if shoot_timer > 0:
        shoot_timer -= dt

    keys = pygame.key.get_pressed()
    is_moving = False

    if keys[pygame.K_d]:  # Вправо
        if keys[pygame.K_w]:
            current_speed = min(current_speed + ACCELERATION, MAX_SPEED)
            animation_speed = 0.05  # Ускоренная анимация для бега
        elif keys[pygame.K_LSHIFT]:
            current_speed = MIN_SPEED
            animation_speed = 0.15  # Замедленная анимация для медленной ходьбы
        else:
            current_speed = PLAYER_SPEED
            animation_speed = 0.1  # Обычная скорость анимации
        player_x -= current_speed
        camera_x += int(current_speed)
        facing_left = False
        is_moving = True

        # Начинаем подсчет очков, когда игрок пересекает флажок
        if not score_started and abs(player_x) >= abs(flag_x):
            score_started = True

        # Обновляем счет только если подсчет очков начался и игрок достиг новой максимальной позиции
        if score_started and abs(player_x) > max_player_x:
            score += (abs(player_x) - max_player_x) // 50
            max_player_x = abs(player_x)
    elif keys[pygame.K_a]:  # Влево
        if keys[pygame.K_w]:
            current_speed = min(current_speed + ACCELERATION, MAX_SPEED)
            animation_speed = 0.05  # Ускоренная анимация для бега
        elif keys[pygame.K_LSHIFT]:
            current_speed = MIN_SPEED
            animation_speed = 0.15  # Замедленная анимация для медленной ходьбы
        else:
            current_speed = PLAYER_SPEED
            animation_speed = 0.1  # Обычная скорость анимации
        player_x += current_speed
        camera_x -= int(current_speed)
        facing_left = True
        is_moving = True
    else:
        current_speed = PLAYER_SPEED
        is_moving = False

    # Обновление анимации
    if is_moving:
        animation_time += dt
        if animation_time >= animation_speed:
            animation_time = 0
            current_frame = (current_frame + 1) % len(sprites)
    else:
        current_frame = 0
        animation_time = 0

    # Обработка прыжка
    if is_jumping:
        if jump_count >= -JUMP_HEIGHT:
            player_y -= int((jump_count * abs(jump_count)) * 0.03)
            jump_count -= JUMP_SPEED
        else:
            is_jumping = False
            jump_count = 0
            player_y = GROUND_LEVEL

    # Обновление позиций пуль и удаление тех, что ушли за экран
    for bullet in bullets[:]:
        bullet[0] += BULLET_SPEED * bullet[2]
        # Удаляем пули, которые ушли за пределы экрана
        if abs(bullet[0] - player_x) > WIDTH:
            bullets.remove(bullet)

    # Генерация врагов
    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
        enemy_spawn_timer = 0
        enemy_x = player_x + random.randint(-WIDTH * 2, WIDTH * 2)
        enemies.append([enemy_x, GROUND_LEVEL - ENEMY_HEIGHT])

    # Обновление позиций врагов и проверка столкновений с пулями
    for enemy in enemies[:]:
        # Проверяем столкновение с каждой пулей
        enemy_rect = pygame.Rect(enemy[0] - camera_x, enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0] - camera_x - BULLET_SIZE // 2,
                                      bullet[1] - BULLET_SIZE // 2,
                                      BULLET_SIZE, BULLET_SIZE)
            if bullet_rect.colliderect(enemy_rect):
                # При попадании удаляем и пулю, и врага
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 10  # Добавляем очки за уничтожение врага
                break

    # Удаление врагов, ушедших далеко от игрока
    enemies = [[ex, ey] for ex, ey in enemies if abs(ex - player_x) <= WIDTH * 2]

    # Проверка столкновений игрока с врагами
    player_rect = pygame.Rect(WIDTH // 2 - sprites[current_frame].get_width() // 2,
                              player_y - sprites[current_frame].get_height(),
                              sprites[current_frame].get_width(),
                              sprites[current_frame].get_height())

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0] - camera_x, enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
        if player_rect.colliderect(enemy_rect):
            print("Игра окончена! Вы столкнулись с врагом.")
            pygame.quit()
            sys.exit()

    # Отрисовка повторяющегося фона
    screen.fill(WHITE)

    # Вычисляем смещение фона для создания эффекта параллакса
    bg_offset = camera_x % background.get_width()

    # Отрисовываем два изображения фона рядом для плавного перехода
    screen.blit(background, (-bg_offset, 0))
    screen.blit(background, (background.get_width() - bg_offset, 0))

    # Отрисовка флага
    flag_screen_x = (flag_x - camera_x) - FLAG_WIDTH // 2
    flag_screen_y = GROUND_LEVEL - FLAG_HEIGHT
    screen.blit(flag_surface, (flag_screen_x, flag_screen_y))

    # Отрисовка врагов
    for enemy in enemies:
        enemy_screen_x = enemy[0] - camera_x
        screen.blit(enemy_sprite, (enemy_screen_x, enemy[1]))

    # Отрисовка пуль
    for bullet in bullets:
        bullet_screen_x = bullet[0] - camera_x
        pygame.draw.circle(screen, YELLOW, (int(bullet_screen_x), int(bullet[1])), BULLET_SIZE // 2)

    # Отрисовка текущего кадра анимации персонажа
    if sprites:
        current_sprite = sprites[current_frame]
        if facing_left:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        # Вычисляем позицию для отрисовки спрайта
        sprite_x = WIDTH // 2 - current_sprite.get_width() // 2
        sprite_y = player_y - current_sprite.get_height()

        screen.blit(current_sprite, (sprite_x, sprite_y))

    # Отображение счетчика очков
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 30))
    screen.blit(score_text, score_rect)

    # Обновление экрана
    pygame.display.flip()

print("Игра завершена")

