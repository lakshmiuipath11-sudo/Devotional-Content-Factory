REQUIRED={"id","deity_key","deity_name","language","title","hook","fact","story","moral","cta","scene_prompts","tags"}
def validate_story(data):
    missing=REQUIRED-set(data)
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")
    if len(data["scene_prompts"]) != 5:
        raise ValueError("Exactly 5 scene prompts required")
    return True
