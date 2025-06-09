from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

class PromptInput(BaseModel):
    user_input: str

class DraftResponse(BaseModel):
    draft: str
