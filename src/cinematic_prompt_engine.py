import json
from pathlib import Path

def load_prompt_config():
    return json.loads(Path("config/prompts.json").read_text(encoding="utf-8"))

def build_cinematic_prompts(story):
    cfg = load_prompt_config()
    common = cfg["common_style"]
    negative = cfg["negative_prompt"]
    roles = cfg["scene_roles"]

    prompts = []

    for index, seed in enumerate(story["scene_seed_descriptions"], start=1):
        role = roles[index - 1]

        # Make each prompt story-aware.
        prompt = (
            f"Scene {index} ({role}). "
            f"Deity: {story['deity_name']}. "
            f"Episode title: {story['title']}. "
            f"Story fact: {story['fact']} "
            f"Visual action: {seed}. "
            f"{common}. "
            f"Maintain visual continuity with the same deity design across all five scenes."
        )

        prompts.append({
            "scene": index,
            "role": role,
            "prompt": prompt,
            "negative_prompt": negative,
            "aspect_ratio": "9:16",
        })

    return prompts

def write_prompt_files(video_dir, story):
    prompts = build_cinematic_prompts(story)

    # Combined JSON
    (video_dir / "prompts.json").write_text(
        json.dumps(prompts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Individual text files
    for item in prompts:
        path = video_dir / f"image_prompt_{item['scene']:02d}.txt"
        path.write_text(
            item["prompt"] +
            "\n\nNEGATIVE PROMPT:\n" +
            item["negative_prompt"],
            encoding="utf-8",
        )

    return prompts
