import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("меню")

# Цвета
GREEN = (68, 148, 74)  # кнопка без наведения
DARK_GREEN = (53, 94, 59)  # кнопка при наведении
RED = (179, 36, 40)  # для текста
WHITE = (255, 255, 255)  # для заглушка

# Шрифты
font_big = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 74)
font_small = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 36)
font_rules = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 24)
font_button = pygame.font.Font(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\ofont.ru_Arco.ttf", 18)


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action, small=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.small = small

    def draw(self, surface):
        # Делаем кнопку без фона только если она маленькая
        if self.small:
            # Цвет текста для маленькой кнопки
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                text_surface = font_button.render(self.text, True, DARK_GREEN)  # Цвет текста при наведении
            else:
                text_surface = font_button.render(self.text, True, self.text_color)  # Обычный цвет текста
        else:
            # Для кнопок с фоном
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


def show_rules():
    # читаем файл
    try:
        with open(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\rules.txt", "r", encoding="utf-8") as file:
            rules_text = file.read()
    except FileNotFoundError:
        rules_text = "Файл с правилами не найден."

    # Кнопка назад
    back_button = Button(WIDTH // 2 - 150, HEIGHT - 100, 300, 50, "Назад", GREEN, RED, show_main_menu)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            back_button.handle_event(event)

        screen.fill(WHITE)

        # Заголовок
        title_text = font_button.render("Правила пользования", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 10))
        screen.blit(title_text, title_rect)

        # Текст правил
        y_offset = HEIGHT // 5
        for line in rules_text.splitlines():
            text_surface = font_rules.render(line, True, RED)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30  # интервал между строками

        # Кнопка назад
        back_button.draw(screen)

        pygame.display.flip()


def show_main_menu():
    try:
        background_image = pygame.image.load(r"C:\Users\zdohn\PycharmProjects\pythonProject\PyGame_Project\phone\bg_menu.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error:
        background_image = None

    # Кнопки
    start_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 100, 290, 65, "Начать игру", GREEN, RED,
                          start_game)
    quit_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 170, 290, 65, "Выйти", GREEN, RED, quit_game)

    # Кнопка для правил
    rules_button = Button(WIDTH // 2 - 100, HEIGHT // - 470, 200, 30, "Правила и условия пользования", GREEN, RED,
                          show_rules, small=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)
            quit_button.handle_event(event)
            rules_button.handle_event(event)

        # фон
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)  # заглушка

        # надпись пиу пау
        title_text = font_big.render("Пиу-Пау", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 7))
        screen.blit(title_text, title_rect)

        # кнопки
        start_button.draw(screen)
        quit_button.draw(screen)
        rules_button.draw(screen)

        pygame.display.flip()


def start_game():
    from main import run_game
    run_game()


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    show_main_menu()
