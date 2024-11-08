"""
Описание игрока компьютера
"""

import numpy as np

# Параметры среды
NUM_EPISODES = 500

# Параметры Q-Learning
LEARNING_RATE = 0.1  # Скорость обучения alpha


class MasPlayer:
    """
    Описание игрока компьютера
    """

    def __init__(self, sing_players: list[str], size: int = 3, num_player: int = 0):
        """
        Инициализация игрока компьютера
        :param size: размер игрового поля
        :param sing_players: список символов игроков
        :param num_player: номер игрока за которого играет компьютер
        """
        self.areal = []
        self.size = size
        self.sing_players = sing_players
        self.my_num_player = num_player
        self.other = (num_player + 1) % 2
        self.len_win = min(self.size, 5)
        # Инициализация Q-таблицы
        self.Q = np.zeros((self.size, self.size))

    def set_areal(self, areal: list[list[str]]):
        """
        Установка нового игрового поля
        :param areal: новое игровое поле
        """
        self.areal = areal

    def set_player(self, num_player: int):
        """
        Установка номера игрока компьютера
        :param num_player:
        :return:
        """
        self.clear_q()
        self.my_num_player = num_player
        self.other = (num_player + 1) % 2

    def set_size(self, size: int):
        """
        Установка размера игрового поля
        :param size:
        :return:
        """
        self.size = size
        self.Q = np.zeros((self.size, self.size))

    def empty_areal(self):
        """
        Проверка на первый ход
        """
        for i in self.areal:
            if 'x' in i or '0' in i:
                return False
        return True

    def check_vin(self, ar: list[str], num_player: int):
        """
        Проверка на возможность победы одним ходом
        :param ar: часть игрового поля
        :param num_player: номер игрока для которого осуществляется проверка
        :return: Если победа возможна, то номер элемента для победы, иначе -1
        """
        count = len(ar)
        if count < self.len_win:
            return -1
        if not ('*' in ar):
            return -1
        for i in range(count):
            if ar[i] == '*':
                test = [ar[j] if j != i else self.sing_players[num_player] for j in range(count)]
                res = self.win_v2(test, self.len_win)
                if res == num_player:
                    return i
        return -1

    def search_win(self, num_player: int):
        """
        Поиск ячейки обеспечивающей победу
        :param num_player: номер игрока
        :return: номер строи и столбца победной ячейки
        """
        for i in range(self.size):
            ar = self.areal[i]
            win = self.check_vin(ar, num_player)
            if not (win == -1):
                return i, win
            ar = [self.areal[j][i] for j in range(self.size)]
            win = self.check_vin(ar, num_player)
            if not (win == -1):
                return win, i
        for k in range(-self.size + 1, self.size):
            ar = [self.areal[i + k][i] for i in range(self.size) if self.size > i + k >= 0]
            win = self.check_vin(ar, num_player)
            if not (win == -1):
                if k < 0:
                    return win - k, win
                else:
                    return win, win + k
            ar = [self.areal[i + k][self.size - 1 - i] for i in range(self.size) if self.size > i + k >= 0]
            win = self.check_vin(ar, num_player)
            if not (win == -1):
                if k < 0:
                    return win, win + k
                else:
                    return win + k, self.size - win - 1
        return -1, -1

    def possible_win(self, ar: list[str], num_player: int):
        """
        Проверка возможности победы на этом участке поля
        :param ar: часть игрового поля
        :param num_player: номер игрока
        :return:
        """
        count = 0
        for i in ar:
            if i in ['*', self.sing_players[num_player]]:
                count += 1
            elif count >= self.len_win:
                break
            else:
                count = 0
        if count >= self.len_win:
            return True
        else:
            return False

    def update_cells(self, list_cells: list[tuple[int, int]]):
        """
        Обновление значений Q
        :param list_cells: координаты ячеек
        :return:
        """
        ar = [self.areal[i][j] for i, j in list_cells]
        pos_my_win = self.possible_win(ar, self.my_num_player)
        pos_other_win = self.possible_win(ar, self.other)
        if pos_my_win and pos_other_win:
            price = 3 * LEARNING_RATE
        elif pos_other_win and not pos_my_win:
            price = - LEARNING_RATE
        else:
            price = LEARNING_RATE
        for i, j in list_cells:
            if self.areal[i][j] == '*':
                self.Q[i][j] += price

    def win_v2(self, ar: list[str], len_win: int):
        """
        Проверка есть ли победитель
        :param ar: проверяемая часть игрового поля
        :param len_win: количество символов для победы
        :return: 0 - победитель "крестик", 1 - победитель "нолик", -1 - нет победителя
        """
        if not ('x' in ar or '0' in ar):
            return -1
        if len(ar) < len_win:
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
            if vin_var >= len_win:
                if char == 'x':
                    return 0
                else:
                    return 1
        return -1

    def update_q(self):
        """
        Обновление значений Q
        :return:
        """
        for i in range(self.size):
            list_t = [(i, j) for j in range(self.size)]
            self.update_cells(list_t)
            list_t = [(j, i) for j in range(self.size)]
            self.update_cells(list_t)
        for k in range(-self.size + 1, self.size):
            list_t = [(i + k, i) for i in range(self.size) if self.size > i + k >= 0]
            self.update_cells(list_t)
            list_t = [(i + k, self.size - 1 - i) for i in range(self.size) if self.size > i + k >= 0]
            self.update_cells(list_t)

    def step(self):
        """
        Шаг игры
        :return:
        """
        if self.empty_areal():
            # Действия при пустом поле
            row = np.random.randint(0, self.size)
            col = np.random.randint(0, self.size)
            return row, col
        # поиск комбинаций своей победы
        row, col = self.search_win(self.my_num_player)
        if not (row == -1 or col == -1):
            return row, col
        # поиск комбинаций чужой победы
        row, col = self.search_win(self.other)
        if not (row == -1 or col == -1):
            return row, col
        # поиск лучшей позиции по оценки
        self.update_q()
        t = - 100
        for i in range(self.size):
            for j in range(self.size):
                if t < self.Q[i][j] and self.areal[i][j] == '*':
                    t = self.Q[i][j]
                    row, col = i, j
        return row, col

    def clear_q(self):
        self.areal = []
        self.Q = np.zeros((self.size, self.size))
