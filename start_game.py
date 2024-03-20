import pygame
from lvl_construct import lvl_parse
from text import load_font, load_text, render_text
from sound import load_game_sound, load_shoot, load_dead
from data_base import data_base_update
from time import sleep
from win_game import win
from ower_game import ower
from random import choice


def game():
    pygame.init()
    pygame.display.set_caption('Tank H')
    size = Width, Height = 850, 800
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True

    sound_shoot = load_shoot()
    sound_dead = load_dead()
    load_game_sound()

    hp = 3
    lvl = 1
    next_lvl = True

    bullet_direction = 'up'
    gg_pos = None
    flag_pos = (0, 0)
    count_gg_bullet = 10.1
    count_enamy_bullet = 0
    count_enamy_shoot = 0

    reiting = 0

    tails_grop = pygame.sprite.Group()
    flag_group = pygame.sprite.Group()
    tank_gg_group = pygame.sprite.Group()
    tank_enamy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    bullet_enamy_group = pygame.sprite.Group()

    font = load_font(35)

    class Tails(pygame.sprite.Sprite):
        def __init__(self, t_type, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            self.t_type = t_type
            if self.t_type:
                self.count_teil = 0
                self.tail_mass = list()
                self.tail_mass.append(pygame.image.load(r'data/images/wall1/wall1.png'))
                self.tail_mass.append(pygame.image.load(r'data/images/wall1/wall1_2.png'))
                self.tail_mass.append(pygame.image.load(r'data/images/wall1/wall1_3.png'))
                self.image = self.tail_mass[self.count_teil]
            else:
                self.image = pygame.image.load(r'data/images/wall2/wall2.png')

            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            if self.t_type and pygame.sprite.spritecollideany(self, bullet_group) or \
                    self.t_type and pygame.sprite.spritecollideany(self, bullet_enamy_group):
                self.count_teil += 1
                if self.count_teil > 2:
                    self.kill()
                    sound_dead.play()
                else:
                    self.image = self.tail_mass[self.count_teil]

    class Flag(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            nonlocal flag_pos
            self.image = pygame.image.load(r'data/images/flag/flag.png')
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            flag_pos = (self.rect.x, self.rect.y)

        def update(self, *args):
            if pygame.sprite.spritecollideany(self, bullet_enamy_group):
                self.kill()

    class TankEnamy(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            self.count_hp = 3
            self.move_pos = 'down'
            self.speed = 0
            self.gg_mass = list()
            self.gg_mass.append(pygame.image.load(r'data/images/tank_enamy/tank_enamy_down.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_enamy/tank_enamy_up.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_enamy/tank_enamy_right.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_enamy/tank_enamy_left.png'))
            self.image = self.gg_mass[0]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            nonlocal reiting
            if args[0] is not None:
                gg_pos_x = args[0][0]
                gg_pos_y = args[0][1]
                flag_pos_x = args[1][0]
                flag_pos_y = args[1][1]
            if pygame.sprite.spritecollideany(self, bullet_group):
                self.count_hp -= 1
                if self.count_hp == 0:
                    self.kill()
                    reiting = int(reiting) + 1
                    sound_dead.play()
            if pygame.sprite.spritecollideany(self, tails_grop):
                if self.move_pos == 'up':
                    self.rect.y += 3
                if self.move_pos == 'down':
                    self.rect.y -= 3
                if self.move_pos == 'right':
                    self.rect.x -= 3
                if self.move_pos == 'left':
                    self.rect.x += 3
            if self.speed > 0.2:
                if self.rect.x - 20 < gg_pos_x < self.rect.x + 20 and gg_pos_y > self.rect.y:
                    self.move_pos = 'down'
                    self.rect.y += 1
                    self.image = self.gg_mass[0]
                elif self.rect.x - 20 < gg_pos_x < self.rect.x + 20 and gg_pos_y < self.rect.y:
                    self.move_pos = 'up'
                    self.rect.y -= 1
                    self.image = self.gg_mass[1]
                elif (self.rect.y - 20 < gg_pos_y < self.rect.y and gg_pos_x > self.rect.x) or \
                        (self.rect.y - 20 < flag_pos_y < self.rect.y and flag_pos_x > self.rect.x):
                    self.move_pos = 'right'
                    self.rect.x += 1
                    self.image = self.gg_mass[2]
                elif (self.rect.y - 20 < gg_pos_y < self.rect.y + 20 and gg_pos_x < self.rect.x) or \
                        (self.rect.y - 20 < flag_pos_y < self.rect.y and flag_pos_x < self.rect.x):
                    self.move_pos = 'left'
                    self.rect.x -= 1
                    self.image = self.gg_mass[3]
                else:
                    self.move_pos = 'down'
                    self.rect.y += 1
                    self.image = self.gg_mass[0]
                self.speed = 0

            self.speed += 0.1

    class TankGg(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            self.key_is_active = [False, False, False, False]
            self.move_pos = 'up'
            self.tank_up_move = False
            self.tank_down_move = False
            self.tank_right_move = False
            self.tank_left_move = False
            self.gg_mass = list()
            self.gg_mass.append(pygame.image.load(r'data/images/tank_gg/tank_gg_up.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_gg/tank_gg_down.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_gg/tank_gg_right.png'))
            self.gg_mass.append(pygame.image.load(r'data/images/tank_gg/tank_gg_left.png'))
            self.image = self.gg_mass[0]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            nonlocal gg_pos
            gg_pos = (self.rect.x, self.rect.y)
            if not args and self.tank_up_move:
                self.rect.y -= 1
            if not args and self.tank_down_move:
                self.rect.y += 1
            if not args and self.tank_right_move:
                self.rect.x += 1
            if not args and self.tank_left_move:
                self.rect.x -= 1
            elif args and args[0] == 'up' and not any(self.key_is_active):
                self.move_pos = 'up'
                self.key_is_active[0] = True
                self.image = self.gg_mass[0]
                self.tank_up_move = True
            elif args and args[0] == 'up2':
                self.key_is_active[0] = False
                self.tank_up_move = False
            elif args and args[0] == 'down' and not any(self.key_is_active):
                self.move_pos = 'down'
                self.key_is_active[1] = True
                self.image = self.gg_mass[1]
                self.tank_down_move = True
            elif args and args[0] == 'down2':
                self.key_is_active[1] = False
                self.tank_down_move = False
            elif args and args[0] == 'right' and not any(self.key_is_active):
                self.move_pos = 'right'
                self.key_is_active[2] = True
                self.image = self.gg_mass[2]
                self.tank_right_move = True
            elif args and args[0] == 'right2':
                self.key_is_active[2] = False
                self.tank_right_move = False
            elif args and args[0] == 'left' and not any(self.key_is_active):
                self.move_pos = 'left'
                self.key_is_active[3] = True
                self.image = self.gg_mass[3]
                self.tank_left_move = True
            elif args and args[0] == 'left2':
                self.key_is_active[3] = False
                self.tank_left_move = False

            if pygame.sprite.spritecollideany(self, tails_grop):
                if self.move_pos == 'up':
                    self.rect.y += 3
                if self.move_pos == 'down':
                    self.rect.y -= 3
                if self.move_pos == 'right':
                    self.rect.x -= 3
                if self.move_pos == 'left':
                    self.rect.x += 3
            if pygame.sprite.spritecollideany(self, tank_enamy_group):
                sound_dead.play()
                data_base_update(reiting)
                sleep(1)
                self.kill()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, gg_pos, bullet_direction):
            pygame.sprite.Sprite.__init__(self)
            self.bullet_direction = bullet_direction
            self.surf = pygame.Surface((7, 7))
            self.surf.fill('blue')
            self.image = self.surf
            self.rect = self.image.get_rect()
            try:
                if self.bullet_direction == 'up':
                    self.rect.x = gg_pos[0] + 17
                    self.rect.y = gg_pos[1]
                elif self.bullet_direction == 'down':
                    self.rect.x = gg_pos[0] + 17
                    self.rect.y = gg_pos[1] + 30
                elif self.bullet_direction == 'right':
                    self.rect.x = gg_pos[0] + 30
                    self.rect.y = gg_pos[1] + 17
                elif self.bullet_direction == 'left':
                    self.rect.x = gg_pos[0] - 5
                    self.rect.y = gg_pos[1] + 17
            except TypeError:
                self.rect.x = 0
                self.rect.y = 0

        def update(self, *args):
            if pygame.sprite.spritecollideany(self, tails_grop) or \
                    pygame.sprite.spritecollideany(self, tank_enamy_group):
                self.kill()
            if self.bullet_direction == 'up':
                self.rect.y -= 3
            elif self.bullet_direction == 'down':
                self.rect.y += 3
            elif self.bullet_direction == 'right':
                self.rect.x += 3
            elif self.bullet_direction == 'left':
                self.rect.x -= 3

    class BulletEnamy(pygame.sprite.Sprite):
        def __init__(self, enamy_pos_x, enamy_pos_y, move_pos):
            pygame.sprite.Sprite.__init__(self)
            self.move_pos = move_pos
            self.surf = pygame.Surface((7, 7))
            self.surf.fill('red')
            self.image = self.surf
            self.rect = self.image.get_rect()

            if self.move_pos == 'up':
                self.rect.x = enamy_pos_x + 17
                self.rect.y = enamy_pos_y
            elif self.move_pos == 'down':
                self.rect.x = enamy_pos_x + 17
                self.rect.y = enamy_pos_y + 30
            elif self.move_pos == 'right':
                self.rect.x = enamy_pos_x + 30
                self.rect.y = enamy_pos_y + 17
            elif self.move_pos == 'left':
                self.rect.x = enamy_pos_x - 5
                self.rect.y = enamy_pos_y + 17

        def update(self, *args):
            nonlocal hp
            if pygame.sprite.spritecollideany(self, tank_gg_group):
                hp -= 1
            if pygame.sprite.spritecollideany(self, tails_grop) or \
                    pygame.sprite.spritecollideany(self, tank_gg_group):
                self.kill()
            if self.move_pos == 'up':
                self.rect.y -= 3
            elif self.move_pos == 'down':
                self.rect.y += 3
            elif self.move_pos == 'right':
                self.rect.x += 3
            elif self.move_pos == 'left':
                self.rect.x -= 3

    def create_group(puth):
        lvl_parse(puth, tank_enamy_group, TankEnamy, type_teil='enamy')
        lvl_parse(puth, tank_gg_group, TankGg, type_teil='gg')
        lvl_parse(puth, tails_grop, Tails)
        lvl_parse(puth, flag_group, Flag, type_teil='flag')

    while running:
        if next_lvl and lvl == 1:
            create_group(r'data/lvl/lvl1.txt')
            next_lvl = False
        elif next_lvl and lvl == 2:
            create_group(r'data/lvl/lvl2.txt')
            next_lvl = False
        elif next_lvl and lvl == 3:
            create_group(r'data/lvl/lvl3.txt')
            next_lvl = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    return 1
                if event.key == pygame.K_UP:
                    tank_gg_group.update('up')
                    bullet_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    tank_gg_group.update('down')
                    bullet_direction = 'down'
                elif event.key == pygame.K_RIGHT:
                    tank_gg_group.update('right')
                    bullet_direction = 'right'
                elif event.key == pygame.K_LEFT:
                    tank_gg_group.update('left')
                    bullet_direction = 'left'
                if event.key == pygame.K_SPACE:
                    if count_gg_bullet > 3:
                        bullet_group.add(Bullet(gg_pos, bullet_direction))
                        sound_shoot.play()
                        count_gg_bullet = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    tank_gg_group.update('up2')
                elif event.key == pygame.K_DOWN:
                    tank_gg_group.update('down2')
                elif event.key == pygame.K_RIGHT:
                    tank_gg_group.update('right2')
                elif event.key == pygame.K_LEFT:
                    tank_gg_group.update('left2')

        screen.fill((0, 0, 0))
        if count_enamy_bullet > 3:
            try:
                enamy_forward = tank_enamy_group.sprites()[count_enamy_shoot]
            except IndexError:
                count_enamy_shoot = -1
            count_enamy_shoot += 1
            if count_enamy_shoot >= len(tank_enamy_group.sprites()) - 1:
                count_enamy_shoot = -1
            bullet_enamy_group.add(BulletEnamy(enamy_forward.rect.x, enamy_forward.rect.y, enamy_forward.move_pos))
            count_enamy_bullet = 0

        text_lable = load_text(font, f'Танков уничтожено: {reiting}')
        text_lable_pos = (10, 10)
        text_hp = load_text(font, f'hp: {hp}')
        text_hp_pos = (600, 10)
        text_lvl = load_text(font, f'lvl: {lvl}')
        text_lvl_pos = (750, 10)

        if lvl > 3:
            data_base_update(reiting)
            game_cod = win()
            if game_cod == 'menu':
                return 1
            elif game_cod == 'ret':
                return 'ret'
            else:
                return 0
        if hp < 1:
            data_base_update(reiting)
            game_cod = ower()
            if game_cod == 'menu':
                return 1
            elif game_cod == 'ret':
                return 'ret'
            else:
                return 0

        if not tank_gg_group:
            data_base_update(reiting)
            game_cod = ower()
            if game_cod == 'menu':
                return 1
            elif game_cod == 'ret':
                return 'ret'
            else:
                return 0

        if not flag_group:
            data_base_update(reiting)
            game_cod = ower()
            if game_cod == 'menu':
                return 1
            elif game_cod == 'ret':
                return 'ret'
            else:
                return 0
        if not tank_enamy_group:
            data_base_update(reiting)
            reiting = 0
            lvl += 1
            next_lvl = True
            for group in [tails_grop, flag_group, tank_gg_group,
                          tank_enamy_group, bullet_group, bullet_enamy_group]:
                for obj in group:
                    obj.kill()
            bullet_direction = 'up'
            gg_pos = None
            flag_pos = (0, 0)
            count_gg_bullet = 10.1
            count_enamy_bullet = 0
            count_enamy_shoot = 0
            hp = 3

        count_gg_bullet += 0.1
        count_enamy_bullet += 0.1
        render_text(screen, text_lable, text_lable_pos)
        render_text(screen, text_hp, text_hp_pos)
        render_text(screen, text_lvl, text_lvl_pos)

        tank_enamy_group.draw(screen)
        tank_enamy_group.update(gg_pos, flag_pos)

        tails_grop.draw(screen)
        tails_grop.update()

        flag_group.draw(screen)
        flag_group.update()

        tank_gg_group.draw(screen)
        tank_gg_group.update()

        bullet_group.draw(screen)
        bullet_group.update()

        bullet_enamy_group.draw(screen)
        bullet_enamy_group.update(gg_pos, flag_pos)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game()
