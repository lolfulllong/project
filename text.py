import pygame


def load_font(size):
    return pygame.font.Font(r'data/fonts/VisitorRus.ttf', size)


def load_text(font, text):
    return font.render(text, 1, 'white')


def render_text(screen, text, pos):
    screen.blit(text, pos)


if __name__ == '__main__':
    pass
