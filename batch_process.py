import pandas as pd
import requests
import time

# 1. Configuration - Pointing to your live Render API
API_URL = "https://exit-survey-ai.onrender.com/extract-competitor"
INPUT_FILE = "fake_exit_survey.csv"
OUTPUT_FILE = "cleaned_exit_survey.csv"


def process_survey():
    print(f"🚀 Starting batch process for {INPUT_FILE}...")

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {INPUT_FILE}")
        return

    results = []

    for index, row in df.iterrows():
        comment = str(row['Comment']) if pd.notna(row['Comment']) else ""
        print(f"[{index+1}/{len(df)}] Processing: {comment[:30]}...")

        try:
            # Call your LIVE API
            response = requests.post(
                API_URL, params={"messy_comment": comment})

            if response.status_code == 200:
                raw_data = response.json()
                # The API now returns true JSON, so we just access the list directly
                clean_json = raw_data.get('ai_cleaned_data', [])

                if isinstance(clean_json, list) and len(clean_json) > 0:
                    # We combine multiple competitors into single strings so they fit in one CSV row
                    combined_result = {
                        "competitor_names": ", ".join([c.get('primary_competitor_name', '') for c in clean_json]),
                        "categories": ", ".join([c.get('competitor_category', '') for c in clean_json]),
                        "any_ai_tools": any([c.get('is_ai_tool', False) for c in clean_json])
                    }
                    results.append(combined_result)
                else:
                    results.append(
                        {"competitor_names": "None Found", "categories": "N/A", "any_ai_tools": False})
            else:
                print(
                    f"⚠️ API Error on row {index+1}: Status {response.status_code}")
                results.append({"competitor_names": "Error",
                               "categories": "Error", "any_ai_tools": None})

        except Exception as e:
            print(f"❌ Error on row {index+1}: {e}")
            results.append({"competitor_names": "Failed",
                           "categories": "Failed", "any_ai_tools": None})

        # 1 second pause to keep the free-tier server happy
        time.sleep(1)

    # Create the new columns
    clean_df = pd.DataFrame(results)

    # Merge with original data
    final_output = pd.concat([df, clean_df], axis=1)

    # Save the new file
    final_output.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Success! Processed {len(df)} rows.")
    print(f"📂 Open '{OUTPUT_FILE}' to see the results!")


if __name__ == "__main__":
    process_survey()
