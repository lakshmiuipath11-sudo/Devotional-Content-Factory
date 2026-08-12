import os
from pathlib import Path

import requests


class ElevenLabsTTSError(RuntimeError):
    pass


def generate_telugu_narration(
    text,
    output_path,
    api_key=None,
    voice_id=None,
    model_id="eleven_v3",
    timeout=120,
):
    api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")

    if not api_key:
        raise ElevenLabsTTSError(
            "ELEVENLABS_API_KEY is missing."
        )

    if not voice_id:
        raise ElevenLabsTTSError(
            "ELEVENLABS_VOICE_ID is missing."
        )

    if not text or not text.strip():
        raise ElevenLabsTTSError(
            "Narration text is empty."
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/"
        f"{voice_id}?output_format=mp3_44100_128"
    )

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": text.strip(),
        "model_id": model_id,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:
        try:
            detail = response.json()
        except Exception:
            detail = response.text

        raise ElevenLabsTTSError(
            f"ElevenLabs error "
            f"{response.status_code}: {detail}"
        )

    output_path.write_bytes(
        response.content
    )

    return output_path


def narration_file_to_mp3(
    narration_txt,
    output_mp3=None,
):
    narration_txt = Path(
        narration_txt
    )

    if not narration_txt.exists():
        raise FileNotFoundError(
            f"Narration file not found: "
            f"{narration_txt}"
        )

    if output_mp3 is None:
        output_mp3 = (
            narration_txt
            .with_name("Narration.mp3")
        )

    text = narration_txt.read_text(
        encoding="utf-8"
    )

    return generate_telugu_narration(
        text,
        output_mp3
    )
