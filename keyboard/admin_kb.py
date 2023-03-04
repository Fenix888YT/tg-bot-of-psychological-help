from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


add_admin_but = InlineKeyboardButton('Добавить нового админа', callback_data='addik_adm')
add_advice_but = InlineKeyboardButton('Добавить новый совет', callback_data='addik_adv')
red_admin_but = InlineKeyboardButton('Список админов', callback_data='Radm')
red_advice_but = InlineKeyboardButton('Список советов', callback_data='Radv')

adm_but = InlineKeyboardMarkup().add(add_admin_but, add_advice_but)
adm_but.add(red_admin_but, red_advice_but)