import json
from youtube_metadata import write_youtube_files
from cinematic_prompt_engine import write_prompt_files

def build_episode(base, number, story, weekday, date_label):
    video_dir = base / f"Video-{number:02d}"
    video_dir.mkdir(parents=True, exist_ok=True)

    narration = "\n\n".join([
        story["hook"],
        story["fact"],
        story["story"],
        "నీతి: " + story["moral"],
        story["cta"],
    ])
    (video_dir / "Narration_Telugu.txt").write_text(narration, encoding="utf-8")

    prompts = write_prompt_files(video_dir, story)
    title, hashtags = write_youtube_files(video_dir, story)

    scene_plan = [
        {
            "scene": item["scene"],
            "role": item["role"],
            "prompt_file": f"image_prompt_{item['scene']:02d}.txt",
        }
        for item in prompts
    ]
    (video_dir / "scene_plan.json").write_text(
        json.dumps(scene_plan, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

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
        "prompt_engine": "V1.4 cinematic story-aligned",
        "status": "planned",
    }

    (video_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (video_dir / "log.txt").write_text(
        f"Story: {story['id']}\n"
        f"Title: {title}\n"
        f"5 cinematic prompts generated.\n",
        encoding="utf-8",
    )
