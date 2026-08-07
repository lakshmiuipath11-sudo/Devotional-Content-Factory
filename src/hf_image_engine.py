from __future__ import annotations

import json
import os
import time
from pathlib import Path

from huggingface_hub import InferenceClient


def get_client() -> InferenceClient:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "HF_TOKEN is missing. Add it in GitHub: "
            "Settings > Secrets and variables > Actions."
        )
    return InferenceClient(api_key=token)


def generate_scene_images(
    video_dir: Path,
    story: dict,
    prompts: list[dict],
    settings: dict,
) -> list[dict]:
    client = get_client()
    model = settings.get(
        "hf_model",
        "black-forest-labs/FLUX.1-schnell",
    )
    max_retries = int(settings.get("max_image_retries", 3))
    delay = int(settings.get("retry_delay_seconds", 8))

    manifest = []

    for item in prompts:
        scene = int(item["scene"])
        output_path = video_dir / f"Scene_{scene:02d}.png"
        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                print(
                    f"[{video_dir.name}] Generating scene {scene}/5 "
                    f"(attempt {attempt}/{max_retries})"
                )

                image = client.text_to_image(
                    prompt=item["prompt"],
                    model=model,
                )
                image.save(output_path)

                manifest.append(
                    {
                        "scene": scene,
                        "file": output_path.name,
                        "model": model,
                        "status": "generated",
                    }
                )
                last_error = None
                break

            except Exception as exc:
                last_error = exc
                print(f"Scene {scene} failed: {exc}")

                if attempt < max_retries:
                    wait = delay * attempt
                    print(f"Retrying in {wait} seconds...")
                    time.sleep(wait)

        if last_error is not None:
            raise RuntimeError(
                f"Scene {scene} failed after {max_retries} attempts: "
                f"{last_error}"
            )

    (video_dir / "image_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return manifest
