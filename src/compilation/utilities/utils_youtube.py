import subprocess
from pathlib import Path
from time import time

from utilities.utils_config import load_config
from utilities.utils_path import data_dir


def download_video_segment(
    start_time="00:00:00",
    end_time="00:00:10",
    video_url="",
    output_path: Path = Path("output.mp4"),
):
    """
    Download a specific segment of a YouTube video using yt-dlp.

    Args:
        start_time (str): Start time of the segment in HH:MM:SS format
        end_time (str): End time of the segment in HH:MM:SS format
        video_url (str): Full YouTube video URL
        output_path (str): Path where the output video will be saved

    Returns:
        str: Path to the downloaded video segment
    """
    # Validate input
    if not video_url:
        raise ValueError("Video URL must be provided")

    config = load_config()
    # Construct yt-dlp command
    command = [
        "yt-dlp",
        "--cookies-from-browser",  # against "Sign in to confirm you’re not a bot."
        config["web_browser"],
        "--format",
        # "best",
        "bv*",  # best video-only (bv)
        # todo: understand other formats
        # "bv*[ext=mp4]",
        # "bestvideo[ext=mp4]",
        "--download-sections",
        f"*{start_time}-{end_time}",  # Specific segment
        "-o",
        str(output_path),
        video_url,
    ]

    print(" ".join(command))

    try:
        # Execute the download command
        print(f"Downloading video segment from {start_time} to {end_time}...")
        print(f"{output_path.stem}: {video_url}")

        time_start = time()
        _ = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"duration = {time() - time_start:.1f} s")

        # Check if file was created
        if not output_path.exists():
            raise RuntimeError("Download completed but no output file found")

        print(f"Video segment saved to {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        print("Download failed:")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")
        raise RuntimeError(f"yt-dlp download failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


# Example usage
if __name__ == "__main__":
    download_video_segment(
        # start_time="00:00:25",
        # end_time="00:00:45",
        # video_url="https://youtu.be/d2Z0cyUmvr8",
        start_time="01:41:25",
        end_time="01:41:44",
        video_url="https://youtu.be/tIqYGhyiI1Y",
        output_path=data_dir / "tmp.mp4",
    )
    # yt-dlp --cookies-from-browser chrome -F https://youtu.be/tIqYGhyiI1Y
