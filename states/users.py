from aiogram.fsm.state import StatesGroup, State    

class UserRegisterSState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_name = State()

class QuarterSubscriptionState(StatesGroup):
    waiting_for_payment = State()

class HelpState(StatesGroup):
    waiting_for_msg = State()