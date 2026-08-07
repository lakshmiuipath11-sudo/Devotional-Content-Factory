import json
from pathlib import Path
from story_validator import validate_story

def load_story(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_story(data)
    return data
