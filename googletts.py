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

    print(f"Payload: {payload}")

    headers = {
        "X-Goog-Api-Key": google_api_key,
        "Content-Type": "application/json; charset=utf-8",
    }

    response = requests.post(
        "https://texttospeech.googleapis.com/v1/text:synthesize",
        headers=headers,
        data=json.dumps(payload),
    )

    try:
        base64_data = response.json()["audioContent"]
        return base64_data
    except:
        Exception(f"Error in request to Google TTS API - maybe not authenticated / api rate limited: {response.text}")

def write_base64_audio_to_file(base64_data, output_audio_path, chunk_size=1024):
    """
    Decode base64 audio data and write it to a file in chunks.

    :param base64_data: Base64 encoded audio data.
    :param output_audio_path: Path to save the decoded audio file.
    :param chunk_size: Size of chunks to write to file (in bytes).
    """
    audio_bytes = base64.b64decode(base64_data)

    with open(output_audio_path, "wb") as f:
        for i in range(0, len(audio_bytes), chunk_size):
            f.write(audio_bytes[i:i+chunk_size])
