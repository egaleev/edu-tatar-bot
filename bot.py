import time
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from db import global_init, Users, create_session
import MyParser
from MyParser import check_user, day_info
import json

TOKEN = '1639033609:AAGav07zaQ8DobbJq-t7RYCFdnYLTKJUGiw'

close = InlineKeyboardButton('❌ Закрыть', callback_data='close')
back = InlineKeyboardButton('◀ Вернуться в главное меню', callback_data='menu')


def get_dayly(json_table):
    ans = ''
    if 'нет' == json_table:
        return 'Данный аккаунт является не действитыльным'
    counter = 1
    for i in json_table["lessons"]:
        if i["homework"] == '' and i['marks'] == '':
            ans += f"{counter}. {i['lesson_time'].split('—')[0]} — {i['lesson_name']}\n"
        elif i["homework"] == '':
            ans += f"{counter}. {i['lesson_time'].split('—')[0]} — {i['lesson_name']}, Оценки: {i['marks']}\n"
        elif i["marks"] == '':
            ans += f"{counter}. {i['lesson_time'].split('—')[0]} — {i['lesson_name']}, ДЗ: {i['homework']}\n"
        else:
            ans += f"{counter}. {i['lesson_time'].split('—')[0]} — {i['lesson_name']}, ДЗ: {i['homework']}, Оценки: {i['marks']}\n"
        ans += '\n'
        counter += 1
    return ans


def get_weekly(day):
    return


class Login(StatesGroup):
    login = State()
    passw = State()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('profile'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(
        callback_query.id,
        text='Не работает', show_alert=True)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('week_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    day = callback_query.data.split('_')[1]
    today = str(datetime.datetime.now().weekday())
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
    if day == today:
        now = datetime.datetime.now()
        s = f"{now.day}/{now.month}/{now.year}"
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(back, close)
        unix_day = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Получаем расписание на сегодня 🔍")
        await bot.edit_message_text(get_dayly(day_info(user.login, user.password, unix_day, user.cookie)),
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)
    elif day > today:
        now = datetime.datetime.now()
        s = f"{now.day + abs(int(day) - int(today))}/{now.month}/{now.year}"
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(back, close)
        unix_day = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Получаем расписание на выбранный вами день 👀")
        await bot.edit_message_text(get_dayly(day_info(user.login, user.password, unix_day, user.cookie)),
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)
    else:
        now = datetime.datetime.now()
        s = f"{now.day - abs(int(today) - int(day))}/{now.month}/{now.year}"
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(back, close)
        unix_day = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Получаем расписание на выбранный вами день 👀")
        await bot.edit_message_text(get_dayly(day_info(user.login, user.password, unix_day, user.cookie)),
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)


@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    if callback_query.data == 'for_2day':
        session = create_session()
        user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
        now = datetime.datetime.now()
        s = f"{now.day}/{now.month}/{now.year}"
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(back, close)
        unix_day = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Получаем расписание на сегодня 🔍")
        await bot.edit_message_text(get_dayly(day_info(user.login, user.password, unix_day, user.cookie)),
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)
    elif callback_query.data == 'week':
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Осталось выбрать день недели 📆")
        inline_btn_1 = InlineKeyboardButton('Понедельник', callback_data='week_0')
        inline_btn_2 = InlineKeyboardButton('Вторник', callback_data='week_1')
        inline_btn_3 = InlineKeyboardButton('Среда', callback_data='week_2')
        inline_btn_4 = InlineKeyboardButton('Четверг', callback_data='week_3')
        inline_btn_5 = InlineKeyboardButton('Пятница', callback_data='week_4')
        inline_btn_6 = InlineKeyboardButton('Суббота', callback_data='week_5')
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4,
                                                           inline_btn_5, inline_btn_6)
        inline_kb1.row(back, close)
        await bot.edit_message_text('Выберете день недели:',
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)
    elif callback_query.data == 'menu':
        session = create_session()
        user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
        inline_btn_1 = InlineKeyboardButton('👨‍🎓 Перейти в профиль', callback_data='profile')
        inline_btn_2 = InlineKeyboardButton('📔 Посмотреть расписание на сегодня', callback_data='for_2day')
        inline_btn_3 = InlineKeyboardButton('🏫 Посмотреть расписание на всю неделю', callback_data='week')
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, close)
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Возвращаемся в главное меню ⬅️")
        await bot.edit_message_text(f"Здравствуйте, {user.name}!",
                                    callback_query.message.chat.id, callback_query.message.message_id,
                                    reply_markup=inline_kb1)

    else:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(commands=['start', 'help'], state=None)
async def process_start_command(message: types.Message):
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == message.chat.id).first()
    if user != None:
        inline_btn_1 = InlineKeyboardButton('👨‍🎓 Перейти в профиль', callback_data='profile')
        inline_btn_2 = InlineKeyboardButton('📔 Посмотреть расписание на сегодня', callback_data='for_2day')
        inline_btn_3 = InlineKeyboardButton('🏫 Посмотреть расписание на всю неделю', callback_data='week')
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, close)
        await message.reply(f"Здравствуйте, {user.name}", reply_markup=inline_kb1)
    else:
        await message.reply("Привет!\nДля продолжения необходимо указать логин и пароль")
        await Login.login.set()


@dp.message_handler()
async def getting_password(msg: types.Message):
    await msg.reply('Я не совсем понимаю что вы имеете ввиду\n Попробуйте нажать /start')


@dp.message_handler(state=Login.login)
async def getting_password(msg: types.Message, state: FSMContext):
    login = msg.text
    async with state.proxy() as data:
        data['user_login'] = login
    await bot.send_message(msg.chat.id, 'Отлично, осталось ввести пароль')
    await Login.passw.set()


@dp.message_handler(state=Login.passw)
async def getting_password(msg: types.Message, state: FSMContext):
    password = msg.text
    data = await state.get_data()
    login = data.get('user_login')
    await state.finish()
    da = await bot.send_message(chat_id=msg.chat.id,
                                text='Проверяем введеные данные...')
    a = check_user(login, password)
    if a:
        session = create_session()
        new = Users()
        new.password = password
        new.login = login
        new.tg_id = msg.chat.id
        new.name = MyParser.get_name(login, password)
        new.cookie = a
        session.add(new)
        session.commit()
        inline_btn_1 = InlineKeyboardButton('👨‍🎓 Перейти в профиль', callback_data='button1')
        inline_btn_2 = InlineKeyboardButton('📔 Посмотреть расписание на сегодня', callback_data='for_2day')
        inline_btn_3 = InlineKeyboardButton('🏫 Посмотреть расписание на всю неделю', callback_data='week')
        inline_kb1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, close)
        await bot.edit_message_text(text=f"Здравствуйте, {new.name}!", message_id=da.message_id, chat_id=msg.chat.id,
                                    reply_markup=inline_kb1)
    else:
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=da.message_id,
                                    text='Видимо вы вели неверные данные(\nПопробуйте еще раз')


if __name__ == '__main__':
    global_init("db.sqlite")
    start_polling(dp)
