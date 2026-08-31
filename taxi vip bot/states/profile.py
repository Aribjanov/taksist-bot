from aiogram.fsm.state import State, StatesGroup

class ProfileState(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_phone = State()
    waiting_for_car_model = State()
    waiting_for_car_number = State()