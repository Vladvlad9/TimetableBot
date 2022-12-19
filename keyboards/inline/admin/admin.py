from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from crud import CRUDUser, CRUDWeek
from loader import bot

admin_cb = CallbackData("admin", "target", "id", "editId")


class AdminPanel:
    @staticmethod
    async def get_admin_panel() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Посмотреть Расписание",
                                         callback_data=admin_cb.new("ShowTimetable", 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def approved_ikb(target: str, user_id: int, user_id_tg: int) -> InlineKeyboardMarkup:
        user = await CRUDUser.get(user_id=user_id_tg)
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Обработать",
                                         callback_data=admin_cb.new("Handle", user_id, user_id_tg)
                                         )
                ],
                [
                    InlineKeyboardButton(text="Дать обратную связь",
                                         callback_data=admin_cb.new("Feedback", user_id, user_id_tg)
                                         )
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=admin_cb.new(target, 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def get_user_ikb(target: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=f"{user.lname} {user.fname}",
                                                         callback_data=admin_cb.new("UserProfile", user.id,
                                                                                    user.user_id))
                                ]
                                for user in await CRUDUser.get_all()
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=admin_cb.new(target, 0, 0))
                                ]
                            ]
        )

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("admin"):
                data = admin_cb.parse(callback_data=callback.data)
                if data.get("target") == "StartAdmin":
                    await callback.message.edit_text(
                        text=f"<b>{callback.message.from_user.full_name}</b>, вы вошли в админ панель.",
                        reply_markup=await AdminPanel.get_admin_panel()
                    )

                elif data.get("target") == "ShowTimetable":
                    await callback.message.edit_text(text="Пользователи которые скинули расписание",
                                                     reply_markup=await AdminPanel.get_user_ikb(target="StartAdmin")
                                                     )

                elif data.get("target") == "UserProfile":
                    user_id: int = int(data.get("id"))
                    user_id_tg: int = int(data.get("editId"))
                    weeks = await CRUDWeek.get(user_id=user_id)

                    text = "Хочу работать так!\n\n" \
                           f"Понедельник - {weeks.Monday}\n" \
                           f"Вторник - {weeks.Tuesday}\n" \
                           f"Среда - {weeks.Wednesday}\n" \
                           f"Четверг - {weeks.Thursday}\n" \
                           f"Пятница - {weeks.Friday}\n" \
                           f"Суббота - {weeks.Saturday}\n" \
                           f"Воскресенье - {weeks.Sunday}\n\n" \
                           f"Пожелание - {weeks.description}"

                    await callback.message.edit_text(text=text,
                                                     reply_markup=await AdminPanel.approved_ikb(target="ShowTimetable",
                                                                                                user_id=user_id,
                                                                                                user_id_tg=user_id_tg))

                elif data.get("target") == "Feedback":
                    bot.send_message(int(data.get('editId')), 'Привет')

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
                pass