import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # Ограничиваем перемещение игрока в пределах экрана
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += BULLET_SPEED
        if self.rect.x > WIDTH:
            self.kill()  # Удаляем пулю, если она вышла за границы экрана

# Функция генерации врагов
def generate_enemies(num_enemies):
    enemies = pygame.sprite.Group()
    for _ in range(num_enemies):
        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.Surface((50, 50))
        enemy.image.fill((0, 255, 0))  # Зеленый цвет
        enemy.rect = enemy.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        enemies.add(enemy)
    return enemies

# Главная функция игры
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Shooter")

    # Создаем игрока и группы спрайтов
    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = generate_enemies(5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Создаем пулю
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                if event.key == pygame.K_f:
                    enemies = generate_enemies(5)

        # Обновляем спрайты
        player_group.update()
        bullets.update()
        enemies.update()  # Вызываем обновление врагов (если они имеют динамику)

        # Проверка коллизий между пулями и врагами
        for bullet in bullets:
            if pygame.sprite.spritecollide(bullet, enemies, True):  # Удаляем врага при попадании
                bullet.kill()

        # Отрисовка
        screen.fill(BLACK)
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
