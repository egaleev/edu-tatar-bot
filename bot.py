import time
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from db import global_init, Users, create_session
import MyParser
from MyParser import check_user, day_info, table
import json

TOKEN = '1605643472:AAGU6XrjOykQTe_N5PHKR3ulGHSOhOYp73Q'

close = InlineKeyboardButton('❌ Закрыть', callback_data='close')
back = InlineKeyboardButton('◀ Вернуться в главное меню', callback_data='menu')
inline_btn_1 = InlineKeyboardButton('👨‍🎓 Перейти в профиль', callback_data='profile')
inline_btn_2 = InlineKeyboardButton('📔 Расписание на сегодня', callback_data='for_2day')
inline_btn_3 = InlineKeyboardButton('🏫 Расписание на всю неделю', callback_data='week')
main_menu = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, close)


def get_dayly(json_table):
    ans = ''
    if 'нет' == json_table:
        return 'Данный аккаунт является не действительным'
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


class Login(StatesGroup):
    login = State()
    passw = State()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.callback_query_handler(
    lambda callback_query: callback_query.data and callback_query.data.startswith('table_lesson'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                     text=f"Загружаем оценки по предмету 📲")
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
    marks = table(user.login, user.password, user.cookie, '2')
    lessons = marks['lessons'][int(callback_query.data.split('_')[2])]
    lesson_name = lessons['lesson_name']
    marks = lessons['marks']
    if len(marks) == 0:
        answer = f'Урок: {lesson_name}\nОценки: Оценок нет! 🙉'
    else:
        if '.' in marks[-1]:
            all_marks = ', '.join(marks[:-1])
            middle = marks[-1]
            final = ''
        else:
            all_marks = ' '.join(marks[:-2])
            middle = marks[-2]
            final = f"Итоговая оценка: {marks[-1]}"
        answer = f'Урок: {lesson_name}\nВсе оценки: {all_marks}\nСредний бал: {middle}\n{final}'
    back = InlineKeyboardButton('◀ Назад', callback_data='profile_table')
    inline_kb1 = InlineKeyboardMarkup(row_width=1).add(back, close)
    await bot.edit_message_text(answer,
                                callback_query.message.chat.id,
                                callback_query.message.message_id, reply_markup=inline_kb1)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('profile_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
    if callback_query.data == 'profile_logout':
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Выходим из аккаунта 👣")
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        session.delete(user)
        session.commit()
        await bot.send_message(callback_query.message.chat.id,
                               "Привет! 👋\nДля продолжения необходимо указать свои данные\nВ следущем сообщении введите *только логин.*",
            parse_mode=ParseMode.MARKDOWN))
        await Login.login.set()
    elif callback_query.data == 'profile_table':
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Открываем список предметов 📖")
        inline_kb1 = InlineKeyboardMarkup(row_width=2)
        marks = table(user.login, user.password, user.cookie, '2')
        counter = 0
        last_button = None
        for i in marks['lessons']:
            inline_btn_1 = InlineKeyboardButton(f'{i["lesson_name"]}', callback_data=f'table_lesson_{counter}')
            if counter % 2 != 0:
                inline_kb1.row(last_button, inline_btn_1)
            counter += 1
            last_button = inline_btn_1
        back = InlineKeyboardButton('◀ Назад', callback_data='profile')
        inline_kb1.row(back)
        inline_kb1.row(close)
        await bot.edit_message_text('Выберете предмет у которого вы хотите узнать оценки ⬇️',
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=inline_kb1)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('profile'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                     text="Открываем профиль 👨‍🎓")
    inline_btn_1 = InlineKeyboardButton('👩‍🏫 Табель успеваемости', callback_data='profile_table')
    inline_btn_3 = types.InlineKeyboardButton(text='ℹ️ Помощь', url="t.me/stripessssssssssssssssssssssssss")
    inline_btn_2 = InlineKeyboardButton('📵 Выйти ', callback_data='profile_logout')
    inline_kb1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_3, inline_btn_2)
    inline_kb1.row(back, close)
    await bot.edit_message_text('Выберете действие ⬇️',
                                callback_query.message.chat.id,
                                callback_query.message.message_id, reply_markup=inline_kb1)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('week_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    day = callback_query.data.split('_')[1]
    today = str(datetime.datetime.now().weekday())
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
    back = InlineKeyboardButton('◀ Назад', callback_data='week')
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
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Возвращаемся в главное меню ⬅")
        await bot.edit_message_text(f"Здравствуйте, {user.name}!",
                                    callback_query.message.chat.id, callback_query.message.message_id,
                                    reply_markup=main_menu)

    else:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(commands=['start', 'help'], state=None)
async def process_start_command(message: types.Message):
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == message.chat.id).first()
    if user != None:
        await message.reply(f"Здравствуйте, {user.name} ✌️", reply_markup=main_menu)
    else:
        await message.reply(
            "Привет! 👋\nДля продолжения необходимо указать свои данные\nВ следущем сообщении введите *только логин.*",
            parse_mode=ParseMode.MARKDOWN)
        await Login.login.set()


@dp.message_handler()
async def getting_password(msg: types.Message):
    await msg.reply('Я не понимаю вас ☹️\nПопробуйте нажать /start')


@dp.message_handler(state=Login.login)
async def getting_password(msg: types.Message, state: FSMContext):
    login = msg.text
    async with state.proxy() as data:
        data['user_login'] = login
    await bot.send_message(msg.chat.id, 'Отлично 😉, осталось ввести пароль')
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
        await bot.send_message(msg.chat.id,
                               'Добро пожаловать! Обратите внимание, что данный бот все еще находится в разработке и, скорее всего, имеет некоторые баги, но вместе с вами мы сможем их устранить! Если вы заметили какую-либо ошибку, '
                               'обратитесь в поддержку. Мы постараемся решить ваш вопрос как можно скорее. Удачного пользования 😉')
        session = create_session()
        new = Users()
        new.password = password
        new.login = login
        new.tg_id = msg.chat.id
        new.name = MyParser.get_name(login, password)
        new.cookie = a
        session.add(new)
        session.commit()
        await bot.edit_message_text(text=f"Привет, {new.name}!", message_id=da.message_id, chat_id=msg.chat.id,
                                    reply_markup=main_menu)
    else:
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=da.message_id,
                                    text='Видимо вы вели неверные данные 😔\nПопробуйте еще раз')


if __name__ == '__main__':
    global_init("db.sqlite")
    start_polling(dp)
