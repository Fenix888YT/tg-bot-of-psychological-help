from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from bson import ObjectId
from keyboard.profile_kb import back_but


async def redact_advice(message, coll):
    list_but = InlineKeyboardMarkup()
    back = InlineKeyboardButton('Назад', callback_data='back')
    posts = coll.find()
    for i in range(0, posts.count()):
        but = InlineKeyboardButton(posts[i]['text'], callback_data='adv:'+str(posts[i]['_id']))
        list_but.add(but)
    list_but.add(back)
    await message.answer('Все что я нашел,\nнажми чтобы удалить', reply_markup=list_but)


async def delete(message, coll, id):
    coll.delete_one({"_id": ObjectId(id)})
    await message.answer('Успешно удалено!', reply_markup=back_but)


async def redact_admin(message, coll):
    list_but = InlineKeyboardMarkup()
    back = InlineKeyboardButton('Назад', callback_data='back')
    posts = coll.find()
    for i in range(0, posts.count()):
        but = InlineKeyboardButton(posts[i]['name'], callback_data='adm:'+str(posts[i]['_id']))
        list_but.add(but)
    list_but.add(back)
    await message.answer('Все что я нашел, нажми чтобы удалить:', reply_markup=list_but)



