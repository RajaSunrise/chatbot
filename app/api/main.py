from fastapi import APIRouter

from api.router import users
from api.router import blackbox
from api.router import chatgpt


router = APIRouter()

router.include_router(users.router, tags=["Users"], prefix="/users")
router.include_router(blackbox.router, tags=["Blackbox"], prefix="/blackbox")
router.include_router(chatgpt.router, tags=["ChatGPT"], prefix="/chatgpt")