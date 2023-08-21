import requests
from aiogram import Router, Dispatcher, dispatcher, F, types, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm import state
from aiogram.types import Message, message
import pandas as pd
from openpyxl import load_workbook
import openpyxl
import bot
from keyboards import user_list_choose_kb, phone_kb, tar_kb
from lexicon_ru import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import FSInputFile
from aiogram.methods.send_photo import SendPhoto
from bot import *

class FSMFillForm(StatesGroup):
    fill_start = State()
    fill_name = State()
    fill_FL = State()
    fill_FL_name = State()
    fill_UL = State()
    fill_phone = State()
    fill_email = State()
    fill_FL_pasp = State()
    fill_reg = State()
    fill_dist = State()
    fill_FL_date = State()
    fill_FL_tar = State()
    fill_3 = State()
    fill_6 = State()
    fill_UL_inn = State()
    fill_UL_bik = State()
    fill_UL_count_num = State()
    fill_sell_count = State()

router: Router = Router()
admin_id = 1147300174
users: dict = {}
exfile = FSInputFile('excelusers.xlsx')
pay50 = FSInputFile('50000.jpg')
pay5 = FSInputFile('5000.jpg')


b = 'excelusers.xlsx'
wb = load_workbook(b)
wsf = wb['ФЛ']
wsu = wb['ЮЛ']


#роутер команды старт
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    if message.from_user.id in users:
        del(users[message.from_user.id])
    await message.answer(text=LEXICON_RU['/start'], reply_markup=user_list_choose_kb)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.from_user.id]
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.from_user.username]
    await state.set_state(FSMFillForm.fill_start)

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Заполнение анкеты остановлено\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /start')
    await state.clear()
    users[message.from_user.id].clear()

#роутер команды хелп
@router.message(Command(commands=['help']), ~StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/help'])


# роутер выбора ЮЛ
@router.message(F.text=='ИП/ЮЛ', StateFilter(FSMFillForm.fill_start))
async def process_buy_answer(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.fill_name)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите ИНН')
    await state.set_state(FSMFillForm.fill_UL_inn)

@router.message(F.text, StateFilter(FSMFillForm.fill_UL_inn))
async def process_buy_answer(message: Message, state: FSMContext, bot:Bot):
    await state.set_state(FSMFillForm.fill_name)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите БИК банковского счета')
    await state.set_state(FSMFillForm.fill_UL_bik)

@router.message(F.text, StateFilter(FSMFillForm.fill_UL_bik))
async def process_buy_answer(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.fill_name)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите № расчетного счета')
    await state.set_state(FSMFillForm.fill_UL_count_num)

@router.message(F.text, StateFilter(FSMFillForm.fill_UL_count_num))
async def process_buy_answer(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.fill_name)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите номер телефона или нажмите на кнопку, чобы поделиться текущим номером', reply_markup=phone_kb)
    await state.set_state(FSMFillForm.fill_phone)

# клиент выбрал ФИзическое лицо
@router.message(F.text=='Физическое лицо', StateFilter(FSMFillForm.fill_start))
async def process_buy_answer(message: Message, state: FSMContext):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите серию и номер паспорта через пробел')
    await state.set_state(FSMFillForm.fill_FL_pasp)
    
#роутер если пользователь не выбрал тип
@router.message(StateFilter(default_state))
async def process_sale_wrong(message: Message):
    await message.answer(text='Пожалуйста, выберите из двух кнопок', reply_markup=user_list_choose_kb)

# ввод клиентом серии и номера паспорта
@router.message(F.text.find(' ') != -1, StateFilter(FSMFillForm.fill_FL_pasp))
async def process_buy_answer(message: Message, state: FSMContext):
    s = message.text.split()
    await message.answer(text='Введите дату рождения в формате дд.мм.гггг')
    users[message.from_user.id] = users.get(message.from_user.id, []) + [s[0]]
    users[message.from_user.id] = users.get(message.from_user.id, []) + [s[1]]
    await state.set_state(FSMFillForm.fill_FL_date)

# Непрвильный ввод паспорта
@router.message(StateFilter(FSMFillForm.fill_FL_pasp))
async def process_FL_wrong(message: Message):
    await message.answer(text='Неверный ввод. Введите серию и номер паспорта через пробел')


# Клиент ввёл корректную дату рождения
@router.message(F.text.replace('.', '').isdigit() == True, StateFilter(FSMFillForm.fill_FL_date))
async def process_buy_answer(message: Message, state: FSMContext):
    await message.answer(text='Введите ФИО полностью')
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await state.set_state(FSMFillForm.fill_FL_name)

# Неправильный ввод даты
@router.message(StateFilter(FSMFillForm.fill_FL_date))
async def process_FL_wrong(message: Message):
    await message.answer(text='Неверный ввод. Введите дату рождения в формате дд.мм.гггг')

# Клиент ввёл корректные ФИО, переход в состояние ввода телефона
@router.message(F.text.replace(' ', '').isalpha() == True, StateFilter(FSMFillForm.fill_FL_name))
async def process_buy_answer(message: Message, state: FSMContext):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите номер телефона с +7 или нажмите на кнопку, чобы поделиться текущим номером', reply_markup=phone_kb)
    await state.set_state(FSMFillForm.fill_phone)

# Клиент ввёл некорректные ФИО
@router.message(StateFilter(FSMFillForm.fill_FL_name))
async def process_FL_wrong(message: Message):
    await message.answer(text='Неверный ввод. Введите ФИО в формате *Фамилия Имя Отчество*')

# Клиент поделился телефоном, переход в стостояние ввода почты
@router.message(F.contact, (FSMFillForm.fill_phone))
async def process_buy_answer(message: Message, state: FSMContext):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.contact.phone_number]
    await message.answer(text='Введите почту')
    await state.set_state(FSMFillForm.fill_email)

# Клиент ввел телефон, переход в стостояние ввода почты
@router.message(F.text.replace('+', '').isdigit() == True, (FSMFillForm.fill_phone))
async def process_buy_answer(message: Message, state: FSMContext):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите почту')
    await state.set_state(FSMFillForm.fill_email)

# Клиент ввёл некорректный телефон
@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_FL_phone_wrong(message: Message):
    await message.answer(text='Неверный ввод. Введите номер телефона с +7 без букв и пробелов ')


# Клиент ввел почту, переход в стостояние ввода региона
@router.message(StateFilter(FSMFillForm.fill_email))
async def process_buy_answer(message: Message, state: FSMContext):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await message.answer(text='Введите Город')
    await state.set_state(FSMFillForm.fill_reg)


@router.message(F.text.replace(' ', '').isalpha() == True, StateFilter(FSMFillForm.fill_reg))
async def process_buy_answer(message: Message, state: FSMContext):
    await message.answer(text='Введите Район')
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await state.set_state(FSMFillForm.fill_dist)


@router.message(F.text, StateFilter(FSMFillForm.fill_dist))
async def process_buy_answer(message: Message, state: FSMContext,):
    await message.answer(text='Выберите тарифный план', reply_markup=tar_kb)
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    await state.set_state(FSMFillForm.fill_FL_tar)


@router.message(F.text, StateFilter(FSMFillForm.fill_FL_tar))
async def process_buy_answer(message: Message, state: FSMContext, bot:Bot):
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]
    if message.text == 'Целиком (50000 рублей)':
        await message.answer(text='https://payment.alfabank.ru/shortlink/Zer6wvNm. QRкод на оплату отправлен следующим сообщением. Для повторного заполнения анкеты нажмите /cancel')
        if users[message.from_user.id][2] == "Физическое лицо":
            wsf.append(users.get(message.from_user.id))
            wb.save(b)
            wb.close()
        if users[message.from_user.id][2] == "ИП/ЮЛ":
            wsu.append(users.get(message.from_user.id))
            wb.save(b)
            wb.close()

        await bot.send_message(admin_id, text=f'Появился новый клиент {users[message.from_user.id]}')
        await bot.send_document(admin_id, exfile)


        await message.answer_photo(pay50)
        await state.set_state(FSMFillForm.fill_sell_count)
    if message.text == 'Рассрочка на 3 месяца (55000 рублей)':
        await message.answer(text='Укажите адрес получения договора рассрочки')
        await state.set_state(FSMFillForm.fill_3)
    if message.text == 'Рассрочка на 6 месяцев (65000 рублей)':
        await message.answer(text='Укажите адрес получения договора рассрочки')
        await state.set_state(FSMFillForm.fill_6)

# отправка QR на 3 месяца
@router.message(F.text, StateFilter(FSMFillForm.fill_3))
async def process_buy_answer(message: Message, state: FSMContext,  bot:Bot):
    await message.answer(text='https://payment.alfabank.ru/shortlink/5187WonS. QRкод на оплату отправлен следующим сообщением. Для повторного заполнения анкеты нажмите /cancel')
    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]

    if users[message.from_user.id][2] == "Физическое лицо":
        wsf.append(users.get(message.from_user.id))
        wb.save(b)
        wb.close()
    if users[message.from_user.id][2] == "ИП/ЮЛ":
        wsu.append(users.get(message.from_user.id))
        wb.save(b)
        wb.close()

    await bot.send_message(admin_id, text=f'Появился новый клиент {users[message.from_user.id]}')
    await bot.send_document(admin_id, exfile)

    await message.answer_photo(pay5)
    await state.set_state(FSMFillForm.fill_sell_count)


# отправка QR на 6 месяцев
@router.message(F.text, StateFilter(FSMFillForm.fill_6))
async def process_buy_answer(message: Message, state: FSMContext,  bot:Bot):
    await message.answer(text='https://payment.alfabank.ru/shortlink/5187WonS. Для повторного заполнения анкеты нажмите /cancel')

    users[message.from_user.id] = users.get(message.from_user.id, []) + [message.text]

    if users[message.from_user.id][2] == "Физическое лицо":
        wsf.append(users.get(message.from_user.id))
        wb.save(b)
        wb.close()
    if users[message.from_user.id][2] == "ИП/ЮЛ":
        wsu.append(users.get(message.from_user.id))
        wb.save(b)
        wb.close()

    await bot.send_message(admin_id, text=f'Появился новый клиент {users[message.from_user.id]}')
    await bot.send_document(admin_id, exfile)

    await message.answer_photo(pay5)
    await state.set_state(FSMFillForm.fill_sell_count)









