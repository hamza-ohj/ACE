\# ACE (Automated Content Engine)



A Python-based command-line interface (CLI) for batch video processing, modification, and downloading. 



\## Prerequisites

\* Python 3.x

\* FFmpeg (Must be installed and added to your system PATH)



\## Installation \& Setup

1\. Download or clone this repository to your local machine.

2\. Ensure you only have `ACE.py` and `start.bat` in the root directory.

3\. Run `start.bat`. This script will automatically:

&#x20;  \* Install the required Python dependencies (`rich`, `yt-dlp`, `static-ffmpeg`).

&#x20;  \* Launch the main application.

&#x20;  \* Generate the required input and output directories.



\## Directory Structure

Upon initialization, ACE automatically creates the following operational directories. Place your source files in the corresponding folders before running a module.



\* `input\_main/`: Place source video files here (`.mp4`, `.mov`, `.mkv`).

\* `input\_stitch/`: Place secondary video clips here for concatenation.

\* `input\_audio/`: Place audio files here for background mixing (`.mp3`, `.wav`).

\* `downloads/`: Destination folder for media retrieved via the downloading module.

\* `processed\_output/`: Destination folder for all rendered media.



\## Operational Modules



| Module ID | Name | Description |

| :--- | :--- | :--- |

| \*\*1\*\* | \*\*Ghost Protocol\*\* | Modifies video DNA to bypass detection. Applies randomized speed, gamma, saturation, and noise filters. Includes an optional text overlay feature. |

| \*\*2\*\* | \*\*Hydra Splitter\*\* | Analyzes video duration and cuts the file exactly at the midpoint, generating a Part 1 and Part 2. |

| \*\*3\*\* | \*\*Venom Injector\*\* | Stitches a secondary clip (from `input\_stitch`) to either the beginning or end of the primary videos. |

| \*\*4\*\* | \*\*Shadow Audio\*\* | Injects a hidden audio track (from `input\_audio`) into the source videos at 1% volume. |

| \*\*5\*\* | \*\*Velocity Boost\*\* | Accelerates video playback speed by 1.25x to increase viewer retention. |

| \*\*6\*\* | \*\*The Harvester\*\* | Downloads media directly from URLs. Supports auto-conversion to MP4 (Best/1080p/720p) or audio extraction to MP3. |



\## Dependencies

\* `rich`: Terminal formatting and UI.

\* `yt-dlp`: Media downloading capabilities.

\* `static-ffmpeg`: FFmpeg binary management.

