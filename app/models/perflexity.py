from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
    stream: bool = False
    raw: bool = False
    optimizer: str = None
    conversationally: bool = False