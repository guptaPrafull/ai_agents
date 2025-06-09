from pydantic import BaseModel
from typing import Optional

class PromptRewriterInput(BaseModel):
    raw_prompt: str


class PromptRewriterOutput(BaseModel):
    rewritten_prompt: str
