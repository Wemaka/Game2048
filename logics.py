import random
from copy import deepcopy


def insert_2or4(mas, coordinates):
    x, y = coordinates[0], coordinates[1]
    if random.randint(1, 100) <= 75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def get_empty_list(mas):
    list_zero = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                list_zero.append((i, j))
    return list_zero


def is_zero_in_mas(mas):
    for i in mas:
        if 0 in i:
            return True
    return False


def move_left(mas):
    delta = 0
    copy_mas = deepcopy(mas)
    for row in mas:
        while 0 in row:
            row.remove(0)
        # if len(row) < 4:
        #     row.extend([0]*(4-len(row)))
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j+1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j+1)
                mas[i].append(0)

    return mas, delta, not copy_mas == mas


def move_right(mas):
    copy_mas = deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) < 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j-1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j-1)
                mas[i].insert(0, 0)
    return mas, delta, not copy_mas == mas


def move_up(mas):
    copy_mas = deepcopy(mas)
    delta = 0
    for j in range(4):
        mas_column = []
        for i in range(4):
            if mas[i][j] != 0:
                mas_column.append(mas[i][j])
        while len(mas_column) < 4:
            mas_column.append(0)
        for i in range(3):
            if mas_column[i] == mas_column[i+1] and mas_column[i] != 0:
                mas_column[i] *= 2
                delta += mas_column[i]
                mas_column.pop(i+1)
                mas_column.append(0)
        for i in range(4):
            mas[i][j] = mas_column[i]
    return mas, delta, not copy_mas == mas


def move_down(mas):
    copy_mas = deepcopy(mas)
    delta = 0
    for j in range(4):
        mas_column = []
        for i in range(4):
            if mas[i][j] != 0:
                mas_column.append(mas[i][j])
        while len(mas_column) < 4:
            mas_column.insert(0, 0)
        for i in range(3, 0, -1):
            if mas_column[i] == mas_column[i-1] and mas_column[i] != 0:
                mas_column[i] *= 2
                delta += mas_column[i]
                mas_column.pop(i-1)
                mas_column.insert(0, 0)
        for i in range(4):
            mas[i][j] = mas_column[i]
    return mas, delta, not copy_mas == mas


def can_move(mas):
    for i in range(4):
        for j in range(4):
            if j < 3 and mas[i][j] == mas[i][j+1]:
                return True
            elif i < 3 and mas[i][j] == mas[i+1][j]:
                return True
    return False
