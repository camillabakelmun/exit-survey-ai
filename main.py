import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, RootModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. The Single Competitor Schema


class CompetitorInsight(BaseModel):
    primary_competitor_name: str
    competitor_category: str
    is_ai_tool: bool

# 2. The LLM Output Schema (A list of competitors)


class CompetitorList(RootModel):
    root: List[CompetitorInsight]

# 3. NEW: The Final API Response Schema


class APIResponse(BaseModel):
    original_comment: str
    ai_cleaned_data: CompetitorList  # Embeds the structured list directly!


app = FastAPI()

# NEW: We tell FastAPI exactly what shape to return using response_model


@app.post("/extract-competitor", response_model=APIResponse)
async def extract_competitor(messy_comment: str):
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

    # NEW: Validate the AI's text and convert it into a true Python object
    parsed_ai_data = CompetitorList.model_validate_json(result.text)

    # Return the data matching the APIResponse schema
    return APIResponse(
        original_comment=messy_comment,
        ai_cleaned_data=parsed_ai_data
    )


@app.get("/list-models")
async def list_models():
    models = [m.name for m in genai.list_models()]
    return {"available_models": models}
