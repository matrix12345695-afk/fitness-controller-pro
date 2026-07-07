from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):

    language = State()

    gender = State()

    birth_date = State()

    height = State()

    weight = State()

    completed = State()
