from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()


router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="views")

@router.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/chatbot", response_class=HTMLResponse)
def chatbot(request: Request):
    return templates.TemplateResponse("chatbot/chatbot.html", {"request": request})