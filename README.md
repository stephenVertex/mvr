# mvr - Move Recent Files

A command-line utility to quickly move recently created files from common directories to your current working directory.

## Installation

```bash
./install.sh
```

This will create a symlink in `~/.local/bin/mvr`. Make sure `~/.local/bin` is in your PATH.

## Usage

```bash
mvr [OPTIONS] [PATTERNS]
```

### Directory Options

- `--docs` - Search in ~/Documents
- `--desktop` - Search in ~/Desktop
- `--dl` - Search in ~/Downloads
- `--auto` - Search in ~, ~/Downloads, ~/Desktop, and ~/Documents

### Pattern Options

- `--scr` - Match Screenshot* files
- `--images` - Match image files (jpg, jpeg, png, gif, bmp, tiff, webp, heic)
- `--videos` - Match video files (mov, mp4, mkv, avi, wmv, flv, webm, m4v)
- Custom patterns - Provide your own glob patterns (e.g., `*.dmg`, `*.pdf`)

### Other Options

- `--window=N` - Time window in minutes (default: 5)
- `--dr` - Dry run mode (list files without moving them)

## Examples

### Move screenshots from Documents (last 10 minutes)
```bash
mvr --docs --window=10 --scr
```

### Move all files from Desktop (last 5 minutes)
```bash
mvr --desktop --window=5
```

### Move from common directories automatically
```bash
mvr --auto
```

### Dry run to see what would be moved
```bash
mvr --auto --dr
```

### Move .dmg files from Downloads
```bash
mvr *.dmg --dl
```

### Move image files (last 5 minutes by default)
```bash
mvr --images
```

### Move video files (last 30 minutes)
```bash
mvr --videos --window=30
```

### Combine options - Move screenshots and images from Desktop
```bash
mvr --desktop --scr --images
```

### Move multiple patterns from Downloads
```bash
mvr *.dmg *.pkg --dl --window=15
```

## Requirements

- Python 3.14+
- uv (for dependency management)

## How It Works

`mvr` searches the specified directories for files matching the given patterns that were created within the specified time window. It then moves those files to your current working directory, automatically handling filename conflicts by appending numbers to duplicate names.

The utility uses file creation time (birth time on macOS) to determine if a file falls within the time window.
