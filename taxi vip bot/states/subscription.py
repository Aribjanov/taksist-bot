from aiogram.fsm.state import State, StatesGroup

class SubscriptionState(StatesGroup):
    waiting_for_receipt = State()

class AdminState(StatesGroup):
    waiting_for_user_id = State()