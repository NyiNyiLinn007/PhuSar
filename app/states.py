from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    language = State()
    full_name = State()
    gender = State()
    seeking = State()
    region = State()
    ask_location = State()
    township = State()
    age = State()
    bio = State()
    photo = State()


class PremiumState(StatesGroup):
    choosing_provider = State()
    awaiting_screenshot = State()
