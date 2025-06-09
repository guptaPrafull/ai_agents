from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .logic import translation_pipeline
from app.auth.auth import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/translation", tags=["Language Translation Agent"])

class TranslationRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str

@router.post("/translate")
async def translate_text(req: TranslationRequest , current_user=Depends(get_current_user)):
    try:
        result = translation_pipeline(req.text, req.src_lang, req.tgt_lang)
        return {"translated_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

