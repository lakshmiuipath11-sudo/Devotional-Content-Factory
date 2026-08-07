# Project ANANTA V1.6 — Hugging Face Image Engine

Overlay these files on top of your existing V1.4/V1.5 project.

Required GitHub secret:

HF_TOKEN

The workflow now accepts:
- date: optional YYYY-MM-DD
- videos: 1 to 10

Start with videos = 1.

One video generates five AI images:
- Scene_01.png
- Scene_02.png
- Scene_03.png
- Scene_04.png
- Scene_05.png

It also preserves:
- Narration_Telugu.txt
- Title_Telugu.txt
- Hashtags_English.txt
- prompts.json
- image_prompt_01.txt ... image_prompt_05.txt
- image_manifest.json
- metadata.json
- log.txt

Important:
10 videos means 50 image-generation requests. Free Hugging Face quota,
provider availability, or rate limits may prevent a full 10-video run.
Test one video first.
