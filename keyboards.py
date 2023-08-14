from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

# клавиатура выбора клиента
button_1: KeyboardButton = KeyboardButton(text='Физическое лицо')
button_2: KeyboardButton = KeyboardButton(text='ИП/ЮЛ')
user_list_choose_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
user_list_choose_kb_builder.row(button_1, button_2)
user_list_choose_kb = user_list_choose_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True)

# клавиатура номера телефона
phone_button: KeyboardButton = KeyboardButton(text = 'Поделиться номером', request_contact=True)
phone_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
phone_kb_builder.row(phone_button)
phone_kb = phone_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

# клавиатура выбора тарифа
tar_btn1: KeyboardButton = KeyboardButton(text='Целиком (50000 рублей)')
tar_btn2: KeyboardButton = KeyboardButton(text='Рассрочка на 3 месяца (53000 рублей)')
tar_btn3: KeyboardButton = KeyboardButton(text='Рассрочка на 6 месяцев (58000 рублей)')

tar_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
tar_kb_builder.row(tar_btn1, tar_btn2, tar_btn3)
tar_kb = tar_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True)