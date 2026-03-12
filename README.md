# AI Powered Competitor Insight Extractor

## Project Overview
This API is designed to solve a real world business problem: extracting structured insights from messy and unstructured user feedback. Using a dataset of exit surveys, this tool identifies which competitors users are moving to, categorises the competitor type and determines if the competitor is an AI based tool.

## The Challenge
The raw data from exit surveys is often noisy as it contains typos, inconsistent naming conventions and multiple mentions within a single sentence. To analyse this data at scale, it must be converted from raw text into a structured JSON format.

## Key Features and Tech Stack
* **FastAPI:** A high performance Python web framework used to build the API endpoints.
* **Google Gemini 2.5 Flash:** Used for advanced natural language processing.
* **Structured Output (Pydantic):** I implemented strict data schemas to ensure the AI always returns predictable and machine readable JSON.
* **Environment Management:** Secured API keys using .env files to follow industry best practices.

## Development Process and Problem Solving
During the development of this project, I encountered a 404 Not Found error when trying to access the standard Gemini 1.5 model. Rather than guessing the fix, I built a model discovery endpoint into the API. By querying the Google API directly through my own code, I discovered that my account had access to the newer Gemini 2.5 Flash model. I updated the configuration, resolved the error and successfully implemented the structured output logic.

## Enterprise Upgrades and Continuous Integration
Following the initial deployment, I implemented several senior level engineering practices to make the API robust and production ready.

* **Strict Data Validation:** Upgraded the application to use Pydantic model validation to ensure the LLM output strictly adheres to the expected schema before it ever reaches the client.
* **Array Based Extraction:** Implemented a RootModel to allow the AI to extract an unlimited number of competitors from a single comment rather than being restricted to one entity.
* **Swagger API Documentation:** Added explicit response models to the FastAPI endpoints so the interactive documentation accurately reflects the nested JSON structure.
* **Professional Git Workflow:** Transitioned from direct commits to a formal feature branching and Pull Request methodology.
* **Continuous Deployment:** Connected the GitHub repository to Render to automate the deployment process every time new code is merged into the main branch.

## How to Run

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
