import pygame
from text import load_font, load_text, render_text
from sound import load_ower
from image import load_image, render_image


def ower():
    pygame.init()
    pygame.display.set_caption('Tank H')
    size = Width, Height = 800, 800
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True

    load_ower()

    img_tank = load_image(r'data/images/tank_gg/tank_gg_right.png')
    img_tank_pos = (200, 452)

    font_lable = load_font(100)
    font = load_font(35)
    text_lable = load_text(font_lable, 'Game Ower!')
    text_lable_pos = (150, 200)
    text_start_game = load_text(font, 'Начать заново')
    text_start_game_pos = (270, 450)
    text_leave_game = load_text(font, 'Выйти в главное меню')
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
                    return 'menu'
                elif event.key == pygame.K_RETURN and img_tank_pos == (200, 452):
                    return 'ret'

        screen.fill((0, 0, 0))
        render_image(screen, img_tank, img_tank_pos)
        render_text(screen, text_lable, text_lable_pos)
        render_text(screen, text_start_game, text_start_game_pos)
        render_text(screen, text_leave_game, text_leave_game_pos)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    ower()
