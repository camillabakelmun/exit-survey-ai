import os
from typing import List, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class CompetitorInsight(BaseModel):
    primary_competitor_name: str
    competitor_category: str
    is_ai_tool: bool
    # NEW: We force the AI to choose one of these exact three words
    sentiment: Literal['Positive', 'Negative', 'Neutral']


class CompetitorList(BaseModel):
    competitors: List[CompetitorInsight]


class APIResponse(BaseModel):
    original_comment: str
    ai_cleaned_data: CompetitorList


app = FastAPI()


@app.post("/extract-competitor", response_model=APIResponse)
async def extract_competitor(messy_comment: str):
    try:
        # NEW: We updated the instructions to ask for sentiment
        prompt = f"""
        Extract all competitors mentioned in the following customer exit survey comment.
        For each competitor, identify their category, if they are an AI tool, 
        and the user's sentiment towards that competitor (Positive, Negative, or Neutral).
        Comment: "{messy_comment}"
        """

        model = genai.GenerativeModel('gemini-2.5-flash')

        result = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=CompetitorList
            )
        )

        parsed_ai_data = CompetitorList.model_validate_json(result.text)

        return APIResponse(
            original_comment=messy_comment,
            ai_cleaned_data=parsed_ai_data
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list-models")
async def list_models():
    models = [m.name for m in genai.list_models()]
    return {"available_models": models}
