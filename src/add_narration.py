import argparse
from pathlib import Path

from elevenlabs_tts import narration_file_to_mp3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="output")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.output_root)

    files = sorted(root.rglob("Narration_Telugu.txt"))

    if not files:
        raise SystemExit(
            f"No Narration_Telugu.txt files found inside: {root}"
        )

    print(f"Found {len(files)} narration file(s).")

    failed = 0

    for txt_file in files:
        mp3_file = txt_file.with_name("Narration.mp3")

        if mp3_file.exists() and not args.overwrite:
            print(f"[SKIP] {mp3_file}")
            continue

        try:
            print(f"[TTS] {txt_file}")

            narration_file_to_mp3(
                txt_file,
                mp3_file
            )

            print(f"[OK] {mp3_file}")

        except Exception as error:
            print(f"[ERROR] {txt_file}: {error}")
            failed += 1

    if failed:
        raise SystemExit(
            f"{failed} narration(s) failed."
        )

    print("All Telugu narrations generated successfully.")


if __name__ == "__main__":
    main()
