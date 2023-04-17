from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def answer_but(id):
    ans = InlineKeyboardButton('Ответить', callback_data='Ответить:' + str(id))

    ans_but = InlineKeyboardMarkup().add(ans)
    return ans_but
