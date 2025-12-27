import argparse
from pathlib import Path
from datetime import datetime

parser = argparse.ArgumentParser(description="Rename files in a folder safely.")
parser.add_argument("folder", help="Path to target folder")
parser.add_argument("--base", default="file", help="Base name for files")

args = parser.parse_args()

folder = Path(args.folder)

if not folder.exists() or not folder.is_dir():
    print("Error: folder does not exist or is not a directory")
    exit(1)

log_file = folder / "rename_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with log_file.open("a", encoding="utf-8") as log:
    log.write(f"\nRun at {timestamp}\n")

    for index, file in enumerate(sorted(folder.iterdir()), start=1):
        if file.is_file() and file.name != log_file.name:
            new_name = f"{args.base}_{index}{file.suffix}"
            new_path = folder / new_name

            if new_path.exists():
                log.write(f"SKIPPED (exists): {file.name}\n")
                continue

            file.rename(new_path)
            log.write(f"RENAMED: {file.name} -> {new_name}\n")

