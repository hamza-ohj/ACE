import os
import random
import subprocess
import time
import sys
import string
import shutil
import yt_dlp
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.align import Align
from rich import print as rprint
import rich.box

# Dynamically add FFmpeg binaries to runtime path
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except ImportError:
    pass

# ================= GLOBAL CONFIGURATION =================
# Use absolute paths based on the script's actual location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
INPUT_MAIN = os.path.join(SCRIPT_DIR, "input_main")
INPUT_STITCH = os.path.join(SCRIPT_DIR, "input_stitch")
INPUT_AUDIO = os.path.join(SCRIPT_DIR, "input_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "processed_output")
DOWNLOADS_DIR = os.path.join(SCRIPT_DIR, "downloads")   # NEW FOLDER FOR MODULE 6
FONT_FILE = os.path.join(SCRIPT_DIR, "font.ttf")
# ========================================================

console = Console()

# ================= HELPER FUNCTIONS =================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def count_files(directory):
    if not os.path.exists(directory): return 0
    return len([f for f in os.listdir(directory) if f.lower().endswith(('.mp4', '.mov', '.mkv', '.avi', '.mp3', '.wav'))])

def print_header():
    clear_screen()
    c_main = count_files(INPUT_MAIN)
    c_stitch = count_files(INPUT_STITCH)
    c_audio = count_files(INPUT_AUDIO)
    c_down = count_files(DOWNLOADS_DIR) # Count downloads

    ace_logo = r"""
[bold red]A[/bold red]   [bold red]C[/bold red]   [bold red]E[/bold red]
[bold white]┌───┐[/bold white] [bold white]┌───┐[/bold white] [bold white]┌───┐[/bold white]
[bold white]|[/bold white][bold red]A[/bold red]  [bold white]│[/bold white] [bold white]|[/bold white][bold red]C[/bold red]  [bold white]│[/bold white] [bold white]|[/bold white][bold red]E[/bold red]  [bold white]│[/bold white]
[bold white]│[/bold white] [bold red]♥[/bold red] [bold white]|[/bold white] [bold white]│[/bold white] [bold red]♦[/bold red] [bold white]|[/bold white] [bold white]│[/bold white] [bold red]♠[/bold red] [bold white]|[/bold white]
[bold white]└───┘[/bold white] [bold white]└───┘[/bold white] [bold white]└───┘[/bold white]
"""
    rprint(Align.center(ace_logo))
    rprint(Align.center("[bold white]AUTOMATED CONTENT ENGINE v2.2[/bold white]"))
    rprint(Align.center("[grey53]CPA & Traffic Command Center[/grey53]"))
    # Added 'Downloads' count to the header
    rprint(Align.center(f"[grey30]Targets: [bold green]{c_main}[/bold green] | Audio: {c_audio} | Stitch: {c_stitch} | [cyan]Downloads: {c_down}[/cyan][/grey30]\n"))

def setup_folders():
    dirs = [INPUT_MAIN, INPUT_STITCH, INPUT_AUDIO, OUTPUT_DIR, DOWNLOADS_DIR]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        rprint("[bold red]CRITICAL ERROR: FFmpeg not detected on system path.[/bold red]")
        sys.exit(1)

def get_files(directory, extensions):
    return [f for f in os.listdir(directory) if f.lower().endswith(extensions)]

def generate_codename(extension):
    chars = string.ascii_lowercase + string.digits
    random_name = ''.join(random.choice(chars) for _ in range(12))
    return f"{random_name}{extension}"

def get_video_duration(file_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except:
        return 0

# ================= MODULE 1: GHOST PROTOCOL =================
def get_dna_filters():
    random.seed()
    speed = random.uniform(0.95, 1.05)
    gamma = random.uniform(0.90, 1.10)
    sat = random.uniform(1.00, 1.20)
    noise = random.randint(2, 6)
    return speed, gamma, sat, noise

def run_ghost_protocol():
    files = get_files(INPUT_MAIN, ('.mp4', '.mov', '.mkv'))
    if not files: rprint(f"[red]No videos found in {INPUT_MAIN}[/red]"); return

    add_text = Confirm.ask("Inject text overlay?")
    text_content = Prompt.ask("Enter text") if add_text else None

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%")) as progress:
        task = progress.add_task("[green]Applying DNA...", total=len(files))
        for file in files:
            in_path = os.path.join(INPUT_MAIN, file)
            out_path = os.path.join(OUTPUT_DIR, generate_codename(os.path.splitext(file)[1]))
            speed, gamma, sat, noise = get_dna_filters()
            
            vf = (f"scale=-2:600,eq=gamma={gamma:.3f}:saturation={sat:.3f},noise=alls={noise}:allf=t+u,"
                  f"unsharp=3:3:0.5:3:3:0.0,setpts={1/speed:.5f}*PTS")
            af = f"atempo={speed:.5f}"

            if text_content:
                sanitized = text_content.replace(":", "\\:")
                font_cmd = f"fontfile='{FONT_FILE}'" if os.path.exists(FONT_FILE) else ("fontfile='C\\:/Windows/Fonts/arial.ttf'" if os.name == 'nt' else "font='Sans'")
                vf += (f",drawtext=text='{sanitized}':{font_cmd}:fontcolor=white:fontsize=32:"
                       "borderw=2:bordercolor=black:x=(w-text_w)/2:y=h-th-50")

            cmd = ['ffmpeg', '-y', '-i', in_path, '-map_metadata', '-1', '-filter_complex', f"[0:v]{vf}[v];[0:a]{af}[a]", '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '26', '-preset', 'veryfast', '-c:a', 'aac', out_path]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
                progress.advance(task)
            except: pass
    rprint("[bold green]Ghost Protocol Complete.[/bold green]")

# ================= MODULE 2: HYDRA SPLITTER =================
def run_hydra_splitter():
    files = get_files(INPUT_MAIN, ('.mp4', '.mov'))
    if not files: rprint(f"[red]No videos found in {INPUT_MAIN}[/red]"); return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:
        task = progress.add_task("[cyan]Splitting...", total=len(files))
        for file in files:
            in_path = os.path.join(INPUT_MAIN, file)
            duration = get_video_duration(in_path)
            midpoint = duration / 2
            base_name, ext = os.path.splitext(file)
            p1_out = os.path.join(OUTPUT_DIR, f"{base_name}_PART1{ext}")
            p2_out = os.path.join(OUTPUT_DIR, f"{base_name}_PART2{ext}")
            subprocess.run(['ffmpeg', '-y', '-i', in_path, '-t', str(midpoint), '-c', 'copy', p1_out], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            subprocess.run(['ffmpeg', '-y', '-i', in_path, '-ss', str(midpoint), '-c', 'copy', p2_out], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            progress.advance(task)
    rprint("[bold green]Hydra Split Complete.[/bold green]")

# ================= MODULE 3: VENOM INJECTOR =================
def run_venom_injector():
    main_files = get_files(INPUT_MAIN, ('.mp4',))
    stitch_files = get_files(INPUT_STITCH, ('.mp4',))
    if not main_files or not stitch_files: rprint("[red]Missing files in input_main or input_stitch[/red]"); return

    stitch_clip = os.path.join(INPUT_STITCH, stitch_files[0])
    mode = Prompt.ask("Inject location?", choices=["Start", "End"], default="End")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:
        task = progress.add_task("[magenta]Stitching...", total=len(main_files))
        for file in main_files:
            main_path = os.path.join(INPUT_MAIN, file)
            out_path = os.path.join(OUTPUT_DIR, f"venom_{file}")
            scale = "[0:v]scale=-2:720[v0];[1:v]scale=-2:720[v1];"
            concat = f"{scale}[v1][1:a][v0][0:a]concat=n=2:v=1:a=1[outv][outa]" if mode == "Start" else f"{scale}[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]"
            inputs = ['-i', main_path, '-i', stitch_clip]
            subprocess.run(['ffmpeg', '-y'] + inputs + ['-filter_complex', concat, '-map', '[outv]', '-map', '[outa]', '-c:v', 'libx264', '-preset', 'veryfast', '-c:a', 'aac', out_path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            progress.advance(task)
    rprint("[bold green]Venom Injection Complete.[/bold green]")

# ================= MODULE 4: SHADOW AUDIO =================
def run_shadow_audio():
    video_files = get_files(INPUT_MAIN, ('.mp4',))
    audio_files = get_files(INPUT_AUDIO, ('.mp3', '.wav'))
    if not video_files or not audio_files: rprint("[red]Missing files[/red]"); return
    
    hidden_track = os.path.join(INPUT_AUDIO, audio_files[0])
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:
        task = progress.add_task("[blue]Mixing...", total=len(video_files))
        for file in video_files:
            in_path = os.path.join(INPUT_MAIN, file)
            out_path = os.path.join(OUTPUT_DIR, f"shadow_{file}")
            fc = "[1:a]volume=0.01[a1];[0:a][a1]amix=inputs=2:duration=first[a_out]"
            subprocess.run(['ffmpeg', '-y', '-i', in_path, '-i', hidden_track, '-filter_complex', fc, '-map', '0:v', '-map', '[a_out]', '-c:v', 'copy', '-c:a', 'aac', out_path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            progress.advance(task)
    rprint("[bold green]Shadow Audio Complete.[/bold green]")

# ================= MODULE 5: VELOCITY =================
def run_velocity():
    files = get_files(INPUT_MAIN, ('.mp4',))
    if not files: rprint(f"[red]No videos in {INPUT_MAIN}[/red]"); return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:
        task = progress.add_task("[orange3]Boosting velocity...", total=len(files))
        for file in files:
            in_path = os.path.join(INPUT_MAIN, file)
            out_path = os.path.join(OUTPUT_DIR, f"velocity_{file}")
            subprocess.run(['ffmpeg', '-y', '-i', in_path, '-filter_complex', "[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]", '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-c:a', 'aac', out_path], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            progress.advance(task)
    rprint("[bold green]Velocity Boost Complete.[/bold green]")

# ================= MODULE 6: THE HARVESTER (UPDATED) =================
def run_harvester():
    rprint("[bold cyan]THE HARVESTER[/bold cyan]")
    url = Prompt.ask(">> Paste Link Here")
    if not url: return

    rprint("\n[bold white]SELECT QUALITY:[/bold white]")
    rprint("[1] Best Available (Auto-Convert to MP4)")
    rprint("[2] 1080p (Force High Res)")
    rprint("[3] 720p (Lightweight)")
    rprint("[4] Audio Only (MP3)")
    
    q_choice = IntPrompt.ask("Choice", choices=["1", "2", "3", "4"], default=1, show_choices=False)
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'), 
        'ffmpeg_location': None, 
    }

    if q_choice == 1:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'
    elif q_choice == 2:
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        ydl_opts['merge_output_format'] = 'mp4'
    elif q_choice == 3:
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        ydl_opts['merge_output_format'] = 'mp4'
    elif q_choice == 4:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    rprint("\n[bold white]Harvesting...[/bold white]")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        rprint(f"[bold green]SUCCESS:[/bold green] Saved to '{DOWNLOADS_DIR}'")
    except Exception as e:
        rprint(f"[bold red]FAILED:[/bold red] {e}")

# ================= MAIN MENU =================
def show_menu():
    print_header()
    table = Table(show_header=False, box=rich.box.ROUNDED, border_style="grey53")
    table.add_column("ID", style="bold cyan", justify="center", width=4)
    table.add_column("Module Name", style="bold white")
    table.add_column("Description", style="grey70")
    
    table.add_row("1", "GHOST PROTOCOL", "Full DNA Randomizer & Anonymizer")
    table.add_row("2", "HYDRA SPLITTER", "Split videos (Part 1 / Part 2)")
    table.add_row("3", "VENOM INJECTOR", "Stitch Intro/Outro to all files")
    table.add_row("4", "SHADOW AUDIO", "Mix hidden trending audio (1% vol)")
    table.add_row("5", "VELOCITY BOOST", "Speed up 1.25x (High Retention)")
    table.add_row("6", "THE HARVESTER", "Download (Saved to /downloads)")
    table.add_row("0", "EXIT", "Close ACE")

    rprint(Panel(table, title="[bold white]OPERATIONAL MODULES[/bold white]", border_style="red", padding=(1, 2)))

def main():
    setup_folders()
    check_ffmpeg()
    while True:
        show_menu()
        choice = IntPrompt.ask("SELECT MODULE", choices=["1", "2", "3", "4", "5", "6", "0"], show_choices=False)
        
        if choice == 0: sys.exit()
        rprint(f"\n[bold white]Initializing Module {choice}...[/bold white]")
        time.sleep(0.5)
        
        if choice == 1: run_ghost_protocol()
        elif choice == 2: run_hydra_splitter()
        elif choice == 3: run_venom_injector()
        elif choice == 4: run_shadow_audio()
        elif choice == 5: run_velocity()
        elif choice == 6: run_harvester()
        
        rprint("\n[grey53]Press Enter to return to menu...[/grey53]")
        input()

if __name__ == "__main__":
    main()