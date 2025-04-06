from utilities.utils_config import load_compilation_config
from utilities.utils_io import file_dump
from utilities.utils_path import timestamps_file


def time_to_seconds(time_str: str) -> int:
    """Convert HH:MM:SS time format to seconds."""
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s


def seconds_to_time(seconds: int) -> str:
    """Convert seconds to HH:MM:SS format."""
    return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"


def generate_timestamps():
    """Generate a YouTube timestamps file from the YAML config."""
    clips = load_compilation_config()

    timestamps = []
    current_time = 0  # Start from 00:00:00

    for i_clip, (key, clip) in enumerate(clips.items()):
        start_sec = time_to_seconds(clip["start"])
        end_sec = time_to_seconds(clip["end"])
        duration = end_sec - start_sec

        chapter_time = seconds_to_time(current_time)
        # chapter_name = clip['info']['description']
        chapter_name = f"{i_clip+1}/{len(clips)}"
        timestamps.append(f"{chapter_time},{chapter_name}")
        current_time += duration  # Update for next chapter

        print(f"[{i_clip+1}/{len(clips)}] {clip['url']}")

    # Write to output file
    file_dump("\n".join(timestamps), timestamps_file)

    print(f"Timestamps saved to {timestamps_file}")


if __name__ == "__main__":
    generate_timestamps()
