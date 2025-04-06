from time import time

from utilities.utils import get_timestamp
from utilities.utils_config import load_compilation_config, load_config
from utilities.utils_ffmpeg import (
    create_black_transition,
    get_video_resolution,
    merge_videos,
    process_video,
)
from utilities.utils_log import logger
from utilities.utils_path import (
    merged_video_dir,
    processed_video_dir,
    raw_video_dir,
    transition_video_path,
)
from utilities.utils_youtube import download_video_segment


def main():
    config = load_config()
    video_width = config["resolution"]["width"]
    video_height = config["resolution"]["height"]

    transition_duration_s = config["transition_duration_s"]
    use_transitions = transition_duration_s > 0

    infos = load_compilation_config()
    processed_video_paths = []

    # Create transition video if it doesn’t exist
    if not transition_video_path.exists():
        if use_transitions:
            create_black_transition(
                transition_video_path,
                width=video_width,
                height=video_height,
                duration=transition_duration_s,
            )

    # 1/3 Download videos
    for i_video, (video_stem, info_dict) in enumerate(infos.items()):
        video_name = f"{video_stem}.{config['video_format']}"
        video_path = raw_video_dir / video_name
        if video_path.exists():
            continue
        download_video_segment(
            video_url=info_dict["url"],
            start_time=info_dict["start"],
            end_time=info_dict["end"],
            output_path=video_path,
        )
        resolution = get_video_resolution(video_path=video_path)
        if resolution:
            logger.info(
                f"resolution = {resolution[0]}x{resolution[1]} for {video_stem}"
            )
            if resolution[0] != video_width:
                logger.warning(f"{resolution[0] = } != {video_width}")
            if resolution[1] != video_height:
                logger.warning(f"{resolution[1] = } != {video_height}")

    # 2/3 Process videos
    for i_video, (video_stem, info_dict) in enumerate(infos.items()):
        video_name = f"{video_stem}.{config['video_format']}"
        raw_video_path = raw_video_dir / video_name
        assert raw_video_path.exists(), f"Video file not found: {raw_video_path}"

        # Output video path
        video_name = raw_video_path.name
        processed_video_path = processed_video_dir / video_name

        if (
            processed_video_path.exists()
            and not config["override_existing_processed_videos"]
        ):
            logger.info(f"{video_name} already processed: {raw_video_path}")
        else:
            process_video(
                raw_video_path=raw_video_path,
                processed_video_path=processed_video_path,
                id_str=f"Clip #{i_video + 1}/{len(infos)}",
                config=config,
                info_dict=info_dict,
            )

        processed_video_paths.append(processed_video_path)
        if use_transitions:
            # Add transition after each clip
            processed_video_paths.append(transition_video_path)

    # 3/3 Merge videos
    merge_videos(
        processed_video_paths=processed_video_paths,
        saving_path=merged_video_dir
        / f"{get_timestamp()}_{config['compilation_file_name'].replace('.yaml', '')}.mp4",
    )


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"total `main()` duration = {time() - start_time:.1f}s")
