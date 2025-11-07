from aiogram import Router
from . import help_user, start, users, taqdimotlar, subscription, sent_msg, quarter_settings
from filters.admins import IsAdmin
from aiogram.types import Message

router = Router()

async def admin_stop(message: Message):
    pass

router.include_router(start.router)
router.include_router(users.router)
router.include_router(taqdimotlar.router)
router.include_router(subscription.router)
router.include_router(quarter_settings.router)
router.include_router(help_user.router)
router.include_router(sent_msg.router)

mini_router = Router()
mini_router.message.register(admin_stop, IsAdmin())

router.include_router(mini_router)