from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.users.all_Callback import main_cb
from keyboards.inline.users import MainForms


class UserForm:
    @staticmethod
    async def user_profile_ikb(target: str) -> InlineKeyboardMarkup:
        data_main_menu = {
            "Назад": target,
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu, callback_data=main_cb.new(target_menu, 0, 0))
                ] for name_menu, target_menu in data_main_menu.items()
            ]
        )

    # @staticmethod
    # async def profile_text(callback: types.CallbackQuery, get_user, get_position):
    #     await callback.message.edit_text(text=f"{get_user.lname} {get_user.fname} {get_user.mname}\n"
    #                                           f"Ваша должность {get_position.name}",
    #                                      reply_markup=await MainForms.main_menu_ikb(
    #                                          user_id=callback.message.from_user.id)
    #                                      )

    @staticmethod
    async def user_exists(message: types.Message):
        await message.answer(text="Главное меню",
                             reply_markup=await MainForms.main_menu_ikb(user_id=message.from_user.id))

    @staticmethod
    async def user_not_exists(message: types.Message):
        await message.answer(text=f"{message.from_user.first_name}, "
                                  "Что бы пользоваться ботом нужно пройти регистрацию",
                             reply_markup=await MainForms.registration_ikb())
