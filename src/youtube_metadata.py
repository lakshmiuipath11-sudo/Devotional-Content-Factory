import json
import re
from pathlib import Path

def load_config():
    return json.loads(Path("config/youtube.json").read_text(encoding="utf-8"))

def generate_telugu_title(story):
    title=story["title"].strip()
    if "?" not in title:
        title=f"{title} తెలుసా?"
    return title[:90]

def to_english_hashtag(text):
    if re.search(r"[^\x00-\x7F]", text):
        return None
    words=re.findall(r"[A-Za-z0-9]+", text)
    if not words:
        return None
    return "#" + "".join(w[:1].upper()+w[1:] for w in words)

def generate_english_hashtags(story):
    cfg=load_config()
    tags=list(cfg["deity_hashtags"].get(story["deity_key"],[]))
    for item in story.get("tags",[]):
        h=to_english_hashtag(item)
        if h:
            tags.append(h)
    tags.extend(cfg["default_hashtags"])
    result=[]
    seen=set()
    for tag in tags:
        k=tag.lower()
        if k not in seen:
            seen.add(k)
            result.append(tag)
    return result[:cfg.get("max_hashtags",10)]

def write_youtube_files(video_dir,story):
    title=generate_telugu_title(story)
    hashtags=generate_english_hashtags(story)
    (video_dir/"Title_Telugu.txt").write_text(title,encoding="utf-8")
    (video_dir/"Hashtags_English.txt").write_text(" ".join(hashtags),encoding="utf-8")
    return title,hashtags
