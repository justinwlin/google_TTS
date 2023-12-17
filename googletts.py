import requests
import json
import base64
import os

# Generate a Google API key here: https://console.cloud.google.com/apis/credentials
# Make a project if you don't have one already.
def generate_audio_using_google_tts(
    text_to_speak,
    google_api_key,
    speed=1.2,
    voice="en-US-Neural2-J",
    pitch=0,
):
    payload = {
        "input": {"text": text_to_speak},
        "voice": {"languageCode": "en-US", "name": voice},
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speed,
            "pitch": pitch,
        },
    }

    headers = {
        "X-Goog-Api-Key": google_api_key,
        "Content-Type": "application/json; charset=utf-8",
    }

    response = requests.post(
        "https://texttospeech.googleapis.com/v1/text:synthesize",
        headers=headers,
        data=json.dumps(payload),
    )

    base64_data = response.json()["audioContent"]
    return base64_data

def write_base64_audio_to_file(base64_data, output_audio_path):
    audio_bytes = base64.b64decode(base64_data)
    with open(output_audio_path, "wb") as f:
        f.write(audio_bytes)
