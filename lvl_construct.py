import pygame


def lvl_parse(puth_to_lvl_txt, sprite_group, class_tail, type_teil='tail'):
    with open(puth_to_lvl_txt, encoding='utf-8') as f:
        for y in range(16):
            tail_line = f.readline().rstrip()
            for x in range(17):
                if type_teil == 'tail':
                    if tail_line[x] == 'v':
                        sprite_group.add(class_tail(False, x * 50, y * 50))
                    elif tail_line[x] == 'h':
                        sprite_group.add(class_tail(True, x * 50, y * 50))
                elif type_teil == 'gg':
                    if tail_line[x] == 'g':
                        sprite_group.add(class_tail(x * 50 + 5, y * 50 + 5))
                elif type_teil == 'enamy':
                    if tail_line[x] == '+':
                        sprite_group.add(class_tail(x * 50 + 5, y * 50 + 5))
                elif type_teil == 'flag':
                    if tail_line[x] == 'f':
                        sprite_group.add(class_tail(x * 50 + 5, y * 50 + 5))


if __name__ == '__main__':
    pass
