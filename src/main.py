import argparse
import json
from pathlib import Path

from scheduler import resolve_run_date
from weekday_router import route_weekday
from library_manager import select_stories
from episode_generator import build_episode


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--date",
        help="Generation date in YYYY-MM-DD format",
        required=False,
    )

    parser.add_argument(
        "--videos",
        type=int,
        default=None,
        help="Number of videos to generate",
    )

    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Generate episode content without Hugging Face images",
    )

    args = parser.parse_args()

    run_date = resolve_run_date(args.date)

    weekday, deity = route_weekday(run_date)

    settings = json.loads(
        Path("config/settings.json").read_text(
            encoding="utf-8"
        )
    )

    if args.videos is not None:
        video_count = args.videos
    else:
        video_count = int(
            settings.get("videos_per_day", 10)
        )

    if video_count < 1 or video_count > 10:
        raise ValueError(
            "--videos must be between 1 and 10"
        )

    date_label = run_date.strftime("%d-%m-%Y")

    output_base = (
        Path("output")
        / weekday
        / date_label
    )

    output_base.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 70)
    print("PROJECT ANANTA - DEVOTIONAL CONTENT FACTORY")
    print("=" * 70)

    print(f"Date         : {date_label}")
    print(f"Weekday      : {weekday}")
    print(f"Deity        : {deity['name']}")
    print(f"Videos       : {video_count}")
    print(f"Skip images  : {args.skip_images}")

    print("=" * 70)

    stories = select_stories(
        deity_key=deity["key"],
        count=video_count,
        seed=f"{weekday}-{date_label}",
    )

    for index, story in enumerate(
        stories,
        start=1
    ):
        print()
        print("-" * 70)
        print(
            f"Processing Video-{index:02d}"
        )
        print("-" * 70)

        build_episode(
            base=output_base,
            number=index,
            story=story,
            weekday=weekday,
            date_label=date_label,
            settings=settings,
            skip_images=args.skip_images,
        )

    print()
    print("=" * 70)
    print(
        f"SUCCESS: Created {video_count} "
        f"episode package(s)"
    )
    print(f"Output: {output_base}")
    print("=" * 70)


if __name__ == "__main__":
    main()
