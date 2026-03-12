import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. The Single Competitor Schema


class CompetitorInsight(BaseModel):
    primary_competitor_name: str
    competitor_category: str
    is_ai_tool: bool

# 2. FIX: Wrap the list inside a standard BaseModel so Gemini doesn't crash


class CompetitorList(BaseModel):
    competitors: List[CompetitorInsight]

# 3. The Final API Response Schema


class APIResponse(BaseModel):
    original_comment: str
    ai_cleaned_data: CompetitorList


app = FastAPI()


@app.post("/extract-competitor", response_model=APIResponse)
async def extract_competitor(messy_comment: str):
    try:
        prompt = f"""
        Extract all competitors mentioned in the following customer exit survey comment.
        For each competitor, identify their category and if they are an AI tool.
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

        # Validate the AI's output
        parsed_ai_data = CompetitorList.model_validate_json(result.text)

        return APIResponse(
            original_comment=messy_comment,
            ai_cleaned_data=parsed_ai_data
        )

    except Exception as e:
        # If anything breaks, show the exact error in the API response!
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list-models")
async def list_models():
    models = [m.name for m in genai.list_models()]
    return {"available_models": models}
