## :film_strip: How This Compilation Was Made

I collected **video segments** featuring **elite short- and long-distance triathletes**.
The compilation is structured using a [yaml compilation config](compilation_configs), which contains:
- Video source links
- Start and end timestamps
- Contextual details (race conditions, athlete actions, key observations)

This allows for easy organization, reproducibility and future updates.

## :tv: YouTube

YouTube videos are automatically downloaded using [yt-dlp](https://github.com/yt-dlp/yt-dlp).
- See `download_video_segment()` in [utils_youtube.py](src/compilation/utilities/utils_youtube.py).

## :movie_camera: ffmpeg

upgrade `yt-dlp`
```bash
uv pip install --upgrade yt-dlp
```

```bash
# checking available quality
yt-dlp -F https://youtu.be/pTCrrTUpOpU
```

```bash
yt-dlp -f best --download-sections "*00:01:23-00:02:00" "https://www.youtube.com/watch?v=d2Z0cyUmvr8"
```

```bash
(.venv) simon-chauvin@me:~/drafts/compilation$ ffmpeg -version
ffmpeg version 4.3 Copyright (c) 2000-2020 the FFmpeg developers
built with gcc 7.3.0 (crosstool-NG 1.23.0.449-a04d0)
```

## :robot: pre-commit

```bash
pre-commit install

pre-commit run --all-files
```

## :sunny: uv

to start the project, I used:

```bash
mkdir compilation
cd compilation/
uv init --package
uv venv .venv
source .venv/bin/activate
conda deactivate
...
git remote add origin https://github.com/chauvinSimon/compilation.git
git branch -M main
git push -u origin main
```
