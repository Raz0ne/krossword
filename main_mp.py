from time import time
from multiprocessing import Pool
from typing import List
from functools import partial
from copy import deepcopy


# 3x3 - 1.9sec, 4x4 - 193sec, 3x4 - 4.8sec
def fill_field(first_horisontal_word: str, height: int, width: int,
               starting_vertical_words, horizontal_words, last_horizontal_idx, starts_of_horizontal_words,
               max_cnt_of_additional_words, max_cnt) -> List:
    def insert_word(word: str, y: int = None, x: int = None):
        if y is None:
            for y in range(height):
                field[y][x] = word[y]
        else:
            for x in range(width):
                field[y][x] = word[x]

    def insert_vertical_words(x: int = 0):
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
            for word in open(f'words/{height}/{field[0][x]}.txt', 'r', encoding='utf-8'):
                if word in cur_words:
                    continue
                insert_word(word, x=x)
                for y in range(1, height):
                    part_of_word = ''.join(field[y][:x + 1]) + '\n'
                    if part_of_word not in starts_of_horizontal_words[x - 1]:
                        break
                else:
                    cur_words.append(word)
                    insert_vertical_words(x + 1)
                    cur_words.pop()
        else:
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
                    cur_fields.append(deepcopy(field))
                    print(field)

    field = [['' for x in range(width)] for y in range(height)]
    cur_fields = []
    cur_words = [first_horisontal_word]
    insert_word(first_horisontal_word, y=0)
    insert_vertical_words(0)
    return cur_fields


if __name__ == '__main__':
    def decrease_on2():
        for cur_field in fields:
            reversed_field = list([cur_field[x][y] for x in range(width)] for y in range(height))
            if reversed_field in fields and cur_field in fields:
                fields.remove(reversed_field)
            else:
                print(cur_field)


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


    width, height = sorted(map(int, input('width, height: ').split()))
    if height == width:
        size = input('format: ')  # short or long or both
    else:
        size = ''
    last_horizontal_idx = width - 1
    time_start = time()
    horizontal_words = open(f'words/{width}/{width}.txt', 'r', encoding='utf-8').readlines()
    starting_horizontal_words = open(f'words/{width}/{width}start.txt', 'r', encoding='utf-8').readlines()
    starting_vertical_words = open(f'words/{height}/{height}start.txt', 'r', encoding='utf-8').readlines()
    starts_of_horizontal_words = [open(f'words/{width}/{width}_{length}.txt', 'r', encoding='utf-8').readlines()
                                  for length in range(2, width)]
    max_cnt_of_additional_words, max_cnt = height, width + height
    start_time = time()
    with Pool(4) as p:
        all_fields = p.map(partial(fill_field, height=height, width=width,
                                   starting_vertical_words=starting_vertical_words,
                                   horizontal_words=horizontal_words,
                                   last_horizontal_idx=last_horizontal_idx,
                                   starts_of_horizontal_words=starts_of_horizontal_words,
                                   max_cnt_of_additional_words=max_cnt_of_additional_words, max_cnt=max_cnt),
                           starting_horizontal_words)
    fields = []
    for cur_fields in all_fields:
        for cur_field in cur_fields:
            fields.append(cur_field)
    write_to_file()
    print(len(fields))
    print(time() - start_time)
