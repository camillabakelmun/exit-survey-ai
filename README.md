# AI-Powered Competitor Insight Extractor

## Project Overview
This is a proof-of-concept API designed to solve a real-world business problem: extracting structured insights from messy, unstructured user feedback. 

Using a dataset of "Exit Surveys," this tool identifies which competitors users are moving to, categorizes the competitor type, and determines if the competitor is an AI-based tool.

## The Challenge
The raw data from exit surveys is often "noisy"—it contains typos, inconsistent naming (e.g., "chat gpt" vs "ChatGPT"), and multiple mentions. To analyze this data at scale, it must be converted from raw text into a **Structured Format (JSON)**.

## Key Features & Tech Stack
- **FastAPI:** A high-performance Python web framework used to build the API endpoints.
- **Google Gemini 2.5 Flash:** Used for advanced natural language processing.
- **Structured Output (Pydantic):** I implemented strict data schemas to ensure the AI always returns predictable, machine-readable JSON.
- **Environment Management:** Secured API keys using `.env` files to follow industry best practices.

## My Process & Debugging
During the development of this project, I encountered a `404 NotFound` error when trying to access the standard Gemini 1.5 model. 

**How I solved it:**
1. I didn't just guess the fix; I built a **Model Discovery Endpoint** (`/list-models`) into the API.
2. By querying the Google API directly through my own code, I discovered that my account had access to the newer `gemini-2.5-flash` model.
3. I updated the configuration, resolved the error, and successfully implemented the structured output logic.

## How to Run
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your `GEMINI_API_KEY` to a `.env` file.
4. Run the server: `uvicorn main:app --reload`.