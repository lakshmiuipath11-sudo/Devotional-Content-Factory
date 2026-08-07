import argparse,json
from pathlib import Path
from scheduler import resolve_run_date
from weekday_router import route_weekday
from library_manager import select_stories
from episode_generator import build_episode

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",help="YYYY-MM-DD")
    args=parser.parse_args()
    run_date=resolve_run_date(args.date)
    weekday,deity=route_weekday(run_date)
    settings=json.loads(Path("config/settings.json").read_text(encoding="utf-8"))
    date_label=run_date.strftime("%d-%m-%Y")
    base=Path("output")/weekday/date_label
    base.mkdir(parents=True,exist_ok=True)
    stories=select_stories(deity["key"],settings["videos_per_day"],f"{weekday}-{date_label}")
    for i,story in enumerate(stories,1):
        build_episode(base,i,story,weekday,date_label)
    print(f"Created {len(stories)} episode packages in {base}")

if __name__=="__main__":
    main()
