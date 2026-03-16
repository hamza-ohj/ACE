# ACE (Automated Content Engine)

A Python CLI for batch video processing, modification, and downloading.

---

## Prerequisites
* **Python 3.x**
* **FFmpeg** (Must be added to your system PATH)

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
Run the initialization script:

DOS
start.bat
This automatically installs dependencies (rich, yt-dlp, static-ffmpeg), generates the required folder structure, and launches the CLI.

Directory Structure
Place your source files in the auto-generated folders before running modules.

/input_main: Source videos (.mp4, .mov, .mkv).

/input_stitch: Secondary clips for concatenation.

/input_audio: Audio tracks for background mixing (.mp3, .wav).

/downloads: Destination for downloaded media.

/processed_output: Destination for all final rendered media.

Modules
[1] Ghost Protocol: Alters file metadata and applies randomized speed, gamma, saturation, and noise filters to bypass automated detection.

[2] Hydra Splitter: Analyzes total duration and splits the video exactly at the midpoint.

[3] Venom Injector: Concatenates a secondary clip to either the start or end of primary videos.

[4] Shadow Audio: Injects a secondary audio track at 1% volume.

[5] Velocity Boost: Increases playback speed by 1.25x.

[6] The Harvester: Downloads media via URL. Supports best quality auto-conversion (MP4) or audio extraction (MP3).

Dependencies
rich: UI and terminal formatting.

yt-dlp: Media extraction.

static-ffmpeg: FFmpeg binary management.
