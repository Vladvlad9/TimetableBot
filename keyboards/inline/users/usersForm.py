from aiogram import types

from keyboards.inline.users import MainForms


class UserForm:
    @staticmethod
    async def user_exists(message: types.Message):
        await message.answer(text="Главное меню")

    @staticmethod
    async def user_not_exists(message: types.Message):
        await message.answer(text="Что бы пользоваться ботом нужно пройти регистрацию",
                             reply_markup=await MainForms.registration_ikb())
