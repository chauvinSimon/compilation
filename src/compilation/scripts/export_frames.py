from pathlib import Path

import cv2
from utilities.utils_config import load_config
from utilities.utils_ffmpeg import normalize_video
from utilities.utils_log import logger
from utilities.utils_path import frames_dir, raw_normalized_video_dir, raw_video_dir


def normalize_raw_videos():
    config = load_config()
    for raw_video_path in raw_video_dir.glob(f"*.{config['video_format']}"):
        normalized_path = raw_normalized_video_dir / raw_video_path.name
        if not normalized_path.exists():
            normalize_video(input_path=raw_video_path, output_path=normalized_path)


def export_frames(video_folder: Path, output_folder: Path):
    config = load_config()
    for video_path in video_folder.glob(f"*.{config['video_format']}"):
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            logger.error(f"Failed to open {video_path.name}: {video_path}")
            continue

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if frame_count > 0:
            # frame_position = 0  # first frame
            # frame_position = frame_count // 2  # middle frame
            frame_position = frame_count - 1  # last frame

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)

            ret, frame = cap.read()
            if ret:
                frame_filename = output_folder / f"{video_path.stem}.jpg"
                cv2.imwrite(str(frame_filename), frame)
                logger.info(f"Saved frame from {video_path.name} as {frame_filename}")

        cap.release()


if __name__ == "__main__":
    print(cv2.getBuildInformation())

    # otherwise issues with encoding: OpenCV’s FFmpeg build doesn't include AV1 decoding by default.
    normalize_raw_videos()

    export_frames(video_folder=raw_normalized_video_dir, output_folder=frames_dir)
