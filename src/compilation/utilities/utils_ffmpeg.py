import json
import shlex
import subprocess
import time
from pathlib import Path

from utilities.utils import get_duration_s
from utilities.utils_config import load_compilation_config, load_config
from utilities.utils_log import logger
from utilities.utils_overlay_text import (
    calculate_text_dimensions,
    create_text,
    get_text_position,
)
from utilities.utils_path import normalized_videos_dir, video_paths_to_merge_file


def create_black_transition(output_path, width, height, duration=0.5):
    # Generate a short black transition video
    command = f"""
    ffmpeg -f lavfi -t {duration} -i color=c=black:s={width}x{height} -c:v libx264 -tune stillimage "{output_path}"
    """
    subprocess.run(command, shell=True)


def get_video_resolution(video_path: Path):
    cmd = [
        "ffprobe",  # Calls the ffprobe command-line tool (part of FFmpeg).
        "-v",
        "error",  # Suppresses unnecessary output, only errors are shown.
        "-select_streams",
        "v:0",  # Selects the first video stream in the file.
        "-show_entries",
        "stream=width,height",  # Extracts only width and height.
        "-of",
        "json",  # Formats the output as JSON for easier parsing.
        str(video_path),  # Converts the Path object to a string for compatibility.
    ]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        width = data["streams"][0]["width"]
        height = data["streams"][0]["height"]
        return width, height
    else:
        logger.error(f"cannot read resolution: {result.stderr}")
        return None


def process_video(
    raw_video_path: Path, processed_video_path: Path, id_str: str, config, info_dict
):
    placement = info_dict.get("placement", "top_left")

    video_width = config["resolution"]["width"]
    video_height = config["resolution"]["height"]

    # Scaling filter for resizing videos to WxH
    scale_filter = f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2"

    # Create overlay text and escape special characters
    duration = get_duration_s(
        start_hh_mm_ss=info_dict["start"], end_hh_mm_ss=info_dict["end"]
    )
    id_str += f" ({duration}s)"
    overlay_text = f"{id_str}{create_text(info_dict=info_dict)}"
    text_width, text_height = calculate_text_dimensions(
        overlay_text, config["overlay_text_params"]["fontsize"]
    )
    overlay_text = overlay_text.replace(":", r"\:").replace("|", r"\|")

    # Use shlex.quote() to ensure proper escaping of spaces and special characters
    overlay_text = shlex.quote(overlay_text)

    x, y = get_text_position(
        placement, video_width, video_height, text_width, text_height, margin_pix=20
    )
    logger.info(f"{x = :.0f}")
    logger.info(f"{y = :.0f}")

    # Define credit text
    # todo: rotate credit text. I was not able to do it. Depends on ffmpeg version
    credit_text = f"{config['signature']}\nvideo credit={info_dict['credit']}"
    resolution = get_video_resolution(video_path=raw_video_path)
    if resolution:
        credit_text += f"\n({resolution[0]}x{resolution[1]})"
    credit_text = shlex.quote(credit_text)  # Escape special characters
    text_width, text_height = calculate_text_dimensions(
        credit_text, config["overlay_text_params"]["fontsize"] / 2
    )
    credit_x, credit_y = get_text_position(
        "bottom_right",
        video_width,
        video_height,
        text_width=text_width,
        text_height=text_height,
        margin_pix=5,
    )

    params = config["overlay_text_params"]
    fontcolor = params["fontcolor"]
    fontsize = params["fontsize"]
    shadowx = params["shadowx"]
    shadowy = params["shadowy"]
    shadowcolor = params["shadowcolor"]
    box = params["box"]
    boxcolor = params["boxcolor"]
    boxborderw = params["boxborderw"]

    command = [
        # FFmpeg executable
        "ffmpeg",
        # -y: Overwrite the output file without asking for confirmation
        "-y",
        # -i: Input file option, specifying the video file path
        "-i",
        f'"{raw_video_path}"',  # Enclose video_path in quotes to handle spaces in the file name
        # -vf: Video filter option, applying scale and text overlay
        "-vf",
        # Apply the scale filter and text overlay with various options
        f'"{scale_filter},'
        f"drawtext=text={overlay_text}:fontcolor={fontcolor}:fontsize={fontsize}:x={x}:y={y}:shadowx={shadowx}:shadowy={shadowy}:shadowcolor={shadowcolor}:box={box}:boxcolor={boxcolor}:boxborderw={boxborderw},",
        f'drawtext=text={credit_text}:fontcolor={fontcolor}:fontsize={fontsize / 2}:x={credit_x}:y={credit_y}:shadowx={shadowx}:shadowy={shadowy}:shadowcolor={shadowcolor}:box={box}:boxcolor={boxcolor}:boxborderw={boxborderw}"',
        # Disable audio (removes sound)
        "-an",
        # Output file path, where the processed video will be saved
        f'"{processed_video_path}"',  # Enclose processed_video_path in quotes to handle spaces in the file name
    ]

    command = " ".join(command)
    print(command)
    # Join the list into a single string and run the command
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"FFmpeg command failed with return code {result.returncode}"
        )


def normalize_video(input_path: Path, output_path: Path):
    """Normalize video by re-encoding it to ensure consistent timestamps, frame rate, and codec."""
    logger.info(f"normalizing {input_path.stem}")
    command = [
        "ffmpeg",
        "-i",
        str(input_path),  # Input video
        "-vf",
        "setpts=PTS-STARTPTS",  # Reset timestamps
        "-r",
        "25",  # Set fixed frame rate (adjust if needed)
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",  # Re-encode video
        "-c:a",
        "aac",
        "-b:a",
        "128k",  # Standardize audio
        "-y",
        str(output_path),  # Output video
    ]
    subprocess.run(command, check=True)


def merge_videos(processed_video_paths: list, saving_path: Path):
    """Normalize videos and merge them using FFmpeg."""
    config = load_config()
    normalized_videos = []
    for video in processed_video_paths:
        normalized_video_path = normalized_videos_dir / f"{video.name}"
        if (
            not normalized_video_path.exists()
            or config["override_existing_normalized_videos"]
        ):
            normalize_video(input_path=video, output_path=normalized_video_path)
        normalized_videos.append(normalized_video_path)

    # Create a text file listing processed videos for FFmpeg
    with video_paths_to_merge_file.open("w") as f:
        for video in normalized_videos:
            f.write(f"file '{video}'\n")

    # FFmpeg merge command as a list of strings
    merge_command = [
        "ffmpeg",
        "-f",
        "concat",  # Use file concatenation mode
        "-safe",
        "0",  # Allows unsafe file paths (absolute paths)
        "-i",
        str(video_paths_to_merge_file),  # Input file list
        "-c",
        "copy",  # Copy codec (since videos are normalized)
        str(saving_path),  # Output file path
    ]

    # Convert list to a string command
    merge_command = " ".join(merge_command)
    print(merge_command)

    # Run the FFmpeg command
    start_time = time.time()
    subprocess.run(merge_command, shell=True, check=True)
    print(f"duration = {time.time() - start_time:.1f} s")

    print(f"Final merged video created: {saving_path}")


if __name__ == "__main__":
    from utilities.utils_path import processed_video_dir, raw_video_dir

    infos = load_compilation_config()
    i_video = 0
    video_stem = next(iter(infos))
    # video_stem = "2024_london_w_3"
    video_name = f"{video_stem}.{load_config()['video_format']}"

    res = get_video_resolution(video_path=raw_video_dir / video_name)
    if res:
        print(f"Resolution: {res[0]}x{res[1]}")

    process_video(
        raw_video_path=raw_video_dir / video_name,
        processed_video_path=processed_video_dir / video_name,
        id_str=f"[{i_video + 1}/{len(infos)}]",
        config=load_config(),
        info_dict=infos[video_stem],
    )
