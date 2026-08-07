from pathlib import Path
import random
from story_loader import load_story

def select_stories(deity_key,count,seed):
    story_files=sorted((Path("library")/deity_key).glob("fact*.json"))
    if not story_files:
        raise FileNotFoundError(f"No stories found for {deity_key}")
    rng=random.Random(seed)
    chosen=[]
    while len(chosen)<count:
        batch=story_files[:]
        rng.shuffle(batch)
        chosen.extend(batch)
    return [load_story(p) for p in chosen[:count]]
