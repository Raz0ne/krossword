from time import time
from copy import deepcopy

height, width = map(int, input('height, width: ').split())
if height == width:
    size = input('format: ')  # short or long or both
else:
    size = ''
last_horizontal_idx = width - 1
time_start = time()
# field = np.chararray((height, width), unicode=True)
field = [['' for x in range(width)] for y in range(height)]
horizontal_words = open(f'words/{width}/{width}.txt', 'r', encoding='utf-8').readlines()
starting_horizontal_words = open(f'words/{width}/{width}start.txt', 'r', encoding='utf-8').readlines()
starting_vertical_words = open(f'words/{height}/{height}start.txt', 'r', encoding='utf-8').readlines()
starts_of_horizontal_words = [open(f'words/{width}/{width}_{length}.txt', 'r', encoding='utf-8').readlines()
                              for length in range(2, width)]
max_cnt_of_additional_words, max_cnt = height, width + height
cur_words = list()
fields = []


def insert_word(word: str, y: int = None, x: int = None):
    if y is None:
        for y in range(height):
            field[y][x] = word[y]
    else:
        for x in range(width):
            field[y][x] = word[x]


def insert_vertical_words(x: int = 0):
    global cur_words
    if x == 0:
        for word in [word for word in open(f'words/{height}/{field[0][0]}.txt', 'r', encoding='utf-8')
                     if word in starting_vertical_words]:
            if word in cur_words:
                continue
            insert_word(word, x=0)
            cur_words.append(word)
            insert_vertical_words(1)
            cur_words.pop()
    elif 0 < x < last_horizontal_idx:
        global max_cnt_of_additional_words
        for word in open(f'words/{height}/{field[0][x]}.txt', 'r', encoding='utf-8'):
            if word in cur_words:
                continue
            insert_word(word, x=x)
            for y in range(1, height):
                part_of_word = ''.join(field[y][:x + 1]) + '\n'
                if part_of_word not in starts_of_horizontal_words[x - 1]:
                    break
            else:
                # print(field)
                '''if cur_cnt < max_cnt_of_additional_words:
                    continue'''
                cur_words.append(word)
                insert_vertical_words(x + 1)
                cur_words.pop()
    else:
        global max_cnt
        for vertical_word in open(f'words/{height}/{field[0][x]}.txt', 'r', encoding='utf-8'):
            if vertical_word in cur_words:
                continue
            insert_word(vertical_word, x=x)
            additional_words = set()
            additional_words.add(vertical_word)
            for y in range(1, height):
                word = ''.join(field[y]) + '\n'
                if word not in horizontal_words:
                    break
                additional_words.add(word)
            else:
                cnt_of_cur_additional_words = len(additional_words)
                if cnt_of_cur_additional_words < max_cnt_of_additional_words:
                    continue
                cnt_of_cur_words = len(additional_words.union(set(cur_words)))
                if cnt_of_cur_words < max_cnt:
                    continue
                '''if cnt_of_cur_words > max_cnt:
                    fields.clear()
                    max_cnt = cnt_of_cur_words
                    max_cnt_of_additinal_words = cnt_of_cur_add_words'''
                fields.append(deepcopy(field))


def decrease_on2():
    for cur_field in fields:
        reversed_field = list([cur_field[x][y] for x in range(width)] for y in range(height))
        fields.remove(reversed_field)


def write_to_file():
    global size
    path = f'answers/{height}x{width}'
    if height == width:
        if size == 'short':
            decrease_on2()
        if size != 'both':
            path += f'_{size}'
        else:
            path += '_long'
    with open(path + '.txt', 'w') as f:
        f.write(str(len(fields)) + '\n\n')
        for cur_field in fields:
            f.writelines(''.join(cur_field[y]) + '\n' for y in range(height))
            f.write('\n')
    if size == 'both':
        size = 'short'
        write_to_file()


def fill_field() -> None:
    global fields
    for first_horizontal_word in starting_horizontal_words:
        #print(first_horizontal_word[:-1])
        insert_word(first_horizontal_word, y=0)
        cur_words.append(first_horizontal_word)
        insert_vertical_words()
        cur_words.pop()
    print(time() - time_start, len(fields))
    write_to_file()
    print(len(fields))


fill_field()
print()
'''for cur_field in fields:
    for y in range(height):
        print(''.join(cur_field[y]))
    print()'''
# change 1
