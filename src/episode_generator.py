import json
from youtube_metadata import write_youtube_files

def build_episode(base,number,story,weekday,date_label):
    video_dir=base/f"Video-{number:02d}"
    video_dir.mkdir(parents=True,exist_ok=True)

    narration="\n\n".join([
        story["hook"], story["fact"], story["story"],
        "నీతి: "+story["moral"], story["cta"]
    ])
    (video_dir/"Narration_Telugu.txt").write_text(narration,encoding="utf-8")

    prompts={f"scene_{i:02d}":p for i,p in enumerate(story["scene_prompts"],1)}
    (video_dir/"prompts.json").write_text(
        json.dumps(prompts,ensure_ascii=False,indent=2),encoding="utf-8"
    )

    title,hashtags=write_youtube_files(video_dir,story)

    metadata={
        "video_number":number,
        "story_id":story["id"],
        "title_telugu":title,
        "hashtags_english":hashtags,
        "weekday":weekday,
        "date":date_label,
        "deity":story["deity_name"],
        "language":"Telugu",
        "scene_count":5,
        "status":"planned"
    }
    (video_dir/"metadata.json").write_text(
        json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8"
    )
    (video_dir/"log.txt").write_text(
        f"Story: {story['id']}\nTitle: {title}\nHashtags: {' '.join(hashtags)}\n",
        encoding="utf-8"
    )
