import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create vertical video clips."
    )
    parser.add_argument("video", type=Path)
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--duration", type=float, default=30)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("clips"))
    args = parser.parse_args()

    if not args.video.is_file():
        parser.error("Input video does not exist.")

    if args.start < 0 or args.duration <= 0 or args.count < 1:
        parser.error("Invalid start, duration or count.")

    if not shutil.which("ffmpeg"):
        parser.error("Install FFmpeg and add it to PATH first.")

    args.output.mkdir(parents=True, exist_ok=True)

    for i in range(args.count):
        target = args.output / f"clip_{i + 1:02d}.mp4"

        subprocess.run([
            "ffmpeg", "-n",
            "-ss", str(args.start + i * args.duration),
            "-i", str(args.video),
            "-t", str(args.duration),
            "-map", "0:v:0",
            "-map", "0:a?",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-movflags", "+faststart",
            str(target)
        ], check=True)

        print(f"Saved: {target}")


if __name__ == "__main__":
    main()
