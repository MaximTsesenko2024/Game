"""
Игра в крестики - нолики

Правила:
Первыми делают ход крестики, вторыми - нолики,
до тех пор пока не закончится поле, либо не появится победитель.
Выигрывает тот, кто первым заполнит столбец либо строку, либо диагональ своим знаком.
"""

import tkinter
from tkinter import messagebox, ttk, colorchooser


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


class Settings:
    def __init__(self, size, color):
        self.dict = {3: '3x3', 5: '5x5', 7: '7x7'}
        self.old_settings = {'size': size, 'color': color}
        self.new_settings = {}
        self.select_areal = tkinter.StringVar(value=self.dict[size])
        self.setting = tkinter.Toplevel()
        self.setting.title('Настройки')
        self.setting.geometry("200x200")
        self.setting.resizable(False, False)
        self.lbl = tkinter.Label(master=self.setting, text='Размер игрового поля')
        self.lbl.grid(column=0, row=0)
        self.frame = tkinter.Frame(self.setting)
        self.frame.grid(column=0, row=1, rowspan=3)
        j = 0
        for i in self.dict.keys():
            areal_btn = ttk.Radiobutton(master=self.frame, text=self.dict[i], value=self.dict[i],
                                        variable=self.select_areal)
            areal_btn.grid(column=0, row=j)
            j += 1

        self.btn = tkinter.Button(self.setting, text='Цвет игрового поля', command=self.choice_color)
        self.btn.grid(column=0, row=5)
        self.btn_exit = tkinter.Button(self.setting, text='Выход', command=self.exit)
        self.btn_exit.grid(column=1, row=6)
        self.btn_Ok = tkinter.Button(self.setting, text='Принять', command=self.done)
        self.btn_Ok.grid(column=0, row=6)

    def exit(self):
        self.new_settings = {}
        self.setting.destroy()

    def choice_color(self):
        result = colorchooser.askcolor(self.old_settings['color'])
        if result:
            if result[1] != self.old_settings['color']:
                self.new_settings['color'] = result[1]

    def done(self):
        if self.select_areal.get() != self.dict[self.old_settings['size']]:
            for i in self.dict.keys():
                if self.select_areal.get() == self.dict[i]:
                    self.new_settings['size'] = i
                    break
        self.setting.destroy()

    def show(self):
        self.setting.grab_set()
        self.setting.wait_window()
        return self.new_settings


class Game:
    def __init__(self, size=3):
        self.window = tkinter.Tk()
        self.window.geometry("300x350")
        self.window.resizable(False, False)
        self.window.title('Игра крестики нолики')
        self.player = [['Крестик', 'Нолик'], ['x', '0']]
        self.player_var = tkinter.StringVar()
        self.number_player = 0
        self.size = size
        self.color = 'Grey'
        self.player_var.set(self.player[0][self.number_player])
        self.lbl = tkinter.Label(self.window, text='Ход игрока', width=20)
        self.lbl.grid(column=0, row=0)
        self.lbl_player = tkinter.Label(self.window, textvariable=self.player_var, width=20)
        self.lbl_player.grid(column=1, row=0)
        self.frame = ttk.Frame(self.window)
        self.frame.grid(column=0, row=1, columnspan=3, rowspan=3, ipadx=3, ipady=3, sticky='nswe')
        self.menu = tkinter.Menu(self.window, tearoff=0)
        self.menu.add_cascade(label='Новая игра', command=self.new_game)
        self.menu.add_cascade(label='Настройки', command=self.settings)
        self.menu.add_cascade(label='Выход', command=self.exit_prog)
        self.window.config(menu=self.menu)
        self.areal = []
        self.areal_draw = []
        self.new_game()

    def settings(self):
        update_size = False
        update_color = False
        setting = Settings(size=self.size, color=self.color)
        result = setting.show()
        for key, value in result.items():
            if key == 'color':
                update_color = True
                self.color = value
            elif key == 'size':
                update_size = True
                self.size = value
        if update_color:
            for i in self.areal_draw:
                i['background'] = self.color
            pass
        if update_size:
            if messagebox.askyesno(title='Новая игра', message='Начать новую игру?'):
                self.new_game()

    def new_game(self):
        def create_areal():
            for i in range(self.size):
                self.areal.append([])
                for j in range(self.size):
                    self.areal[i].append('*')
                    btn = tkinter.Button(self.frame, command=lambda k=self.size * i + j: self.click(k),
                                         font=('Arial', 14), background=self.color)
                    btn.grid(column=j, row=i + 1, sticky='nswe', padx=4, pady=4)
                    self.areal_draw.append(btn)

        def config_areal():
            for i in range(self.size):
                self.frame.columnconfigure(index=i, weight=1)
            for i in range(self.size):
                self.frame.rowconfigure(index=i, weight=1)

        if len(self.areal) > 0:
            self.clear()
        config_areal()
        create_areal()
        self.draw('all')

    def click(self, k):
        i, j = k // self.size, k % self.size
        if self.areal[i][j] == '*':
            self.areal[i][j] = self.player[1][self.number_player]
            self.draw(k)
            result = end_game(self.areal)
            if result > -1:
                messagebox.showinfo(title='Победа', message='Игра завершена. Победил %s' % self.player[0][result])
            elif result == -2:
                messagebox.showinfo(title='Ничья', message='Игра завершена. Ничья')
            else:
                self.number_player = (self.number_player + 1) % 2
                self.player_var.set(self.player[0][self.number_player])
            if result != -1:
                result = messagebox.askyesno(title='Новая игра', message='Начать новую игру?')
                if result:
                    self.new_game()
        else:
            messagebox.showwarning(title='Ошибка', message='Ячейка уже занята')

    def draw(self, k):
        if k == 'all':
            for btn in self.areal_draw:
                btn['text'] = '*'
        else:
            self.areal_draw[k]['text'] = self.player[1][self.number_player]

    def clear(self):
        self.areal = []
        for btn in self.areal_draw:
            btn.destroy()
        self.areal_draw = []
        self.number_player = 0

    def exit_prog(self):
        self.window.destroy()
        exit()


def start():
    game = Game()
    update(game.window)


def update(window: tkinter.Tk):
    window.mainloop()


if __name__ == '__main__':
    start()
