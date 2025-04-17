import requests
import pandas as pd
import os

# Constants
AUDIOS_PATH = "Audios\\"
URL = "http://localhost:8000/voice/"
OUTPUT_FILE = "responses.xlsx"

responses = []

def test_audio_transcript():
    
    audio_files = [f for f in os.listdir(AUDIOS_PATH) if f.endswith(".wav")]

    for audio_file in audio_files:
        audio_path = os.path.join(AUDIOS_PATH, audio_file)

        with open(audio_path, "rb") as f:
            files = {"record": (audio_file, f)}
            try:
                response = requests.post(URL, files=files)
                response.raise_for_status()

                try:
                    result = response.json()
                except ValueError:
                    result = {"error": "Invalid JSON response"}

                # Add filename to result
                result["filename"] = audio_file
                responses.append(result)

                print(f"File {audio_file} processed successfully.")

            except requests.RequestException as e:
                print(f"Error processing file {audio_file}: {e}")
                responses.append({"filename": audio_file, "error": str(e)})

    # Convert list of dicts to DataFrame (flattening nested JSON if needed)
    df = pd.json_normalize(responses)

    # Save to Excel
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    df.to_excel(OUTPUT_FILE, index=True)
    print(f"Responses saved to {OUTPUT_FILE}")

# Run the function
if __name__ == "__main__":
    test_audio_transcript()
