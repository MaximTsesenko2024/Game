from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
import logging
from config import *
from logic import *

logging.basicConfig(level=logging.INFO)


def generat_keybord(areal: list[list[str]]):
    inline_kb_list = []
    for i in range(len(areal)):
        inline_kb_list.append([])
        for j in range(len(areal[i])):
            inline_kb_list[i].append(InlineKeyboardButton(text=areal[i][j], callback_data=f'Step_{i}_{j}'))

    areal_kb = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    return areal_kb


game_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новая игра'),
            KeyboardButton(text='Вариант игры'),
            KeyboardButton(text='Размер игрового поля')
        ]
    ], resize_keyboard=True
)

size_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="3x3", callback_data=f'Size_3'),
            InlineKeyboardButton(text="5x5", callback_data=f'Size_5'),
            InlineKeyboardButton(text="7x7", callback_data=f'Size_7')
        ]
    ]
)

game_var_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Один игрок крестик", callback_data=f'var_game:cross'),
            InlineKeyboardButton(text="Один игрок нолик", callback_data=f'var_game:zero'),
            InlineKeyboardButton(text="Два игрока", callback_data=f'var_game:two')
        ]
    ]
)

bot = Bot(token=API)
dsp = Dispatcher()
game = Game()


@dsp.message(Command('start'))
async def start(message: Message):
    await message.answer('Добро пожаловать в игру')
    await message.answer('Меню', reply_markup=game_kb)


@dsp.message(F.text == 'Новая игра')
async def new_game(message: Message):
    game.new_game()
    await message.answer(f'Ход игрока {game.get_player()}', reply_markup=generat_keybord(game.get_areal()))


@dsp.message(F.text == 'Вариант игры')
async def var_game(message: Message):
    await message.answer(f'Выберите вариант игры', reply_markup=game_var_kb)


@dsp.message(F.text == 'Размер игрового поля')
async def resize(message: Message):
    await message.answer(f'Выберете размер игрового поля', reply_markup=size_kb)


@dsp.callback_query(F.data.contains('var_game'))
async def set_var_game(call: CallbackQuery):
    size = str(call.data)
    list_ = size.split(':')
    k = None
    if list_[1] == 'cross':
        k = 0
    elif list_[1] == 'zero':
        k = 1
    elif list_[1] == 'two':
        k = 2
    game.select_game(k)
    await call.message.answer('Новая игра')
    await new_game(call.message)
    await call.answer()

    @dsp.callback_query(F.data.contains('Size'))
    async def set_size(call: CallbackQuery):
        size = str(call.data)
        list_ = size.split('_')
        game.set_size(int(list_[1]))
        await call.message.answer('Новая игра')
        await new_game(call.message)
        await call.answer()


@dsp.callback_query(F.data.contains('Step'))
async def step_game(call: CallbackQuery):
    text = str(call.data)
    list_ = text.split('_')
    result = game.step(list_[1], list_[2])
    if result[0] == 'end':
        await call.message.answer(result[1], reply_markup=generat_keybord(game.get_areal()))
        await call.message.answer('Меню', reply_markup=game_kb)
    elif result[0] == 'error':
        await call.message.answer(result[1])
        await call.message.answer(f'Ход игрока {game.get_player()}', reply_markup=generat_keybord(game.get_areal()))
    else:
        await call.message.answer(f'Ход игрока {game.get_player()}', reply_markup=generat_keybord(game.get_areal()))
    await call.answer()


@dsp.message()
async def all_massages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main():
    await bot.delete_webhook()
    await dsp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
