from aiogram.fsm.state import State, StatesGroup


class SurveyState(StatesGroup):
    """
    Universal survey FSM.

    The current question number and all answers are stored
    in FSMContext, therefore the number of questions can
    be changed without changing the FSM itself.
    """

    waiting_answer = State()

    completed = State()
