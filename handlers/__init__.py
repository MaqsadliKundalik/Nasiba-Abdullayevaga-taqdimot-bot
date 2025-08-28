from aiogram import Router
from . import admin, users

router = Router()
router.include_router(admin.router)
router.include_router(users.router)