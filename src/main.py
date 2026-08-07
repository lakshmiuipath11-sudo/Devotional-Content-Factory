import argparse
import json
from pathlib import Path

from episode_generator import build_episode
from library_manager import select_stories
from scheduler import resolve_run_date
from weekday_router import route_weekday


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="YYYY-MM-DD")
    parser.add_argument(
        "--videos",
        type=int,
        default=None,
        help="Override videos_per_day. Use 1 for testing.",
    )
    args = parser.parse_args()

    run_date = resolve_run_date(args.date)
    weekday, deity = route_weekday(run_date)

    settings = json.loads(
        Path("config/settings.json").read_text(encoding="utf-8")
    )

    count = (
        args.videos
        if args.videos is not None
        else int(settings["videos_per_day"])
    )

    if count < 1 or count > 10:
        raise ValueError("--videos must be between 1 and 10")

    date_label = run_date.strftime("%d-%m-%Y")
    base = Path("output") / weekday / date_label
    base.mkdir(parents=True, exist_ok=True)

    stories = select_stories(
        deity["key"],
        count,
        seed=f"{weekday}-{date_label}",
    )

    for index, story in enumerate(stories, start=1):
        build_episode(
            base,
            index,
            story,
            weekday,
            date_label,
            settings,
        )

    print(
        f"SUCCESS: Created {len(stories)} Hugging Face "
        f"episode package(s) in {base}"
    )


if __name__ == "__main__":
    main()
