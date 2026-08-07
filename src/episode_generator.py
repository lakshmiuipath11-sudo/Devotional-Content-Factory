import json

from cinematic_prompt_engine import write_prompt_files
from hf_image_engine import generate_scene_images
from youtube_metadata import write_youtube_files


def build_episode(
    base,
    number,
    story,
    weekday,
    date_label,
    settings,
):
    video_dir = base / f"Video-{number:02d}"
    video_dir.mkdir(parents=True, exist_ok=True)

    narration = "\n\n".join(
        [
            story["hook"],
            story["fact"],
            story["story"],
            "నీతి: " + story["moral"],
            story["cta"],
        ]
    )

    (video_dir / "Narration_Telugu.txt").write_text(
        narration,
        encoding="utf-8",
    )

    prompts = write_prompt_files(video_dir, story)

    images = generate_scene_images(
        video_dir,
        story,
        prompts,
        settings,
    )

    title, hashtags = write_youtube_files(video_dir, story)

    metadata = {
        "video_number": number,
        "story_id": story["id"],
        "title_telugu": title,
        "hashtags_english": hashtags,
        "weekday": weekday,
        "date": date_label,
        "deity": story["deity_name"],
        "deity_key": story["deity_key"],
        "language": "Telugu",
        "scene_count": 5,
        "image_engine": "huggingface",
        "hf_model": settings.get("hf_model"),
        "images": [item["file"] for item in images],
        "status": "generated",
    }

    (video_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (video_dir / "log.txt").write_text(
        f"Story: {story['id']}\n"
        f"Generated 5 Hugging Face images.\n"
        f"Title: {title}\n"
        f"Hashtags: {' '.join(hashtags)}\n",
        encoding="utf-8",
    )
