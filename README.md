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

   
## Scaling to Entire Datasets
This project is built to handle bulk data processing out of the box. The batch process script can easily scale to analyse thousands of rows of employee exit survey data. 

To run this tool on your own full dataset you simply need to:
1. Place your large CSV file into the main project folder.
2. Ensure your spreadsheet contains a column named exactly 'Comment'.
3. Open `batch_process.py` and update the `INPUT_FILE` variable to match your new filename.
4. Run the script in your terminal and watch the AI seamlessly categorise your entire dataset.

## Handling API Rate Limits
When processing large datasets programmatically it is crucial to handle API rate limits. The free tier of the Google Gemini API restricts usage to 15 requests per minute. If you send data too quickly the server will reject the request and return a 429 Too Many Requests error. 

To solve this I implemented a five second delay (`time.sleep(5)`) inside the batch processing loop. This simple throttle keeps the extraction process safely under the speed limit and ensures every single row is processed reliably without dropping any data.