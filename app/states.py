from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    language = State()
    gender = State()
    seeking = State()
    region = State()
    township = State()
    age = State()
    bio = State()
    photo = State()


class PremiumState(StatesGroup):
    awaiting_screenshot = State()
