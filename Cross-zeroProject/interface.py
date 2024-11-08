import tkinter
from tkinter import ttk, messagebox, colorchooser
from logic import *


class Interface:
    def __init__(self, size=3):
        self.window = tkinter.Tk()
        self.dict = {3: '3x3', 5: '5x5', 7: '7x7'}
        self.select_areal = tkinter.StringVar(value=self.dict[size])
        self.var_game_list = ["Один игрок крестик", "Один игрок нолик", "Два игрока"]
        self.sel_var_game = 2
        self.var_game_stVar = tkinter.StringVar(value=self.var_game_list[self.sel_var_game])
        self.window.geometry("300x380")
        self.window.resizable(False, False)
        self.window.title('Игра крестики нолики')
        self.player_var = tkinter.StringVar()
        self.game = Game(size)
        self.color = 'Grey'
        self.player_var.set(self.game.get_player())
        self.var_game_lbl = tkinter.Label(self.window, textvariable=self.var_game_stVar)
        self.var_game_lbl.grid(column=0, row=0)
        self.lbl = tkinter.Label(self.window, text='Ход игрока', width=20)
        self.lbl.grid(column=0, row=1)
        self.lbl_player = tkinter.Label(self.window, textvariable=self.player_var, width=20)
        self.lbl_player.grid(column=1, row=1)
        self.frame = ttk.Frame(self.window)
        self.frame.grid(column=0, row=2, columnspan=3, rowspan=3, ipadx=3, ipady=3, sticky='nswe')
        self.main_menu = tkinter.Menu(self.window, tearoff=0)
        self.var_game_menu = tkinter.Menu(self.window, tearoff=0)
        self.setting_menu = tkinter.Menu(self.window, tearoff=0)
        self.size_game_menu = tkinter.Menu(self.window, tearoff=0)
        self.main_menu.add_cascade(label='Новая игра', command=self.new_game)
        self.main_menu.add_cascade(label='Вариант игры', menu=self.var_game_menu)
        for i in self.var_game_list:
            self.var_game_menu.add_radiobutton(label=i, value=i, variable=self.var_game_stVar, command=self.select_game)
        self.main_menu.add_cascade(label='Настройки', menu=self.setting_menu)
        self.setting_menu.add_cascade(label='Размер игрового поля', menu=self.size_game_menu)
        self.setting_menu.add_cascade(label='Цвет игрового поля', command=self.choice_color)
        for i in self.dict.keys():
            self.size_game_menu.add_radiobutton(label=self.dict[i], value=self.dict[i],
                                                variable=self.select_areal, command=self.size_game)
        self.main_menu.add_cascade(label='Выход', command=self.exit_prog)
        self.window.config(menu=self.main_menu)
        self.areal_draw = []
        self.new_game()


    def size_game(self):
        def find_key_by_value(dict_: dict, value: str | int):
            for k, v in dict_.items():
                if v == value:
                    return k
            return None

        print(self.select_areal.get())
        if self.select_areal.get() == self.dict[self.game.get_size()]:
            return 0
        result = messagebox.askyesno(title='Изменение размера игрового поля',
                                     message=f'Выбран размер {self.select_areal.get()}\n'
                                             f'Изменение размера приведёт началу новой игры.')
        if result:
            self.game.set_size(find_key_by_value(self.dict, self.select_areal.get()))
            self.new_game()

    def select_game(self):
        if self.var_game_stVar.get() == self.var_game_list[self.sel_var_game]:
            return 0
        result = messagebox.askyesno(title='Изменение варианта игры',
                                     message=f'Выбран вариант {self.var_game_stVar.get()}\n'
                                             f'Изменение варианта приведёт началу новой игры.')
        if result:
            self.sel_var_game = self.var_game_list.index(self.var_game_stVar.get())
            self.game.select_game(self.sel_var_game)
            self.new_game()

    def choice_color(self):
        result = colorchooser.askcolor(self.color)
        if result:
            self.color = result[1]
            for i in self.areal_draw:
                i['background'] = self.color


    def new_game(self):
        def create_areal():
            size = self.game.get_size()
            for i in range(size):
                for j in range(size):
                    btn = tkinter.Button(self.frame, command=lambda k=size * i + j: self.click(k),
                                         font=('Arial', 14), background=self.color)
                    btn.grid(column=j, row=i + 1, sticky='nswe', padx=4, pady=4)
                    self.areal_draw.append(btn)

        def config_areal():
            for i in range(self.game.get_size()):
                self.frame.columnconfigure(index=i, weight=1)
            for i in range(self.game.get_size()):
                self.frame.rowconfigure(index=i, weight=1)

        self.clear()
        config_areal()
        create_areal()
        self.game.new_game()
        self.draw('all')

    def click(self, k):
        size = self.game.get_size()
        i, j = k // size, k % size
        result = self.game.step(i, j)
        if self.sel_var_game < 2:
            self.draw('all')
        else:
            self.draw(k)
        if result[0] == 'end' and 'Победил' in result[1]:
            messagebox.showinfo(title='Победа', message=result[1])
        elif result[0] == 'end':
            messagebox.showinfo(title='Ничья', message=result[1])
        elif result[0] == 'error':
            messagebox.showwarning(title='Ошибка', message='Ячейка уже занята')
        else:
            self.player_var.set(self.game.get_player())

    def draw(self, k):
        size = self.game.get_size()
        if k == 'all':
            areal = self.game.get_areal()
            for x in range(len(self.areal_draw)):
                i, j = x // size, x % size
                self.areal_draw[x]['text'] = areal[i][j]
        else:
            i, j = k // size, k % size
            self.areal_draw[k]['text'] = self.game.get_areal()[i][j]

    def clear(self):
        self.game.clear()
        for btn in self.areal_draw:
            btn.destroy()
        self.areal_draw = []

    def exit_prog(self):
        self.window.destroy()
        exit()


def start():
    game = Interface()
    update(game.window)


def update(window: tkinter.Tk):
    window.mainloop()


if __name__ == '__main__':
    start()
