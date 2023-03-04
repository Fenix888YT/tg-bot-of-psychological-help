from aiogram import Bot, Dispatcher, executor, types
from pymongo import MongoClient
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from admin_list.admins import BOT_TOKEN, MDB_TOKEN
from profiles.help import profile, advice, question_ask, add_advice, add_admin, Admin_add, Advice_add, add_admin_s2, \
    add_advice_s2, add_admin_s3
from profiles.redact import redact_admin, redact_advice, delete

# Mongo connect
client = MongoClient(MDB_TOKEN)
db = client['user']

# Диспетчер
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

uid = None

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await profile(message, db['users'])


@dp.message_handler()
async def start(message: types.Message):
    await profile(message, db['users'])


@dp.callback_query_handler(lambda c: c.data == 'quest' or c.data == 'advice' or c.data == 'back')
async def call_ans(call: types.CallbackQuery):
    await call.message.delete()
    match call.data:
        case "quest":
            await question_ask(call.message)
        case "advice":
            await advice(call.message, db['advices'])
        case "back":
            await profile(call.message, db['users'])


@dp.callback_query_handler(
    lambda c: c.data == 'addik_adm' or c.data == 'addik_adv' or c.data == 'Radm' or c.data == 'Radv')
async def call_adm_ans(call: types.CallbackQuery):
    await call.message.delete()
    match call.data:
        case "addik_adm":
            await add_admin(call.message)
        case "addik_adv":
            await add_advice(call.message)
        case "Radm":
            await redact_admin(call.message, db['users'])
        case "Radv":
            await redact_advice(call.message, db['advices'])


@dp.callback_query_handler(lambda c: c.data.startswith('adv:') or c.data.startswith('adm:'))
async def call_ans(call: types.CallbackQuery):
    await call.message.delete()
    match call.data[:4]:
        case "adv:":
            await delete(call.message, db['advices'], call.data[4:])
        case "adm:":
            await delete(call.message, db['users'], call.data[4:])


@dp.message_handler(state=Admin_add.adm_add)
async def admin_adding_process(message: types.Message):
    global uid
    uid = await add_admin_s2(message, db['users'])


@dp.message_handler(state=Admin_add.adm_name_add)
async def admin_adding_process(message: types.Message, state: FSMContext):
    global uid
    await add_admin_s3(message, db['users'], state, uid)
    uid = None


@dp.message_handler(state=Advice_add.adv_add)
async def advice_adding_process(message: types.Message, state: FSMContext):
    await add_advice_s2(message, db['advices'], state)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
