from fastapi import APIRouter, Query
from g4f.client import Client

router = APIRouter()
client = Client()

@router.post("/")
async def complete(prompt: str = Query(..., title="Prompt")):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content":prompt}]
    )
    return {"response": response.choices[0].message.content}
