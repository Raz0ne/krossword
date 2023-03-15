from os import listdir, SEEK_END, SEEK_SET
from utils import *
# print(*sorted(input().lower().split()), sep='\n')
def inp():
    mas = []
    s = input().lower()
    while s:
        input()
        mas.append(s)
        s = input().lower()
    print(*mas, sep='\n')


def create_full_file(n: int) -> None:
    with open(f'words/{n}/{n}.txt', 'w') as of:
        for file_name in listdir(f'words/{n}')[1:]:
            cur_words = open(f'words/{n}/{file_name}', 'r').readlines()
            of.writelines(cur_words)
            print(file_name)
            of.write('\n')


def create_file_with_first_alphas(n: int):
    tabus = 'йъыь'
    words = open(f'words/{n}/{n}.txt', 'r', encoding='utf-8').readlines()
    with open(f'words/{n}/{n}start.txt', 'w', encoding='utf-8') as of:
        for word in words:
            if not any(tabu in word for tabu in tabus):
                of.write(word)


def create_additional_files(n: int):
    words = open(f'words/{n}/{n}.txt', 'r', encoding='utf-8').readlines()
    lst = [set() for _ in range(n - 2)]
    for word in words:
        for end_idx in range(2, n):
            lst[end_idx - 2].add(word[:end_idx] + '\n')
    # print(lst)
    for length in range(2, n):
        with open(f'words/{n}/{n}_{length}.txt', 'w', encoding='utf-8') as of:
            of.writelines(sorted(lst[length - 2]))


create_additional_files(6)
