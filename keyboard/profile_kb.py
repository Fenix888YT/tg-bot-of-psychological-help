from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

question = InlineKeyboardButton('Задать вопрос', callback_data='quest')
advice_but = InlineKeyboardButton('Случайный совет дня', callback_data='advice')
pr_kb = InlineKeyboardMarkup().add(question, advice_but)

back = InlineKeyboardButton('Назад', callback_data='back')
new_ad = InlineKeyboardButton('Еще совет', callback_data='advice')
ad_but = InlineKeyboardMarkup().add(new_ad, back)

back_but = InlineKeyboardMarkup().add(back)
