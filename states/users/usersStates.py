from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):

    Name = State()
    Surname = State()
    Patronymic = State()
