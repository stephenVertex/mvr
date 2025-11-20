#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

"""
mvr - Move Recent files
A utility to move recently created files from common directories to the current directory.
"""

import argparse
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional


# Predefined patterns
PATTERNS = {
    "scr": ["Screenshot*"],
    "images": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp", "*.heic"],
    "videos": ["*.mov", "*.mp4", "*.mkv", "*.avi", "*.wmv", "*.flv", "*.webm", "*.m4v"],
}

# Directory shortcuts
DIRECTORIES = {
    "docs": Path.home() / "Documents",
    "desktop": Path.home() / "Desktop",
    "dl": Path.home() / "Downloads",
    "auto": [Path.home(), Path.home() / "Downloads", Path.home() / "Desktop", Path.home() / "Documents"],
}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Move recently created files to the current directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mvr --docs --window=10 --scr    # Move screenshots from Documents (last 10 mins)
  mvr --desktop --window=5        # Move all files from Desktop (last 5 mins)
  mvr --auto                      # Move from common dirs (last 5 mins)
  mvr --auto --dr                 # Dry run
  mvr *.dmg --dl                  # Move .dmg files from Downloads (last 5 mins)
  mvr --images                    # Move image files (last 5 mins)
  mvr --videos --window=30        # Move video files (last 30 mins)
        """
    )

    # Directory options
    parser.add_argument("--docs", action="store_true", help="Search in ~/Documents")
    parser.add_argument("--desktop", action="store_true", help="Search in ~/Desktop")
    parser.add_argument("--dl", action="store_true", help="Search in ~/Downloads")
    parser.add_argument("--auto", action="store_true", help="Search in ~, ~/Downloads, ~/Desktop, ~/Documents")

    # Pattern options
    parser.add_argument("--scr", action="store_true", help="Match Screenshot* files")
    parser.add_argument("--images", action="store_true", help="Match image files")
    parser.add_argument("--videos", action="store_true", help="Match video files")

    # Time window
    parser.add_argument("--window", type=int, default=5, help="Time window in minutes (default: 5)")

    # Dry run
    parser.add_argument("--dr", action="store_true", help="Dry run - list files without moving")

    # Custom patterns
    parser.add_argument("patterns", nargs="*", help="Custom file patterns (e.g., *.dmg)")

    return parser.parse_args()


def get_search_directories(args) -> List[Path]:
    """Determine which directories to search based on arguments."""
    directories = []

    if args.auto:
        directories.extend(DIRECTORIES["auto"])
    else:
        if args.docs:
            directories.append(DIRECTORIES["docs"])
        if args.desktop:
            directories.append(DIRECTORIES["desktop"])
        if args.dl:
            directories.append(DIRECTORIES["dl"])

    # Default to current directory if none specified
    if not directories:
        directories.append(Path.cwd())

    return directories


def get_patterns(args) -> List[str]:
    """Determine which file patterns to use based on arguments."""
    patterns = []

    # Add predefined patterns
    if args.scr:
        patterns.extend(PATTERNS["scr"])
    if args.images:
        patterns.extend(PATTERNS["images"])
    if args.videos:
        patterns.extend(PATTERNS["videos"])

    # Add custom patterns
    if args.patterns:
        patterns.extend(args.patterns)

    # Default to all files if no patterns specified
    if not patterns:
        patterns.append("*")

    return patterns


def is_within_window(file_path: Path, minutes: int) -> bool:
    """Check if file was created within the specified time window."""
    try:
        # Use birth time (creation time) on macOS
        file_time = datetime.fromtimestamp(file_path.stat().st_birthtime)
    except AttributeError:
        # st_birthtime not available on this system
        print(f"Warning: Cannot determine creation time for {file_path}, skipping", file=sys.stderr)
        return False

    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    return file_time >= cutoff_time


def find_matching_files(directories: List[Path], patterns: List[str], window: int, dest_dir: Path) -> List[Path]:
    """Find all files matching the criteria."""
    matching_files = []

    for directory in directories:
        if not directory.exists():
            continue

        # Skip the destination directory
        if directory.resolve() == dest_dir.resolve():
            continue

        for pattern in patterns:
            # Use glob to find matching files
            for file_path in directory.glob(pattern):
                # Skip directories
                if not file_path.is_file():
                    continue

                # Skip files not in the immediate directory (don't recurse)
                if file_path.parent != directory:
                    continue

                # Skip dotfiles (files starting with .)
                if file_path.name.startswith('.'):
                    continue

                # Check if file is within time window
                if is_within_window(file_path, window):
                    matching_files.append(file_path)

    # Remove duplicates and sort
    matching_files = sorted(set(matching_files))
    return matching_files


def move_files(files: List[Path], dest_dir: Path, dry_run: bool = False):
    """Move files to destination directory."""
    if not files:
        print("No matching files found.")
        return

    print(f"Found {len(files)} file(s):")

    for file_path in files:
        dest_path = dest_dir / file_path.name

        # Handle name conflicts
        if dest_path.exists():
            base = dest_path.stem
            suffix = dest_path.suffix
            counter = 1
            while dest_path.exists():
                dest_path = dest_dir / f"{base}_{counter}{suffix}"
                counter += 1

        if dry_run:
            print(f"  [DRY RUN] Would move: {file_path} -> {dest_path}")
        else:
            try:
                shutil.move(str(file_path), str(dest_path))
                print(f"  Moved: {file_path} -> {dest_path}")
            except Exception as e:
                print(f"  Error moving {file_path}: {e}", file=sys.stderr)


def main():
    """Main entry point."""
    args = parse_arguments()

    # Get destination directory (current directory)
    dest_dir = Path.cwd()

    # Determine search directories
    search_dirs = get_search_directories(args)

    # Determine patterns
    patterns = get_patterns(args)

    # Find matching files
    matching_files = find_matching_files(search_dirs, patterns, args.window, dest_dir)

    # Move files
    move_files(matching_files, dest_dir, args.dr)


if __name__ == "__main__":
    main()
