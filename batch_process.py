import pandas as pd
import requests
import time

API_URL = "https://exit-survey-ai.onrender.com/extract-competitor"
INPUT_FILE = "fake_exit_survey.csv"
OUTPUT_FILE = "cleaned_exit_survey.csv"


def process_survey():
    print(f"Starting batch process for {INPUT_FILE}...")

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_FILE}")
        return

    results = []

    for index, row in df.iterrows():
        comment = str(row['Comment']) if pd.notna(row['Comment']) else ""
        print(f"[{index+1}/{len(df)}] Processing: {comment[:30]}...")

        try:
            response = requests.post(
                API_URL, params={"messy_comment": comment})

            if response.status_code == 200:
                raw_data = response.json()
                clean_json = raw_data.get(
                    'ai_cleaned_data', {}).get('competitors', [])

                if isinstance(clean_json, list) and len(clean_json) > 0:
                    combined_result = {
                        "Competitor Name": ", ".join([c.get('primary_competitor_name', '') for c in clean_json]),
                        "Category": ", ".join([c.get('competitor_category', '') for c in clean_json]),
                        "Is AI": ", ".join(["Yes" if c.get('is_ai_tool') else "No" for c in clean_json]),
                        "Sentiment": ", ".join([c.get('sentiment', 'Neutral') for c in clean_json])
                    }
                    results.append(combined_result)
                else:
                    results.append({"Competitor Name": "None Found",
                                   "Category": "N/A", "Is AI": "No", "Sentiment": "Neutral"})
            else:
                results.append({"Competitor Name": "Error", "Category": "Error",
                               "Is AI": "Error", "Sentiment": "Error"})

        except Exception as e:
            print(f"Error on row {index+1}: {e}")
            results.append({"Competitor Name": "Failed", "Category": "Failed",
                           "Is AI": "Failed", "Sentiment": "Failed"})

        # 5 second pause to stay under the Gemini 15 requests per minute limit
        time.sleep(5)

    clean_df = pd.DataFrame(results)
    final_output = pd.concat([df, clean_df], axis=1)
    final_output.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSuccess! Processed {len(df)} rows.")
    print(f"Open '{OUTPUT_FILE}' to see your clean data!")


if __name__ == "__main__":
    process_survey()
