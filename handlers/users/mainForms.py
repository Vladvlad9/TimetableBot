import json

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest

from crud.usersCRUD import CRUDUser
from keyboards import UserForm
from keyboards.inline.users.mainForm import MainForms
from keyboards.inline.users.all_Callback import main_cb
from loader import dp, bot
from states.users import UserStates


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    get_user = await CRUDUser.get(user_id=message.from_user.id)
    if get_user:
        await message.delete()
        await UserForm.user_exists(message=message)
    else:
        await message.delete()
        await UserForm.user_not_exists(message=message)


@dp.message_handler(commands=["reg"])
async def registration_start(message: types.Message):
    await message.delete()
    await message.answer(text="Привет!", reply_markup=await MainForms.open_site_kb())


@dp.message_handler(content_types="web_app_data") #получаем отправленные данные
async def answer(webAppMes):
    print(webAppMes) #вся информация о сообщении
    print(webAppMes.web_app_data.data) #конкретно то что мы передали в бота
    json_string = json.loads(webAppMes.web_app_data.data)

    text = f"Понедельник - {json_string['Monday']}\n" \
           f"Вторник - {json_string['Tuesday']}\n" \
           f"Среда - {json_string['Wednesday']}\n" \
           f"Четверг - {json_string['Thursday']}\n" \
           f"Пятница - {json_string['Friday']}\n" \
           f"Суббота - {json_string['Saturday']}\n" \
           f"Воскресенье - {json_string['Sunday']}"

    await bot.send_message(text=f"получили инофрмацию из веб-приложения:\n{text}",
                           chat_id=webAppMes.chat.id)
    print('asd')


@dp.callback_query_handler(main_cb.filter())
@dp.callback_query_handler(main_cb.filter(), state=UserStates.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text", "web_app_data"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)
