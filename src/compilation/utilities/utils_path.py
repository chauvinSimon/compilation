from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent

config_path = project_root / "config.yaml"
assert config_path.exists(), f"config file not found at {config_path}"

data_dir = project_root / "data"
video_dir = data_dir / "video"
raw_video_dir = video_dir / "raw"
raw_normalized_video_dir = video_dir / "raw_normalized"
processed_video_dir = video_dir / "processed"
normalized_videos_dir = video_dir / "normalized"
merged_video_dir = video_dir / "merged"

video_paths_to_merge_file = video_dir / "paths_to_merge_file.txt"
transition_video_path = processed_video_dir / "black_transition.mp4"

raw_video_dir.mkdir(exist_ok=True, parents=True)
raw_normalized_video_dir.mkdir(exist_ok=True, parents=True)
processed_video_dir.mkdir(exist_ok=True, parents=True)
normalized_videos_dir.mkdir(exist_ok=True, parents=True)
merged_video_dir.mkdir(exist_ok=True, parents=True)

frames_dir = data_dir / "frames"
frames_dir.mkdir(exist_ok=True, parents=True)

compilation_configs_dir = project_root / "compilation_configs"
assert compilation_configs_dir.exists(), (
    f"compilation_configs_dir not found at " f"{compilation_configs_dir}"
)

timestamps_file = data_dir / "timestamps.csv"
