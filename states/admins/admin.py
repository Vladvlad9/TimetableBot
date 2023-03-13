from aiogram.dispatcher.filters.state import StatesGroup, State


class AddMailingFSM(StatesGroup):
    Back = State()
    NewsletterUser = State()
