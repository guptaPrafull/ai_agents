from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth import get_current_user, create_access_token, authenticate_user
from app.models.email import Token, User, PromptInput, DraftResponse
from datetime import timedelta
from app.agents.personalized_email_drafter.routes import router as email_drafter_router
from app.agents.personalized_letter_drafter.routes import router as letter_router
from app.agents.reprompt_drafter.routes import router as rewriter_router
from app.agents.language_translation.routes import router as translation_router
from app.agents.ocr_text_extractor.routes import router as ocr_router
from app.agents.talk_to_your_knowledgebase.routes import router as document_insight_router
from fastapi.responses import JSONResponse
from fastapi import Request
import traceback

app = FastAPI(debug=True)

#app = FastAPI(title="AI Agents API")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Agent Suite is running!"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Register routes
app.include_router(email_drafter_router)
app.include_router(letter_router)
app.include_router(rewriter_router)
app.include_router(translation_router)
app.include_router(ocr_router)
app.include_router(document_insight_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
