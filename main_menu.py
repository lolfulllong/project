import pygame
from sound import load_main_menu_sound
from text import load_font, load_text, render_text
from image import load_image, render_image
from data_base import data_base_read
from start_game import game


def main_game_menu():
    pygame.init()
    pygame.display.set_caption('Tank H')
    size = Width, Height = 800, 800
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    game_code = None

    load_main_menu_sound()

    img = load_image(r'data/images/menu/menu.png')
    img_pos = (0, 0)

    img_tank = load_image(r'data/images/tank_gg/tank_gg_right.png')
    img_tank_pos = (200, 452)

    reiting = data_base_read()
    font = load_font(35)
    text_lable = load_text(font, 'With love for Yandex Lyceum')
    text_lable_pos = (190, 637)
    text_start_game = load_text(font, 'Начать игру')
    text_start_game_pos = (270, 450)
    text_leave_game = load_text(font, 'Выйти из игры')
    text_leave_game_pos = (270, 520)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    img_tank_pos = (200, 523)
                if event.key == pygame.K_UP:
                    img_tank_pos = (200, 452)
                if event.key == pygame.K_RETURN and img_tank_pos == (200, 523):
                    running = False
                elif event.key == pygame.K_RETURN and img_tank_pos == (200, 452):
                    game_code = game()
                    reiting = data_base_read()
        if game_code == 0:
            running = False
        elif game_code == 1:
            screen = pygame.display.set_mode(size)
            load_main_menu_sound()
            game_code = None
        elif game_code == 'ret':
            game_code = game()
            reiting = data_base_read()
            screen = pygame.display.set_mode(size)
            load_main_menu_sound()

        screen.fill((0, 0, 0))
        text_reiting = load_text(font, f'Всего танков уничтожено: {reiting}')
        text_reiting_pos = (10, 10)
        render_image(screen, img, img_pos)
        render_image(screen, img_tank, img_tank_pos)
        render_text(screen, text_lable, text_lable_pos)
        render_text(screen, text_start_game, text_start_game_pos)
        render_text(screen, text_leave_game, text_leave_game_pos)
        render_text(screen, text_reiting, text_reiting_pos)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main_game_menu()
