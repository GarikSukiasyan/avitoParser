import asyncio
from datetime import datetime
import time
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from tg_bot.config.config import bot, dp, db
from tg_bot.keyboards.users import *
from syncer import sync

from SimpleQIWI import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
# token = ""         # https://qiwi.com/api
# phone = ""
#
# api = QApi(token=token, phone=phone)
#
# # Баланс
# print(api.balance[0])
#
# # Платежи
# print(api.payments)

# for i in api.payments['data']:
#     print('Дата:' + str(i['date']))
#     print('Сумма:' + str(i['sum']['amount']))
#     print('Коментарий:' + str(i['provider']['description']))
#     print('\n\n')

class Test(StatesGroup):
    Q1 = State()
    Q2 = State()




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Проверка наличия в базе
    # Проверка наличия бана
    # Проверка от флуда
    # Проверка лишних данных

    # Регистрируем в базе
    status_user = db.check_the_user(message.from_user.id, message.from_user.last_name, message.from_user.username)

    await bot.send_message(
        message.chat.id,
        "Привет Я телеграм бот для отслеживания новых товаров на avito.ru с моей помощью ты будешь первым узнавать о новых товарах.",
        reply_markup=btn_menu)

    if str(status_user) == "False":
        await bot.send_message(
            message.chat.id,
            "Я посмотрю Ты тут новенький(ая), для тебя был выдан доступ к боту на три дня. Проверь раздел: Профиль")
    elif str(status_user) == "True":
        pass


@dp.message_handler(text="Профиль")
async def send_profil(message: types.Message):
    staus_user_in_db = db.check_user_in_db(message.from_user.id)

    if staus_user_in_db == "Error":
        # Регистрируем в базе
        status_user = db.check_the_user(message.from_user.id, message.from_user.last_name, message.from_user.username)
    else:
        pass

    us_name, us_link, us_num_prod, us_subs, us_time = db.get_my_profil(message.from_user.id)

    con_us_time = datetime.utcfromtimestamp(int(float(us_time))).strftime('%H:%M:%S %d-%m-%Y')

    # Текущая дата
    tek_ti = time.time()
    # Если подписка законченна
    if int(tek_ti) > int(us_time):
        rep_btn_prof = btn_buy_prem

        await bot.send_message(
            message.chat.id,
            """
Поупая подписку Вы поддержите разработчика и получите доступ к боту
Нажимая кнопку купить подписку, будет выставлен счет qiwi на 15 минут который вы можете оплатить и поле получить подписку.
Возврат вредств можно осуществить в течении пяти дней с момента оплаты.""", reply_markup=inline_kb1)

    # Если подписка действует
    elif int(tek_ti) < int(us_time):
        pass

    await bot.send_message(
        message.chat.id,
        "ID: " + str(message.from_user.id) +
        "\nИмя: " + str(us_name) +
        "\nТоваров отслеживаем: " + str(us_num_prod) +
        "\nПодписка до: " + str(con_us_time),
        reply_markup=btn_menu)


@dp.message_handler(text="Купить подписку")
async def send_products(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Что бы купить подписку .....")


@dp.message_handler(text="Товары")
async def send_products(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Выберите действие",
        reply_markup=btn_products)


@dp.message_handler(text="Список")
async def send_help(message: types.Message):
    list_links = db.get_my_list_links(message.from_user.id)
    lst = list_links.replace(',', '').split()

    text_links = ""; x = 0

    for i in lst:
        text_links += f"[{str(x)}]" + i + "\n\n"; x += 1

    await bot.send_message(
        message.chat.id,
        "Список отслеживаемых товаров:\n" + str(text_links))


@dp.message_handler(text="Добавить")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Выберите способ добавления товара на отслеживаение",
        reply_markup=btn_products_add)


@dp.message_handler(text="Ссылка")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Пришлите ссылку c фильтрами",
        reply_markup=btn_cancell)

    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answers_1(message: types.message, state: FSMContext):
    await state.update_data(answer1=message.text)
    data = await state.get_data()
    answer1 = data.get('answer1')

    if answer1 != "Отменить":
        if "https://www.avito.ru" in str(answer1) or "https://m.avito.ru" in str(answer1):
            await message.answer('Ссылка была добавленна ' + str(answer1), reply_markup=btn_products)
            db.add_links_in_db(message.from_user.id, answer1)
        elif "https://www.avito.ru" not in str(answer1) or "https://m.avito.ru" not in str(answer1):
            await message.answer('Убедитесь что бы добавляете ссылку на avito.ru', reply_markup=btn_products)
    elif answer1 == "Отменить":
        await message.answer('Вы отменили действие', reply_markup=btn_products)

    await state.finish()


@dp.message_handler(text="Ручная")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Раздел еще не добавлен",
        reply_markup=btn_cancell)


@dp.message_handler(text="Удалить")
async def send_help(message: types.Message):

    list_links = db.get_my_list_links(message.from_user.id)
    lst = list_links.replace(',', '').split()

    text_links = ""; x = 0

    for i in lst:
        text_links += f"[{str(x)}]" + i + "\n\n"; x += 1

    await bot.send_message(
        message.chat.id,
        "Список отслеживаемых товаров:\n" + str(text_links))

    await bot.send_message(
        message.chat.id,
        "Пришлите номер ссылки для удаления",
        reply_markup=btn_cancell)

    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answers_2(message: types.message, state: FSMContext):
    await state.update_data(answer2=message.text)
    data = await state.get_data()
    answer2 = data.get('answer2')

    if answer2 != "Отменить":
        status_del = db.del_links_in_db(message.from_user.id, answer2)

        await message.answer('Будет удаленна ссылка под номером:' + str(answer2), reply_markup=btn_products)
    elif answer2 == "Отменить":
        await message.answer('Вы отменили действие', reply_markup=btn_products)

    await state.finish()


@dp.message_handler(text="Отменить")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Вы отменили действие",
        reply_markup=btn_products)


@dp.message_handler(text="Инструкция")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Ссылка на инструкцию текстом:" +
        "\nСсылка на видео инструкцию:")


@dp.message_handler(text="Назад")
async def send_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Вы открыли главное меню",
        reply_markup=btn_menu)


# https://pypi.org/project/pyQiwiP2P/

# Купить
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # amount = 1 # Сумма 1 рубль
    # lifetime = 15 # Форма будет жить 15 минут
    # comment = 'Купить арбуз' # Комментарий
    # bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment) # Выставление счета
    # print(bill)
    # await bot.send_message(callback_query.from_user.id,
    #                        f'Сумма: {amount}\nСсылка живет: {lifetime} минут\nСсылка:\n{bill.pay_url}') # Отправляем ссылку человеку


# Проверить
@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # bill_id - номер платежа

    # Клиент отменил заказ? Тогда и счет надо закрыть
    # await p2p.reject(bill_id=new_bill.bill_id)

    # Выставим счет на сумму 228 рублей который будет работать 45 минут
    # new_bill = p2p.bill(bill_id=212332030, amount=228, lifetime=45)
    #
    # status = (p2p.check(bill_id=212332030)).status
    # if status == 'PAID': # Если статус счета оплачен (PAID)
    #     await bot.send_message(callback_query.from_user.id, 'Оплата прошла успешно!')
    # else: # В другом случае
    #     await bot.send_message(callback_query.from_user.id, 'Вы не оплатили счет!')