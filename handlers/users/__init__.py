from aiogram import Router
from . import start, subscription, taqdimotlar, profile

router = Router()
router.include_router(start.router)
router.include_router(subscription.router)
router.include_router(taqdimotlar.router)
router.include_router(profile.router)
