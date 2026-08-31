from aiogram import Router
from .start import router as start_router
from .profile import router as profile_router
from .group import router as group_router
from .callback import router as callback_router
from .admin import router as admin_router
from .subscription import router as subscription_router

router = Router()
router.include_router(start_router)
router.include_router(profile_router)
router.include_router(group_router)
router.include_router(callback_router)
router.include_router(admin_router)
router.include_router(subscription_router)