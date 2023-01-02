import json

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest

from crud.usersCRUD import CRUDUser
from filters import IsAdmin
from keyboards import UserForm, admin_cb, AdminPanel
from keyboards.inline.users.mainForm import MainForms
from keyboards.inline.users.all_Callback import main_cb
from loader import dp, bot
from states.users import UserStates


@dp.message_handler(commands=["admin"], state=UserStates.all_states)
async def sing_in_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.delete()
    await message.answer(
        text=f"<b>{message.from_user.full_name}</b>, вы вошли в админ панель.",
        reply_markup=await AdminPanel.get_admin_panel()
    )


@dp.message_handler(commands=["start"], state=UserStates.all_states)
async def registration_start(message: types.Message, state: FSMContext):
    await state.finish()
    get_user = await CRUDUser.get(user_id=message.from_user.id)
    if get_user:
        await message.delete()
        if get_user.positions_id == 2:
            await message.answer(
                text=f"<b>{get_user.lname}</b>, вы вошли в админ панель.",
                reply_markup=await AdminPanel.get_admin_panel()
            )
        else:
            await UserForm.user_exists(message=message)
    else:
        await message.delete()
        await UserForm.user_not_exists(message=message)


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    get_user = await CRUDUser.get(user_id=message.from_user.id)
    if get_user:
        await message.delete()
        if get_user.positions_id == 2:
            await message.answer(
                text=f"<b>{message.from_user.full_name}</b>, вы вошли в админ панель.",
                reply_markup=await AdminPanel.get_admin_panel()
            )
        else:
            await UserForm.user_exists(message=message)

    else:
        await message.delete()
        await UserForm.user_not_exists(message=message)


# @dp.message_handler(content_types="web_app_data") #получаем отправленные данные
# async def answer(webAppMes):
#     print(webAppMes) #вся информация о сообщении
#     print(webAppMes.web_app_data.data) #конкретно то что мы передали в бота
#     json_string = json.loads(webAppMes.web_app_data.data)
#
#     text = f"Понедельник - {json_string['Monday']}\n" \
#            f"Вторник - {json_string['Tuesday']}\n" \
#            f"Среда - {json_string['Wednesday']}\n" \
#            f"Четверг - {json_string['Thursday']}\n" \
#            f"Пятница - {json_string['Friday']}\n" \
#            f"Суббота - {json_string['Saturday']}\n" \
#            f"Воскресенье - {json_string['Sunday']}"
#
#     await bot.send_message(text=f"получили инофрмацию из веб-приложения:\n{text}",
#                            chat_id=webAppMes.chat.id)
#     print('asd')
@dp.message_handler(commands=["test"])
async def registration_start(message: types.Message):
    text_update = "Вышло новое обновление\n\n" \
                  "1.В профиле появилась новая кнопка 'Посмотреть расписание' - позволяет увидеть какое вы скинули " \
                  "последнее расписание\n" \
                  "2.Добавлены подсказки\n" \
                  "3.Исправлены мелкие ошибки\n\n" \
                  "‼Напоминаю‼\n" \
                  "Первое что нужно сделать когда хотите добавить расписание это нажать \n" \
                  "❗ Меню ➡️ Старт ... ❗️"

    text = f'‼️Напоминание‼️\n\n'\
           f'Понедельник\n'\
           f'Ты не добавил расписание на 09.01.23 - 15.01.23\n'\
           f'Срок до <b>среды 19:00</b>\n\n' \
           f'(Меню -> Войти ...)'

    user = await CRUDUser.get_all()
    try:
        for users in user:
            await bot.send_message(chat_id=users.user_id,
                                   text=text,
                                   parse_mode="HTML"
                                   )
    except Exception as e:
        print(e)


@dp.callback_query_handler(main_cb.filter())
@dp.callback_query_handler(main_cb.filter(), state=UserStates.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text", "web_app_data"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)
