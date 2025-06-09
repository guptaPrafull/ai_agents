from fastapi import APIRouter, Depends
from app.auth.auth import get_current_user
from app.agents.reprompt_drafter.logic import reprompt_input
from app.models.reprompt import PromptRewriterInput, PromptRewriterOutput
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/prompt-rewriter", tags=["Prompt Rewriter"])



@router.post("/reprompt", response_model=PromptRewriterOutput)
def rewrite_prompt(data: PromptRewriterInput, current_user=Depends(get_current_user)):
    try:
        print(data.dict())
        rewritten = reprompt_input(data.raw_prompt )

        return {"rewritten_prompt": rewritten}
    except ValueError as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
