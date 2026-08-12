import os
import requests

api_key = os.environ["ELEVENLABS_API_KEY"]
voice_id = os.environ["ELEVENLABS_VOICE_ID"]

text = """
మీకు తెలుసా?

గణేశుడు తన జ్ఞానంతో ప్రపంచ యాత్రలో విజయం సాధించాడు.

తల్లిదండ్రులే తన ప్రపంచమని భావించి వారిని ప్రదక్షిణ చేసి
తన భక్తి మరియు జ్ఞానాన్ని చాటాడు.

ఇలాంటి మరిన్ని భక్తి విశేషాల కోసం
మా ఛానల్‌ను సబ్‌స్క్రైబ్ చేయండి.
"""

url = (
    f"https://api.elevenlabs.io/v1/text-to-speech/"
    f"{voice_id}?output_format=mp3_44100_128"
)

headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "text": text,
    "model_id": "eleven_v3"
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=120
)

if response.status_code != 200:
    raise RuntimeError(
        f"ElevenLabs error {response.status_code}: {response.text}"
    )

with open("Narration_Test.mp3", "wb") as f:
    f.write(response.content)

print("SUCCESS: Narration_Test.mp3 generated")
