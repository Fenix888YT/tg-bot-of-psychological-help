from random import randint
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard.profile_kb import pr_kb, ad_but, back_but
from keyboard.admin_kb import adm_but
from keyboard.answer import answer_but

dat = None
class Advice_add(StatesGroup):
    adv_add = State()


class Admin_add(StatesGroup):
    adm_add = State()
    adm_name_add = State()


class question(StatesGroup):
    qu_ask = State()
    qu_ans = State()


async def profile(message, user_col):
    user = user_col.find_one({'user_id': str(message.chat.id)})

    if not user or user['user_id'] == '798892590':
        await message.answer("Доброго времени суток, мы можем выслушать вас, помочь в трудной ситуации" +
                             " и ответить на ваши вопросы.\nЧто вы хотите выбрать?", reply_markup=pr_kb)
    else:
        await message.answer("Доброго времени суток, чем мог бы я вам помочь?", reply_markup=adm_but)


async def advice(message, adv_col):
    advices = adv_col.find()
    await message.answer('Случайный совет: \n' + advices[randint(0, adv_col.count() - 1)]['text'], reply_markup=ad_but)


async def question_ask(message):
    await message.answer('Напиши свой вопрос максимально подробно одним сообщением, после чего просто дождись ответа:',
                         reply_markup=back_but)
    await question.qu_ask.set()


async def question_ask_s2(message, us_col, state, bot):
    users = us_col.find()
    for user in users:
        await bot.send_message(user['user_id'], "Вопрос от пользователя:\n" + message.text,
                           reply_markup=answer_but(message.from_user.id))
    await message.answer('Сообщение отправлено, ожидайте ответа, постараемся помочь в кратчайшие сроки!')
    await state.finish()

async def quest_ans(message, data):
    global dat
    await message.answer('Напиши свой ответ одним сообщением:',
                         reply_markup=back_but)
    await question.qu_ans.set()
    dat = data

async def quest_ans_s2(message, bot, state):
    global dat
    await bot.send_message(dat, message.text)
    await message.answer('Отправлено!',
                         reply_markup=back_but)
    await state.finish()
    dat = None




async def add_advice(message):
    await message.answer('Напишите совет, который смогут увидеть пользователи)')
    await Advice_add.adv_add.set()


async def add_advice_s2(message, adv_col, state):
    adv_col.insert_one({'text': message.text})
    await state.finish()
    await message.answer('Совет успешно сохранен!', reply_markup=back_but)


async def add_admin(message):
    await message.answer('Введите айди будущего работника\nЧтобы его узнать, попроси админа написать ему @userinfobot')
    await Admin_add.adm_add.set()


async def add_admin_s2(message, adm_col):
    adm_col.insert_one({'user_id': message.text})
    await message.answer('А теперь напиши его никнейм!')
    await Admin_add.adm_name_add.set()
    return message.text


async def add_admin_s3(message, user_col, state, uid):
    user_col.update({'user_id': uid}, {"$set": {'name': message.text}})
    await state.finish()
    await message.answer('Админ успешно сохранен!', reply_markup=back_but)

