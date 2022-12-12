from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BadRequest

from crud.usersCRUD import CRUDUser
from keyboards import UserForm
from keyboards.inline.users.mainForm import main_cb, MainForms
from loader import dp, bot
from states.users import UserStates


@dp.message_handler(commands=["start"])
async def registration_start(message: types.Message):
    get_user = await CRUDUser.get(user_id=message.from_user.id)
    if get_user:
        await UserForm.user_exists(message=message)
    else:
        await message.answer(text="Что бы пользоваться ботом нужно пройти регистрацию",
                             reply_markup=await MainForms.registration_ikb())


@dp.callback_query_handler(main_cb.filter())
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)
