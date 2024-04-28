from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from handlers.blackbox import BLACKBOXAI

router = APIRouter()

ai_instance = BLACKBOXAI()

class Prompt(BaseModel):
    prompt: str

@router.post("/")
def generate_response(prompt: Prompt):
    try:
        response = ai_instance.chat(prompt.prompt, stream=False)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
