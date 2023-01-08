import json

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from crud import CRUDUser, CRUDPosition, CRUDWeek
from loader import bot
from schemas import UserSchema, WeekSchema, WeekInDBSchema
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
                    KeyboardButton(text='Добавить расписание',
                                   web_app=WebAppInfo(url="https://voluble-palmier-a2b577.netlify.app" + "/form")
                                   ),
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
    async def profile_user_ikb(user_id) -> InlineKeyboardMarkup:
        data_main_menu = {
            "Посмотреть расписание": {"target": "ProfileTimetable", "user_id": user_id},
            "◀️ Назад": {"target": "MainForms", "user_id": user_id}
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
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("main"):
                data = main_cb.parse(callback_data=callback.data)

                if data.get("target") == "Registration":
                    await callback.message.edit_text(text="Введите ФИО")
                    await UserStates.FIO.set()

                elif data.get("target") == "Profile":
                    try:
                        user_id = callback.from_user.id  # 964691423
                        if user_id == 964691423:
                            await callback.message.edit_text(text="Аннушка ты самая красивая и крутая\n"
                                                                  "Никогда не грусти!\n"
                                                                  "C наступающим новым годом 🌹 💐 🌷 🌺",
                                                             reply_markup=await MainForms.profile_user_ikb(
                                                                 user_id=callback.from_user.id)
                                                             )
                        else:
                            await callback.message.edit_text(text="Мой Профиль",
                                                             reply_markup=await MainForms.profile_user_ikb(
                                                                 user_id=callback.from_user.id)
                                                             )
                    except Exception as e:
                        print(e)

                elif data.get("target") == "ProfileTimetable":
                    try:
                        get_user = await CRUDUser.get(user_id=int(data.get("id")))
                        weeks_user = await CRUDWeek.get(user_id=get_user.id)
                        if weeks_user:
                            text = "Мои пожелания\n\n" \
                                   f"Понедельник - {weeks_user.Monday}\n" \
                                   f"Вторник - {weeks_user.Tuesday}\n" \
                                   f"Среда - {weeks_user.Wednesday}\n" \
                                   f"Четверг - {weeks_user.Thursday}\n" \
                                   f"Пятница - {weeks_user.Friday}\n" \
                                   f"Суббота - {weeks_user.Saturday}\n" \
                                   f"Воскресенье - {weeks_user.Sunday}\n\n" \
                                   f"Пожелание - {weeks_user.description}"
                            await callback.message.edit_text(text=text,
                                                             reply_markup=await MainForms.back_ikb("MainForms"),
                                                             parse_mode="HTML")
                        else:
                            await callback.message.edit_text(text="‼️Ты еще не добавил расписание‼️",
                                                             reply_markup=await MainForms.back_ikb(target="MainForms"))
                    except Exception as e:
                        print(e)

                elif data.get("target") == "MainForms":
                    await callback.message.edit_text(text="Главное меню",
                                                     reply_markup=await MainForms.main_menu_ikb(
                                                         user_id=callback.from_user.id)
                                                     )

                elif data.get("target") == "Timetable":
                    get_user = await CRUDUser.get(user_id=int(data.get("id")))
                    get_position = await CRUDPosition.get(position_id=get_user.positions_id)

                    await callback.message.delete()
                    await callback.message.answer(text=f"{get_user.lname} {get_user.fname} {get_user.mname}\n",
                                                  reply_markup=await MainForms.open_site_kb()
                                                  )
                    await UserStates.Back.set()

                elif data.get("target") == "Approved":
                    data_timetable = await state.get_data()
                    get_user = await CRUDUser.get(user_id=callback.from_user.id)
                    user_week = await CRUDWeek.get(user_id=get_user.id)
                    if user_week:
                        try:
                            user_week.Monday = data_timetable["Monday"]
                            user_week.Tuesday = data_timetable["Tuesday"]
                            user_week.Wednesday = data_timetable["Wednesday"]
                            user_week.Thursday = data_timetable["Thursday"]
                            user_week.Friday = data_timetable["Friday"]
                            user_week.Saturday = data_timetable["Saturday"]
                            user_week.Sunday = data_timetable["Sunday"]
                            user_week.description = data_timetable["Description"]
                            user_week.handle = True
                            get_user.checked = True

                            await CRUDUser.update(user_id=get_user)
                            await CRUDWeek.update(user_week=user_week)
                            await callback.message.edit_text(text="Вы успешно отправили расписание\n"
                                                                  "Главное меню",
                                                             reply_markup=await MainForms.main_menu_ikb(
                                                                 user_id=callback.from_user.id)
                                                             )
                            await bot.send_message(chat_id=381252111,
                                                   text=f"{get_user.lname} {get_user.fname} Обновил дасписание",
                                                   parse_mode="HTML",
                                                   )
                        except Exception as e:
                            print(e)
                            await callback.message.edit_text(text="Возникла Ошибка\n"
                                                                  "Попробуй добавить еще раз расписание или "
                                                                  "обратись к менеджеру")
                            await bot.send_message(chat_id=381252111,
                                                   text=f"{get_user.lname} {get_user.fname} добавил дасписание",
                                                   parse_mode="HTML",
                                                   )

                        await state.finish()
                    else:
                        await CRUDWeek.add(week=WeekSchema(**data_timetable))
                        await callback.message.edit_text(text="Вы успешно отправили расписание\n"
                                                              "Главное меню",
                                                         reply_markup=await MainForms.main_menu_ikb(
                                                             user_id=callback.from_user.id)
                                                         )
                    await state.finish()

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
                    nickname = "None"
                    if message.from_user.username:
                        nickname = message.from_user.username

                    if len(fio) < 3:
                        await message.answer(text="Введите полное ФИО!")
                        await UserStates.FIO.set()
                    else:
                        await state.update_data(user_id=user_id)
                        await state.update_data(lname=fio[0].title())
                        await state.update_data(fname=fio[1].title())
                        await state.update_data(mname=fio[2].title())
                        await state.update_data(checked=False)
                        await state.update_data(nickname=nickname)

                        data = await state.get_data()

                        if await CRUDUser.add(user=UserSchema(**data)):
                            await message.answer(text=f"{fio[0].title()} {fio[1].title()} {fio[2].title()}\n"
                                                      "Вы успешно зарег. в системе\n\n"
                                                      "Главное меню",
                                                 reply_markup=await MainForms.main_menu_ikb(user_id=user_id))
                            await state.finish()

                elif await state.get_state() == "UserStates:Back":
                    try:
                        if message.content_type == "web_app_data":
                            webAppMes = message.web_app_data.data
                            json_string = json.loads(webAppMes)

                            text = f"Понедельник - <b>{json_string['Monday']}</b>\n" \
                                   f"Вторник - <b>{json_string['Tuesday']}</b>\n" \
                                   f"Среда - <b>{json_string['Wednesday']}</b>\n" \
                                   f"Четверг - <b>{json_string['Thursday']}</b>\n" \
                                   f"Пятница - <b>{json_string['Friday']}</b>\n" \
                                   f"Суббота - <b>{json_string['Saturday']}</b>\n" \
                                   f"Воскресенье - <b>{json_string['Sunday']}</b>\n" \
                                   f"Пожелание - <b>{json_string['Description']}</b>"
                            user = await CRUDUser.get(user_id=message.from_user.id)

                            await state.update_data(user_id=user.id)
                            await state.update_data(Monday=json_string['Monday'])
                            await state.update_data(Tuesday=json_string['Tuesday'])
                            await state.update_data(Wednesday=json_string['Wednesday'])
                            await state.update_data(Thursday=json_string['Thursday'])
                            await state.update_data(Friday=json_string['Friday'])
                            await state.update_data(Saturday=json_string['Saturday'])
                            await state.update_data(Sunday=json_string['Sunday'])
                            await state.update_data(Description=json_string['Description'])

                            await bot.send_message(text=f"‼️Нажми еще раз 'Отправить'\n"
                                                        f"что бы твои пожеления увидел менеджер‼️\n\n"
                                                        f"Ваши пожелания:\n{text}",
                                                   chat_id=message.chat.id,
                                                   reply_markup=await MainForms.approved_ikb(),
                                                   parse_mode="HTML")
                    except Exception as e:
                        await message.answer(text=f"Ошибка расписание не добавлено\n\n"
                                                  f"Обратись к разработчику Владислав и покажи эту ошибку\n\n"
                                                  f"{e}")
                    if message.text == "Назад":
                        await message.answer(text="Главное меню",
                                             reply_markup=await MainForms.main_menu_ikb(
                                                 user_id=message.from_user.id))
                        await state.finish()
