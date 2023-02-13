from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


# /start
btn_menu = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_menu_1 = KeyboardButton('Профиль')
_btn_menu_2 = KeyboardButton('Товары')
_btn_menu_3 = KeyboardButton('Инструкция')
btn_menu.add(_btn_menu_1, _btn_menu_2)
btn_menu.add(_btn_menu_3)


# Товары
btn_products = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_products_1 = KeyboardButton('Список')
_btn_products_2 = KeyboardButton('Добавить')
_btn_products_3 = KeyboardButton('Удалить')
_btn_products_4 = KeyboardButton('Назад')
btn_products.add(_btn_products_1)
btn_products.add(_btn_products_2, _btn_products_3)
btn_products.add(_btn_products_4)


# Добавить
btn_products_add = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_products_add_1 = KeyboardButton('Ссылка')
# _btn_products_add_2 = KeyboardButton('Ручная')
_btn_products_add_3 = KeyboardButton('Товары')
btn_products_add.add(_btn_products_add_1)
btn_products_add.add(_btn_products_add_3)


# Отменить
btn_cancell = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_cancell_1 = KeyboardButton('Отменить')
btn_cancell.add(_btn_cancell_1)


# назад
btn_end = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_end_1 = KeyboardButton('Назад')
btn_end.add(_btn_end_1)


# Купить подписку
btn_buy_prem = ReplyKeyboardMarkup(resize_keyboard=True)
_btn_buy_prem_1 = KeyboardButton('Купить подписку')
_btn_buy_prem_2 = KeyboardButton('Назад')
btn_buy_prem.add(_btn_buy_prem_1)
btn_buy_prem.add(_btn_buy_prem_2)


# Оплата подписки
inline_kb1 = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('Купить подписку', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('Проверить оплату', callback_data='button2')
inline_kb1.add(inline_btn_1)
inline_kb1.add(inline_btn_2)