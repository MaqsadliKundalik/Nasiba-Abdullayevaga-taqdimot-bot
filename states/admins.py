from aiogram.fsm.state import StatesGroup, State

class NewPresentationState(StatesGroup):
    waiting_for_code = State()
    waiting_for_file = State()
    waiting_for_title = State()
    waiting_for_lang = State()

class FindTaqdimotState(StatesGroup):
    waiting_for_code = State()

class SentMsgState(StatesGroup):
    waiting_for_message = State()

class HelpAdminState(StatesGroup):
    waiting_for_msg = State()

class QuarterSettingsState(StatesGroup):
    waiting_for_quarter = State()