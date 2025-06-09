from fastapi import APIRouter, UploadFile, File,Depends
from app.agents.ocr_text_extractor.logic import extract_text_from_image
import tempfile
import shutil
from app.auth.auth import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter( prefix="/ocr", tags=["OCR Text Extractor"])

@router.post("/ocr-extract")
async def ocr_extract(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        result = extract_text_from_image(tmp_path)
        return {"extracted_text": result}
    except Exception as e:
        return {"error": str(e)}
