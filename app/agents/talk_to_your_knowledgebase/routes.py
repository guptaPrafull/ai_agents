from fastapi import APIRouter, UploadFile, File, Form , Depends
from typing import Optional
from app.auth.auth import get_current_user
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
from .logic import (
    save_upload_file,
    extract_text_from_file,
    summarize_document,
    generate_faq_by_topic,
    chat_with_document
)
import os
import uuid

router = APIRouter(prefix="/document-insight", tags=["Talk to your Knowledgebase"])


@router.post("/summarize")
async def summarize(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    print("Incoming file:", file.filename)
    try:
        file_path = await save_upload_file(file)
        print(f"Uploaded file path: {file_path}")
        print("Detected extension:", os.path.splitext(file_path)[-1])
        text = extract_text_from_file(file_path)
        summary = summarize_document(text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}


@router.post("/faq")
async def generate_faq(
        topic: str = Form(...),
        file: UploadFile = File(...),
        current_user=Depends(get_current_user)
):

    try:
        file_path = await save_upload_file(file)
        print(f"Uploaded file path: {file_path}")
        print("Detected extension:", os.path.splitext(file_path)[-1])
        text = extract_text_from_file(file_path)
        faq = generate_faq_by_topic(topic, text)
        return {"faq": faq}
    except Exception as e:
        return {"error": str(e)}



class ChatRequest(BaseModel):
    history: List[Dict[str, str]]
    message: str
    document: str


@router.post("/chat")
async def chat_endpoint(request: ChatRequest, current_user=Depends(get_current_user)):
    try:
        reply, updated_history = chat_with_document(
            document_text=request.document,
            user_input=request.message,
            history=request.history
        )
        return {
            "reply": reply,
            "updated_history": updated_history[2:]  # Remove system & document messages
        }
    except Exception as e:
        return {"error": str(e)}
