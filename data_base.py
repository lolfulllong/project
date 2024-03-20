def data_base_read():
    with open('data/db/db.txt', encoding='utf-8') as f:
        return f.read().rstrip()


def data_base_update(value):
    with open('data/db/db.txt', encoding='utf-8') as f:
        old_value = int(f.read().rstrip())
    with open('data/db/db.txt', 'w', encoding='utf-8') as f:
        f.write(str(old_value + int(value)))


if __name__ == '__main__':
    pass
