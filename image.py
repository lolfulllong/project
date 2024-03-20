import pygame


def render_image(screen, img, pos):
    screen.blit(img, pos)


def load_image(puth):
    return pygame.image.load(puth)


if __name__ == '__main__':
    pass
