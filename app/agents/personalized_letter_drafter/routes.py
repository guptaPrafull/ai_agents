from fastapi import APIRouter, Depends
from app.models.email import PromptInput, DraftResponse
from app.auth.auth import get_current_user
from app.agents.personalized_letter_drafter.logic import generate_letter

router = APIRouter(prefix="/letter-drafter", tags=["Personalized Letter Drafter"])

@router.post("/generate", response_model=DraftResponse)
def draft_letter(prompt: PromptInput, user=Depends(get_current_user)):
    letter = generate_letter(prompt.user_input)
    return {"draft": letter}
