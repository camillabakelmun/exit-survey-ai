import pandas as pd
import requests
import time

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
            response = requests.post(
                API_URL, params={"messy_comment": comment})

            if response.status_code == 200:
                raw_data = response.json()

                # FIX: Navigate into the new 'competitors' wrapper
                clean_json = raw_data.get(
                    'ai_cleaned_data', {}).get('competitors', [])

                if isinstance(clean_json, list) and len(clean_json) > 0:
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
                # This will print the exact error message if it crashes again!
                error_msg = response.json().get('detail', 'Unknown API Error')
                print(f"⚠️ Error on row {index+1}: {error_msg}")
                results.append({"competitor_names": "Error",
                               "categories": "Error", "any_ai_tools": None})

        except Exception as e:
            print(f"❌ Script Error on row {index+1}: {e}")
            results.append({"competitor_names": "Failed",
                           "categories": "Failed", "any_ai_tools": None})

        time.sleep(1)

    clean_df = pd.DataFrame(results)
    final_output = pd.concat([df, clean_df], axis=1)
    final_output.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Success! Processed {len(df)} rows.")
    print(f"📂 Open '{OUTPUT_FILE}' to see the results!")


if __name__ == "__main__":
    process_survey()
