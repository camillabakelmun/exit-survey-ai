import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, RootModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the structure for a SINGLE competitor


class CompetitorInsight(BaseModel):
    primary_competitor_name: str
    competitor_category: str
    is_ai_tool: bool

# Define a List of competitors (The "RootModel" fix)
# This tells the AI: "You can return one, zero, or ten competitors in a list"


class CompetitorList(RootModel):
    root: List[CompetitorInsight]


app = FastAPI()


@app.post("/extract-competitor")
async def extract_competitor(messy_comment: str):
    # Updated Prompt to handle multiple mentions
    prompt = f"""
    Extract all competitors mentioned in the following customer exit survey comment.
    For each competitor, identify their category and if they are an AI tool.
    Comment: "{messy_comment}"
    """

    model = genai.GenerativeModel('gemini-2.5-flash')

    # We use CompetitorList here so it returns a list of results
    result = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=CompetitorList
        )
    )

    return {"original_comment": messy_comment, "ai_cleaned_data": result.text}


@app.get("/list-models")
async def list_models():
    models = [m.name for m in genai.list_models()]
    return {"available_models": models}
