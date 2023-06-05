import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from config import CONFIG
from crud import CRUDUser, CRUDWeek
from loader import bot
from states.admins.admin import AddMailingFSM
from states.users import UserStates
import logging
admin_cb = CallbackData("admin", "target", "action", "id", "editId")


class AdminPanel:
    @staticmethod
    async def get_admin_panel() -> InlineKeyboardMarkup:
        get_count = await CRUDUser.get_all(get_add=1)
        get_all_count = await CRUDUser.get_all()
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"Все работники ({len(get_all_count)})",
                                         callback_data=admin_cb.new("ShowTimetable", 0, 0, 0)
                                         )
                ],
                [
                    InlineKeyboardButton(text=f"Добавили расписание ({len(get_count)})",
                                         callback_data=admin_cb.new("AddTimetable", 0, 0, 0)
                                         )
                ],
                [
                    InlineKeyboardButton(text=f"Рассылка кто не добавил расписание",
                                         callback_data=admin_cb.new("NewsletterUser", 0, 0, 0)
                                         )
                ],
                [
                    InlineKeyboardButton(text=f"Рассылка Всем",
                                         callback_data=admin_cb.new("NewsletterAll", 0, 0, 0)
                                         )
                ],
                [
                    InlineKeyboardButton(text=f"Удалить расписание",
                                         callback_data=admin_cb.new("DeleteSchedule", "getSchedule", 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def ConfirmingNewsletter(AllUser: bool) -> InlineKeyboardMarkup:
        if AllUser:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Yes",
                                             callback_data=admin_cb.new("ConfirmingAllYes", 0, 0, 0)
                                             ),
                        InlineKeyboardButton(text="No",
                                             callback_data=admin_cb.new("ConfirmingNo", 0, 0, 0)
                                             )
                    ],
                ]
            )
        else:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Да",
                                             callback_data=admin_cb.new("ConfirmingUserYes", 0, 0, 0)
                                             ),
                        InlineKeyboardButton(text="Нет",
                                             callback_data=admin_cb.new("ConfirmingNo", 0, 0, 0)
                                             )
                    ],
                ]
            )

    @staticmethod
    async def DeleteSchedule() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да",
                                         callback_data=admin_cb.new("DeleteSchedule", "DeleteScheduleYes", 0, 0)
                                         ),
                    InlineKeyboardButton(text="Нет",
                                         callback_data=admin_cb.new("DeleteSchedule", "DeleteScheduleNo", 0, 0)
                                         )
                ],
            ]
        )

    @staticmethod
    async def DeleteUser(db_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да",
                                         callback_data=admin_cb.new("UserProfile", "DeleteUserYes", db_id, 0)
                                         ),
                    InlineKeyboardButton(text="Нет",
                                         callback_data=admin_cb.new("UserProfile", "DeleteUserNo", 0, 0)
                                         )
                ],
            ]
        )

    @staticmethod
    async def approved_ikb(target: str, user_id: int, user_id_tg: int) -> InlineKeyboardMarkup:
        user = await CRUDUser.get(user_id=user_id_tg)
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Обработать",
                                         callback_data=admin_cb.new("Handle",  0, user_id, user_id_tg)

                                         )
                ],
                [
                    InlineKeyboardButton(text="Дать обратную связь",
                                         callback_data=admin_cb.new("Feedback", user_id, 0, user_id_tg),
                                         url=f"https://t.me/{user.nickname}"
                                         )
                ],
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=admin_cb.new(target, 0, 0, 0)
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
                                                         callback_data=admin_cb.new("UserProfile", "getProfile",
                                                                                    user.id,
                                                                                    user.user_id)
                                                         ),
                                    InlineKeyboardButton(text=f"❌",
                                                         callback_data=admin_cb.new("UserProfile", "getDeleteUser",
                                                                                    user.id,
                                                                                    user.user_id)
                                                         )
                                ]
                                for user in await CRUDUser.get_all()
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=admin_cb.new(target, 0, 0, 0))
                                ]
                            ]
        )

    @staticmethod
    async def order_show_get_user_ikb(target: str, checked: bool) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text=f"{user.lname} {user.fname}",
                                                         callback_data=admin_cb.new("UserProfile", "getProfile", user.id,
                                                                                    user.user_id))
                                ]
                                for user in await CRUDUser.get_all(get_add=1)
                            ] + [
                                [
                                    InlineKeyboardButton(text="← Назад",
                                                         callback_data=admin_cb.new(target, 0, 0, 0))
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

                elif data.get("target") == "AddTimetable":
                    await callback.message.edit_text(text="Пользователи которые скинули расписание",
                                                     reply_markup=await AdminPanel.order_show_get_user_ikb(
                                                         target="StartAdmin",
                                                         checked=True)
                                                     )

                elif data.get("target") == "UserProfile":
                    if data.get('action') == "getProfile":
                        user_id: int = int(data.get("id"))
                        user_id_tg: int = int(data.get("editId"))
                        weeks = await CRUDWeek.get(user_id=user_id)
                        if weeks:
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
                                                             reply_markup=await AdminPanel.approved_ikb(
                                                                 target="AddTimetable",
                                                                 user_id=user_id,
                                                                 user_id_tg=user_id_tg)
                                                             )
                        else:
                            await callback.message.edit_text(text="Пользователь не добавил расписание",
                                                             reply_markup=await AdminPanel.approved_ikb(
                                                                 target="AddTimetable",
                                                                 user_id=user_id,
                                                                 user_id_tg=user_id_tg))

                    elif data.get('action') == "getDeleteUser":
                        user_id: int = int(data.get("id"))
                        get_user = await CRUDUser.get(db_id=user_id)

                        await callback.message.edit_text(text="Вы действительно хотите удалить пользователя\n"
                                                              f"<i>{get_user.lname} {get_user.fname}</i> ?",
                                                         parse_mode="HTML",
                                                         reply_markup=await AdminPanel.DeleteUser(
                                                             db_id=user_id)
                                                         )

                    elif data.get('action') == "DeleteUserYes":
                        try:
                            user_id: int = int(data.get("id"))
                            await CRUDWeek.delete(user_id=user_id)
                            await CRUDUser.delete(user_id=user_id)

                            await callback.message.edit_text(text="Пользователь успешно удален!",
                                                             reply_markup=await AdminPanel.get_admin_panel())
                        except Exception as e:
                            await bot.send_message(text=f"Ошибка при удалении\n {e}",
                                                   chat_id=381252111)

                    elif data.get('action') == "DeleteUserNo":
                        await callback.message.edit_text(text="Пользователь не удален",
                                                         reply_markup=await AdminPanel.get_admin_panel())

                elif data.get('target') == "NewsletterUser":
                    await callback.message.edit_text(text="Введите текст!")
                    await AddMailingFSM.NewsletterUser.set()

                elif data.get('target') == "NewsletterAll":
                    await callback.message.edit_text(text="Введите текст!")
                    await AddMailingFSM.NewsletterAll.set()

                elif data.get('target') == "ConfirmingUserYes":
                    users = await CRUDUser.get_all(checked=True)

                    tasks = []
                    try:
                        for user in users:
                            tasks.append(bot.send_message(chat_id=user.user_id,
                                                          text=CONFIG.NewsletterUser))

                        await asyncio.gather(*tasks, return_exceptions=True)  # Отправка всем админам сразу

                        await callback.message.edit_text(text="Рассылка успешно отправлена")
                    except Exception as e:
                        await bot.send_message(text=f"Ошибка при отправке рассылки всем кто не добавил\n {e}",
                                               chat_id=381252111)

                elif data.get('target') == "ConfirmingAllYes":
                    users = await CRUDUser.get_all()

                    tasks = []
                    try:
                        for user in users:
                            tasks.append(bot.send_message(chat_id=user.user_id,
                                                          text=CONFIG.NewsletterUser))

                        await asyncio.gather(*tasks, return_exceptions=True)  # Отправка всем админам сразу

                        await callback.message.edit_text(text="Рассылка успешно отправлена")
                    except Exception as e:
                        await bot.send_message(text=f"Ошибка при отправке рассылки всем\n {e}",
                                               chat_id=381252111)

                elif data.get('target') == "ConfirmingNo":
                    await state.finish()
                    await callback.message.edit_text(text="Рассылка Отменена")

                elif data.get('target') == "DeleteSchedule":
                    if data.get('action') == "getSchedule":
                        await callback.message.edit_text(text="Вы уверены что желаете удалить расписание?",
                                                         reply_markup=await AdminPanel.DeleteSchedule())

                    elif data.get('action') == "DeleteScheduleYes":
                        get_users = await CRUDUser.get_all(get_add=1)
                        for user in get_users:
                            user.checked = True
                            await CRUDUser.update(user_id=user)

                        await CRUDWeek.delete()
                        await callback.message.edit_text(text="Расписание успешно Удалено",
                                                         reply_markup=await AdminPanel.get_admin_panel())

                    elif data.get('action') == "DeleteScheduleNo":
                        await callback.message.edit_text(text='Удаление отменено')

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
                if await state.get_state() == "AddMailingFSM:NewsletterUser":
                    try:
                        text = "‼️Напоминание‼️\n\n" \
                               f"{message.text}\n\n" \
                               "(Меню -> Войти ...)\n\n"

                        CONFIG.NewsletterUser = text
                        await state.finish()
                        await message.answer(text="Желаете отправить!\n\n"
                                                  f"{text}",
                                             reply_markup=await AdminPanel.ConfirmingNewsletter(AllUser=False))
                    except Exception as e:
                        print(e)
                        await state.finish()
                        await message.answer(text="Ошибка, Кто то удалился из бота"
                                                  "короче напиши Владиславу!")

                elif await state.get_state() == "AddMailingFSM:NewsletterAll":
                    try:
                        CONFIG.NewsletterUser = message.text
                        await state.finish()
                        await message.answer(text="Желаете отправить!\n\n"
                                                  f"{message.text}",
                                             reply_markup=await AdminPanel.ConfirmingNewsletter(AllUser=True))
                    except Exception as e:
                        print(e)
                        await state.finish()
                        await message.answer(text="Ошибка, Кто то удалился из бота"
                                                  "короче напиши Владиславу!")