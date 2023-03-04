from random import randint
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard.profile_kb import pr_kb, ad_but, back_but
from keyboard.admin_kb import adm_but


class Advice_add(StatesGroup):
    adv_add = State()


class Admin_add(StatesGroup):
    adm_add = State()
    adm_name_add = State()

# class question(StatesGroup):


async def profile(message, user_col):
    user = user_col.find_one({'user_id': str(message.chat.id)})
    if not user:
        await message.answer("Доброго времени суток, мы можем выслушать вас, помочь в трудной ситуации" +
                             " и ответить на ваши вопросы.\nЧто вы хотите выбрать?", reply_markup=pr_kb)
    else:
        await message.answer("Доброго времени суток, чем мог бы я вам помочь?", reply_markup=adm_but)


async def advice(message, adv_col):
    advices = adv_col.find()
    await message.answer('Случайный совет: \n' + advices[randint(0, adv_col.count() - 1)]['text'], reply_markup=ad_but)


async def question_ask(message):
    await message.answer('Здесь должно быть что то, но я еще не сделал прикол с чатом :)', reply_markup=back_but)


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
