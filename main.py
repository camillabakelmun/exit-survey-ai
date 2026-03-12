import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the secret API key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Start our FastAPI application
app = FastAPI()

# 3. Define our STRUCTURED OUTPUT (This is the MVP skill!)
# We are telling the AI: "You MUST reply with exactly these three fields."


class CompetitorInsight(BaseModel):
    primary_competitor_name: str
    competitor_category: str
    is_ai_tool: bool


# 4. Set up the Gemini Model (Flash is super fast for this)
model = genai.GenerativeModel('gemini-2.5-flash')

# 5. Create our API Endpoint


@app.post("/extract-competitor")
async def extract_competitor(messy_comment: str):

    # This is the prompt we send to the AI
    prompt = f"""
    You are an expert data analyst. Review this messy comment from an exit survey.
    Identify the main competitor or alternative resource the user is moving to.
    Standardize the spelling (e.g., 'chatgpt' -> 'ChatGPT', 'ixl' -> 'IXL').
    Categorize the competitor (e.g., 'EdTech Platform', 'AI Tool', 'Private Tutor', 'Other').
    
    Here is the messy comment: {messy_comment}
    """

    # We call Gemini and force it to use our CompetitorInsight structure
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=CompetitorInsight,
        ),
    )

    # Return the result!
    return {
        "original_comment": messy_comment,
        "ai_cleaned_data": response.text
    }


@app.get("/list-models")
async def list_models():
    # Ask Google for all available models
    available_models = [m.name for m in genai.list_models()]
    return {"models": available_models}
