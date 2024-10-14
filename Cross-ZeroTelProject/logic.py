"""
Описание логики работы программы
"""
"""
Игра в крестики - нолики

Правила:
Первыми делают ход крестики, вторыми - нолики,
до тех пор пока не закончится поле, либо не появится победитель.
Выигрывает тот, кто первым заполнит столбец либо строку, либо диагональ своим знаком.
"""


def print_areal(ar):
    """
    Отрисовка поля игры
    :param ar: - игровое поле
    :return:
    """

    for i in ar:
        print(*i)


def empty_cel(ar, rol, col):
    """
    Проверка на незанятость ячейки
    :param ar: - игровое поле
    :param rol: - номер строки
    :param col: - номер столбца
    :return: True - если ячейка свободна, False - занята
    """
    return ar[rol][col] == '*'


def win(ar):
    """
    Проверка есть ли победитель
    :param ar: проверяемая часть игрового поля
    :return: 1 - победитель "крестик", 0 - победитель "нолик", -1 - нет победителя
    """
    if '*' in ar:
        return -1
    elif ('x' in ar) and not ('0' in ar):
        return 1
    elif ('0' in ar) and not ('x' in ar):
        return 0
    else:
        return -1


def win_v2(ar, size):
    """
    Проерка есть ли победитель
    :param size: размер игрового поля
    :param ar: проверяемая часть игрового поля
    :return: 0 - победитель "крестик", 1 - победитель "нолик", -1 - нет победителя
    """
    if not ('x' in ar or '0' in ar):
        return -1
    vin = min(size, 5)
    if len(ar) < vin:
        return -1
    vin_var = 1
    char = ar[0]
    for i in range(1, len(ar)):
        if char == '*':
            char = ar[i]
        elif char == ar[i]:
            vin_var = vin_var + 1
        else:
            char = ar[i]
            vin_var = 1
        if vin_var >= vin:
            if char == 'x':
                return 0
            else:
                return 1
    return -1


def win_play(ar):
    """
    Определение победителя в игре
    :param ar: - игровое поле
    :return: 0 - победитель "крестик", 1 - победитель "нолик", -1 - нет победителя
    """
    size = len(ar)
    result = -1
    for i in range(len(ar)):
        result = win_v2(ar[i], size)
        if result > -1:
            return result
        result = win_v2(list(ar[j][i] for j in range(size)), size)
        if result > -1:
            return result
    for k in range(-size + 1, size):
        x = [ar[i + k][i] for i in range(size) if size > i + k >= 0]
        result = win_v2(x, size)
        if result > -1:
            return result
        x = [ar[i + k][size - 1 - i] for i in range(size) if size > i + k >= 0]
        result = win_v2(x, size)
        if result > -1:
            return result
    return result


def end_game(ar):
    """
    Определение окончания игры
    :param ar: - игровое поле
    :return: 0 - победитель "крестик", 1 - победитель "нолик", -1 - нет победителя, -2 - Ничья
    """

    res = win_play(ar)
    if res > -1:
        return res
    data = filter(lambda x: '*' in x, ar)
    if len(list(data)) == 0:
        return -2
    return res


class Game:
    def __init__(self, size=3):
        self.player = [['Крестик', 'Нолик'], ['x', '0']]
        self.number_player = 0
        self.size = size
        self.areal = []
        self.new_game()

    def new_game(self):
        def create_areal():
            for i in range(self.size):
                self.areal.append([])
                for j in range(self.size):
                    self.areal[i].append('*')

        if len(self.areal) > 0:
            self.clear()
        create_areal()

    def step(self, row, column):
        if isinstance(row, str):
            row = int(row)
        if isinstance(column, str):
            column = int(column)
        if self.areal[row][column] == '*':
            self.areal[row][column] = self.player[1][self.number_player]
            result = end_game(self.areal)
            if result > -1:
                return 'end', f'Игра завершена. Победил {self.player[0][result]}'
            elif result == -2:
                return 'end', f'Игра завершена. Ничья'
            else:
                self.number_player = (self.number_player + 1) % 2
                return 'next', 1
        else:
            return 'error', 'Ячейка уже занята'

    def get_areal(self):
        return self.areal

    def get_player(self):
        return self.player[0][self.number_player]

    def set_size(self, size):
        self.size = size

    def clear(self):
        self.areal = []
        self.number_player = 0

    def exit_prog(self):
        exit()


def start():
    game = Game()


if __name__ == '__main__':
    start()
