import pygame
import sys
from main_menu import show_main_menu

pygame.init()

WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню")

# Цвета
GREEN = (68, 148, 74)  # кнопка без наведения
DARK_GREEN = (53, 94, 59)  # кнопка при наведении
RED = (179, 36, 40)  # для текста
WHITE = (255, 255, 255)  # для заглушки

# Шрифты
font_big = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 40)
font_small = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 36)


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        # Создание кнопок с изменением цвета при наведении
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, DARK_GREEN, self.rect)  # цвет при наведении
        else:
            pygame.draw.rect(surface, self.color, self.rect)  # обычный цвет кнопки

        text_surface = font_small.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()


def show_post_game_menu(score):
    try:
        background_image = pygame.image.load(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\phone\bg_post_menu.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error:
        background_image = None

    start_button = Button(WIDTH // 3 - 240, HEIGHT // 2 + 170, 290, 65, "Еще разок", GREEN, RED, start_game)
    quit_button = Button(WIDTH // 3 + 200, HEIGHT // 2 + 170, 290, 65, "Выйти", GREEN, RED, quit_game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)
            quit_button.handle_event(event)

        # Отображаем фон
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)  # Заглушка

        # Текст с результатом
        score_text = font_big.render(f"Ваш результат: {score}", True, RED)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 10 - 20))
        screen.blit(score_text, score_rect)

        # Кнопки
        start_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()


def start_game():
    show_main_menu()


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    show_post_game_menu(1500)
