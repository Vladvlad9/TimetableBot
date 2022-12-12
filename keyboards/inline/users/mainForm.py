from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from crud import CRUDUser
from loader import bot
from schemas import UserSchema
from states.users import UserStates

main_cb = CallbackData("main", "target", "id", "editId")


class MainForms:
    @staticmethod
    async def back_ikb(target: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="◀️ Назад", callback_data=main_cb.new(target, 0, 0))
                ]
            ]
        )

    @staticmethod
    async def registration_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Регистрация", callback_data=main_cb.new("Registration", 0, 0))
                ]
            ]
        )

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("main"):
                data = main_cb.parse(callback_data=callback.data)

                if data.get("target") == "Registration":
                    await callback.message.edit_text(text="Введите ФИО")
                    await UserStates.FIO.set()

        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                if await state.get_state() == "UserStates:FIO":
                    fio: list = message.text.split()
                    user_id: int = int(message.from_user.id)

                    if len(fio) < 3:
                        await message.answer(text="Введите полное ФИО!")
                        await UserStates.FIO.set()
                    else:
                        await state.update_data(user_id=user_id)
                        await state.update_data(lname=fio[0].title())
                        await state.update_data(fname=fio[1].title())
                        await state.update_data(mname=fio[2].title())
                        await state.update_data(positions_id=1)
                        data = await state.get_data()

                        print('asd')
                        a = await CRUDUser.add(user=UserSchema(**data))
                        if a:
                            await message.answer(text="Вы успешно зарег. в системе")
