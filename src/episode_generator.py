import json

from youtube_metadata import write_youtube_files
from cinematic_prompt_engine import write_prompt_files
from hf_image_engine import generate_scene_images


def build_episode(
    base,
    number,
    story,
    weekday,
    date_label,
    settings,
    skip_images=False,
):
    video_dir = base / f"Video-{number:02d}"

    video_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"[{video_dir.name}] "
        f"Creating episode package"
    )

    # --------------------------------------------------
    # 1. TELUGU NARRATION TEXT
    # --------------------------------------------------

    narration = "\n\n".join(
        [
            story["hook"],
            story["fact"],
            story["story"],
            "నీతి: " + story["moral"],
            story["cta"],
        ]
    )

    narration_file = (
        video_dir
        / "Narration_Telugu.txt"
    )

    narration_file.write_text(
        narration,
        encoding="utf-8",
    )

    print(
        f"[{video_dir.name}] "
        "Narration_Telugu.txt created"
    )

    # --------------------------------------------------
    # 2. CINEMATIC PROMPTS
    # --------------------------------------------------

    prompts = write_prompt_files(
        video_dir,
        story,
    )

    print(
        f"[{video_dir.name}] "
        f"{len(prompts)} cinematic prompts created"
    )

    # --------------------------------------------------
    # 3. IMAGE GENERATION
    # --------------------------------------------------

    images = []

    if skip_images:
        print(
            f"[{video_dir.name}] "
            "Hugging Face image generation SKIPPED"
        )

    else:
        print(
            f"[{video_dir.name}] "
            "Generating Hugging Face images..."
        )

        images = generate_scene_images(
            video_dir,
            story,
            prompts,
            settings,
        )

        print(
            f"[{video_dir.name}] "
            f"{len(images)} image(s) generated"
        )

    # --------------------------------------------------
    # 4. YOUTUBE TITLE + HASHTAGS
    # --------------------------------------------------

    title, hashtags = write_youtube_files(
        video_dir,
        story,
    )

    print(
        f"[{video_dir.name}] "
        "YouTube metadata created"
    )

    # --------------------------------------------------
    # 5. SCENE PLAN
    # --------------------------------------------------

    scene_plan = []

    for prompt_item in prompts:
        scene_number = prompt_item["scene"]

        scene_plan.append(
            {
                "scene": scene_number,
                "role": prompt_item.get(
                    "role",
                    "",
                ),
                "prompt_file":
                    f"image_prompt_"
                    f"{scene_number:02d}.txt",
                "image_file":
                    (
                        f"Scene_"
                        f"{scene_number:02d}.png"
                        if not skip_images
                        else None
                    ),
            }
        )

    (
        video_dir
        / "scene_plan.json"
    ).write_text(
        json.dumps(
            scene_plan,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------
    # 6. METADATA
    # --------------------------------------------------

    metadata = {
        "video_number": number,
        "story_id": story["id"],
        "title_telugu": title,
        "hashtags_english": hashtags,
        "weekday": weekday,
        "date": date_label,
        "deity": story["deity_name"],
        "deity_key": story["deity_key"],
        "language": story["language"],
        "scene_count": 5,
        "image_engine": (
            "skipped"
            if skip_images
            else "huggingface"
        ),
        "hf_model": (
            None
            if skip_images
            else settings.get("hf_model")
        ),
        "images": [
            item["file"]
            for item in images
        ],
        "narration_text_file":
            "Narration_Telugu.txt",
        "narration_audio_file":
            "Narration.mp3",
        "status":
            "content_ready_for_tts",
    }

    (
        video_dir
        / "metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------
    # 7. LOG
    # --------------------------------------------------

    log_lines = [
        f"Story ID: {story['id']}",
        f"Video: Video-{number:02d}",
        f"Deity: {story['deity_name']}",
        f"Title: {title}",
        (
            "Images: SKIPPED"
            if skip_images
            else f"Images generated: {len(images)}"
        ),
        "Narration text: CREATED",
        "Narration MP3: PENDING ELEVENLABS STEP",
        (
            "Hashtags: "
            + " ".join(hashtags)
        ),
    ]

    (
        video_dir
        / "log.txt"
    ).write_text(
        "\n".join(log_lines),
        encoding="utf-8",
    )

    print(
        f"[{video_dir.name}] "
        "Episode package completed"
    )

    return video_dir
