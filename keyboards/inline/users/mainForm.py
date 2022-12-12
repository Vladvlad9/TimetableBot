import json

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from crud import CRUDUser, CRUDPosition
from loader import bot
from schemas import UserSchema
from states.users import UserStates

main_cb = CallbackData("main", "target", "id", "editId")


class MainForms:
    @staticmethod
    async def open_site_kb() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Добаить расписание',
                                   web_app=WebAppInfo(url="https://voluble-palmier-a2b577.netlify.app" + "/form"),
                                   callback_data=main_cb.new("Site", 0, 0)),
                    KeyboardButton(text='Назад',
                                   callback_data=main_cb.new("MainForms", 0, 0))
                ]
            ]
        )

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
    async def main_menu_ikb(user_id: int) -> InlineKeyboardMarkup:
        data_main_menu = {
            "Профиль": {"target": "Profile", "user_id": user_id},
            "Расписание": {"target": "Timetable", "user_id": user_id},
        }
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=name_menu,
                                         callback_data=main_cb.new(target_menu['target'], target_menu['user_id'], 0))
                ] for name_menu, target_menu in data_main_menu.items()
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
    async def approved_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Отправить", callback_data=main_cb.new("Approved", 0, 0))
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

                elif data.get("target") == "MainForms":
                    await callback.message.answer(text="Главное меню",
                                                  reply_markup=await MainForms.main_menu_ikb(user_id=message.from_user.id))

                elif data.get("target") == "Timetable":
                    get_user = await CRUDUser.get(user_id=int(data.get("id")))
                    get_position = await CRUDPosition.get(position_id=get_user.positions_id)
                    await callback.message.delete()
                    await callback.message.answer(text=f"{get_user.lname} {get_user.fname} {get_user.mname}\n"
                                                       f"Ваша должность {get_position.name}",
                                                  reply_markup=await MainForms.open_site_kb())
                    await UserStates.Back.set()

                elif data.get("target") == "Approved":
                    await callback.message.edit_text(text="Вы успешно отправили расписание\n"
                                                          "Главное меню",
                                                     reply_markup=await MainForms.main_menu_ikb(
                                                         user_id=callback.message.from_user.id)
                                                     )

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
                        data = await state.get_data()

                        if await CRUDUser.add(user=UserSchema(**data)):
                            await message.answer(text=f"{fio[0].title()} {fio[1].title()} {fio[2].title()}\n"
                                                      "Вы успешно зарег. в системе\n\n"
                                                      "Главное меню",
                                                 reply_markup=await MainForms.main_menu_ikb(user_id=user_id))
                            await state.finish()

                elif await state.get_state() == "UserStates:Back":
                    if message.content_type == "web_app_data":
                        webAppMes = message.web_app_data.data
                        json_string = json.loads(webAppMes)

                        text = f"Понедельник - {json_string['Monday']}\n" \
                                   f"Вторник - {json_string['Tuesday']}\n" \
                                   f"Среда - {json_string['Wednesday']}\n" \
                                   f"Четверг - {json_string['Thursday']}\n" \
                                   f"Пятница - {json_string['Friday']}\n" \
                                   f"Суббота - {json_string['Saturday']}\n" \
                                   f"Воскресенье - {json_string['Sunday']}"

                        await bot.send_message(text=f"получили инофрмацию из веб-приложения:\n{text}",
                                               chat_id=message.chat.id,
                                               reply_markup=await MainForms.approved_ikb())
                        await state.finish()
