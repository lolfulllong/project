import pygame


def load_main_menu_sound():
    pygame.mixer.music.load('data/sounds/main_menu.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)


def load_game_sound():
    pygame.mixer.music.load('data/sounds/game_musik.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)


def load_ower():
    pygame.mixer.music.load('data/sounds/ower.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.8)


def load_win():
    pygame.mixer.music.load('data/sounds/win.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1)


def load_shoot():
    return pygame.mixer.Sound('data/sounds/shoot.wav')


def load_dead():
    return pygame.mixer.Sound('data/sounds/dead.wav')


if __name__ == '__main__':
    pass
