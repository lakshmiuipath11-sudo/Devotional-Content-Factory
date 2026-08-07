import json
from pathlib import Path

def route_weekday(run_date):
    cfg = json.loads(Path("config/deities.json").read_text(encoding="utf-8"))
    weekday = run_date.strftime("%A")
    return weekday, cfg[weekday]
