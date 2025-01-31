import pygame
import sys
import random
from main_menu import show_main_menu
from post_menu import show_post_game_menu

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("пиу пау")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Загрузка звуков
piypau = [pygame.mixer.Sound(r'C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\sound\piu.ogg'),
          pygame.mixer.Sound(r'C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\sound\pay.ogg')]  # звук при выстреле

pygame.mixer.music.load(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\sound\main_music.mp3")  # фоновая музыка
pygame.mixer.music.set_volume(0.2)

# Загрузка фонового изображения
try:
    bg_url = r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\phone\bg_game.jpg"
    background = pygame.image.load(bg_url).convert()
    # Масштабируем фон до нужной высоты с сохранением пропорций
    bg_height = HEIGHT
    bg_aspect_ratio = background.get_width() / background.get_height()
    bg_width = int(bg_height * bg_aspect_ratio)
    background = pygame.transform.scale(background, (bg_width, bg_height))

    # Определяем границу между небом и землей (примерно 6/7 высоты изображения)
    GROUND_LEVEL = int(HEIGHT * 6 / 7)
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color = (100, 180, 255) if y < HEIGHT * 5 / 6 else (34, 139, 34)
        pygame.draw.line(background, color, (0, y), (WIDTH, y))
    GROUND_LEVEL = int(HEIGHT * 6 / 7)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.max_speed = 6
        self.min_speed = 2
        self.acceleration = 0.1
        self.current_speed = self.speed
        self.jump_height = 30
        self.jump_speed = 2
        self.is_jumping = False
        self.jump_count = 0
        self.facing_left = False
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_time = 0
        self.load_sprites()

    def load_sprites(self):
        """Загружает спрайты для анимации игрока."""
        sprite_files = [fr"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\sprite\running_man({i}).png" for
                        i in range(1, 9)]
        self.sprites = []
        for file in sprite_files:
            try:
                sprite = pygame.image.load(file).convert_alpha()
                sprite = pygame.transform.scale(sprite, (sprite.get_width() // 3, sprite.get_height() // 3))
                self.sprites.append(sprite)
            except Exception as e:
                print(f"Ошибка загрузки спрайта {file}: {e}")
        if not self.sprites:
            print("Не удалось загрузить ни одного спрайта. Используем заглушку.")
            fallback_sprite = pygame.Surface((40, 50), pygame.SRCALPHA)
            pygame.draw.rect(fallback_sprite, RED, (0, 0, 40, 50))
            self.sprites = [fallback_sprite]
        self.sprites = [self.sprites[0], self.sprites[1], self.sprites[2], self.sprites[3], self.sprites[4],
                        self.sprites[5], self.sprites[4], self.sprites[3], self.sprites[2], self.sprites[1]]

    def move(self, direction, dt, keys):
        """Обрабатывает движение игрока."""
        is_moving = False
        if direction == 'right':
            if keys[pygame.K_w]:
                self.current_speed = min(self.current_speed + self.acceleration, self.max_speed)
                self.animation_speed = 0.05
            elif keys[pygame.K_LSHIFT]:
                self.current_speed = self.min_speed
                self.animation_speed = 0.15
            else:
                self.current_speed = self.speed
                self.animation_speed = 0.1
            self.x -= self.current_speed
            self.facing_left = False
            is_moving = True
        elif direction == 'left':
            if keys[pygame.K_w]:
                self.current_speed = min(self.current_speed + self.acceleration, self.max_speed)
                self.animation_speed = 0.05
            elif keys[pygame.K_LSHIFT]:
                self.current_speed = self.min_speed
                self.animation_speed = 0.15
            else:
                self.current_speed = self.speed
                self.animation_speed = 0.1
            self.x += self.current_speed
            self.facing_left = True
            is_moving = True
        else:
            self.current_speed = self.speed
        return is_moving

    def update_animation(self, dt, is_moving):
        """Обновляет анимацию игрока."""
        if is_moving:
            self.animation_time += dt
            if self.animation_time >= self.animation_speed:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.sprites)
        else:
            self.current_frame = 0
            self.animation_time = 0

    def jump(self):
        """Обрабатывает прыжок игрока."""
        if self.is_jumping:
            if self.jump_count >= -self.jump_height:
                self.y -= int((self.jump_count * abs(self.jump_count)) * 0.03)
                self.jump_count -= self.jump_speed
            else:
                self.is_jumping = False
                self.jump_count = 0
                self.y = GROUND_LEVEL

    def draw(self, screen, camera_x):
        """Отображает игрока на экране."""
        current_sprite = self.sprites[self.current_frame]
        if self.facing_left:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        sprite_x = WIDTH // 2 - current_sprite.get_width() // 2
        sprite_y = self.y - current_sprite.get_height()
        screen.blit(current_sprite, (sprite_x, sprite_y))

    def get_rect(self):
        """Возвращает прямоугольник для столкновений игрока."""
        return pygame.Rect(WIDTH // 2 - self.sprites[self.current_frame].get_width() // 2,
                           self.y - self.sprites[self.current_frame].get_height(),
                           self.sprites[self.current_frame].get_width(),
                           self.sprites[self.current_frame].get_height())


class Enemy:
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite

    def draw(self, screen, camera_x):
        """Отображает врага на экране."""
        screen.blit(self.sprite, (self.x, self.y))

    def get_rect(self):
        """Возвращает прямоугольник для столкновений врага."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @staticmethod
    def spawn(player_x, flag_x, screen_width, ground_level, enemy_width, enemy_height):
        """Рандомно спавнит врага в радиусе видимости игрока."""
        spawn_side = random.choice(['left', 'right'])
        if spawn_side == 'left':
            x = camera_x + random.randint(200, 300)
        else:
            x = camera_x + random.randint(400, 800)

        return Enemy(x, ground_level - enemy_height, enemy_width, enemy_height, enemy_sprite)


# Настройки врагов
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 50

# Загрузка спрайта врага
enemy_sprite = pygame.image.load(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\sprite\pomidor.png").convert_alpha()
enemy_sprite = pygame.transform.scale(enemy_sprite, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Настройки стрельбы
BULLET_SPEED = 10
BULLET_SIZE = 10
bullets = []
SHOOT_COOLDOWN = 0.5
shoot_timer = 0

# Создание флага
FLAG_WIDTH = 30
FLAG_HEIGHT = 40
flag_surface = pygame.Surface((FLAG_WIDTH, FLAG_HEIGHT), pygame.SRCALPHA)
pygame.draw.line(flag_surface, BLACK, (5, 0), (5, FLAG_HEIGHT), 2)
pygame.draw.polygon(flag_surface, RED, [(5, 5), (25, 15), (5, 25)])


def run_game():
    global shoot_timer, bullets, enemies, score, score_started, max_player_x, camera_x, camera_y, enemy_spawn_timer

    pygame.mixer.music.play(-1)  # включение фоновой музыки

    shoot_timer = 0
    enemy_spawn_timer = 0
    clock = pygame.time.Clock()

    # Настройки игрока и флага
    player = Player(WIDTH // 2, GROUND_LEVEL)
    flag_x = player.x + 30

    # Настройки камеры
    camera_x = 0
    camera_y = 0

    # Счетчик очков
    score = 0
    score_started = False
    max_player_x = player.x

    # Настройки врагов
    enemies = []
    ENEMY_SPAWN_RATE = 2  # начальная скорость спауна врагов
    enemy_spawn_timer = 0

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.is_jumping = True
                    player.jump_count = player.jump_height
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if shoot_timer <= 0:
                        bullet_x = player.x
                        bullet_y = player.y - player.sprites[player.current_frame].get_height() // 2
                        direction = -1 if player.facing_left else 1
                        bullets.append([bullet_x, bullet_y, direction])
                        shoot_timer = SHOOT_COOLDOWN

                        shoot = random.choice(piypau)  # Звук выстрела
                        shoot.play()

        if shoot_timer > 0:
            shoot_timer -= dt

        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_d]:
            is_moving = player.move('right', dt, keys)
            camera_x += int(player.current_speed)
        elif keys[pygame.K_a]:
            is_moving = player.move('left', dt, keys)
            camera_x -= int(player.current_speed)

        player.update_animation(dt, is_moving)
        player.jump()

        if not score_started and abs(player.x) >= abs(flag_x):
            score_started = True

        if score_started and abs(player.x) > max_player_x:
            score += (abs(player.x) - max_player_x) // 50
            max_player_x = abs(player.x)

        # Обновляем пули
        for bullet in bullets[:]:
            bullet[0] += BULLET_SPEED * bullet[2]  # Пули двигаются относительно мира
            if abs(bullet[0] - player.x) > WIDTH:
                bullets.remove(bullet)

        # Уменьшаем интервал спауна врагов с течением времени
        enemy_spawn_timer += dt
        if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            enemy_spawn_timer = 0
            enemies.append(Enemy.spawn(player.x, camera_x, WIDTH, GROUND_LEVEL, ENEMY_WIDTH, ENEMY_HEIGHT))

        # Уменьшаем время спауна врагов, делая их появление более частым
        ENEMY_SPAWN_RATE = max(0.5, ENEMY_SPAWN_RATE - 0.005 * dt)  # Уменьшаем скорость спауна

        # Обработка столкновений с врагами
        for enemy in enemies[:]:
            enemy.draw(screen, camera_x)
            enemy_rect = enemy.get_rect()
            enemy_rect.x -= camera_x
            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0] + camera_x - BULLET_SIZE // 2,
                                          bullet[1] + BULLET_SIZE // 2,
                                          BULLET_SIZE, BULLET_SIZE)
                if bullet_rect.colliderect(enemy_rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 10

        # Обработка столкновений с игроком
        player_rect = player.get_rect()

        for enemy in enemies:
            enemy_rect = enemy.get_rect()
            enemy_rect.x -= camera_x
            if player_rect.colliderect(enemy_rect):
                pygame.mixer.music.pause()
                show_post_game_menu(score)

        # Отображаем экран
        screen.fill(WHITE)

        bg_offset = camera_x % background.get_width()

        screen.blit(background, (-bg_offset, 0))
        screen.blit(background, (background.get_width() - bg_offset, 0))

        # Отображаем флаг
        flag_screen_x = (flag_x - camera_x) - FLAG_WIDTH // 2
        flag_screen_y = GROUND_LEVEL - FLAG_HEIGHT
        screen.blit(flag_surface, (flag_screen_x, flag_screen_y))

        # Отображаем врагов
        for enemy in enemies:
            enemy_screen_x = enemy.x - camera_x
            screen.blit(enemy_sprite, (enemy_screen_x, enemy.y))

        # Отображаем пули
        for bullet in bullets:
            bullet_screen_x = bullet[0] + camera_x  # Учитываем смещение камеры при отображении пули
            bullet_screen_y = bullet[1]
            pygame.draw.circle(screen, YELLOW, (int(bullet_screen_x), int(bullet_screen_y)), BULLET_SIZE // 2)

        # Отображаем игрока
        player.draw(screen, camera_x)

        # Отображаем счет
        font = pygame.font.Font(r'C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf', 36)
        score_text = font.render(f"Результат: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(score_text, score_rect)

        pygame.display.flip()


if __name__ == "__main__":
    show_main_menu()
