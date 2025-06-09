from sys import prefix

from fastapi import APIRouter, Depends
from app.models.email import PromptInput, DraftResponse, User
from .logic import generate_email_
from app.auth.auth import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/email-drafter", tags=["Personalized Email Drafter"])

@router.post("/generate-email/", response_model=DraftResponse)
def generate_email(prompt: PromptInput, current_user: User = Depends(get_current_user)):
    draft = generate_email_(prompt.user_input)
    if draft.startswith("Error:"):
        return JSONResponse(status_code=500, content={"detail": draft})
    return {"draft": draft}

