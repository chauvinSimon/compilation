# note

## :film_strip: How This Compilation Was Made

I collected **video segments** featuring **elite short- and long-distance triathletes**.
The compilation is structured using [metadata.yaml](metadata.yaml), which contains:
- Video source links
- Start and end timestamps
- Contextual details (race conditions, athlete actions, key observations)

This allows for easy organization, reproducibility and future updates.

# ffmpeg

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
(.venv) (draft) simon-chauvin@me:~/drafts/compilation$ ffmpeg -version
ffmpeg version 4.3 Copyright (c) 2000-2020 the FFmpeg developers
built with gcc 7.3.0 (crosstool-NG 1.23.0.449-a04d0)
configuration: --prefix=/opt/conda/conda-bld/ffmpeg_1597178665428/_h_env_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placeh --cc=/opt/conda/conda-bld/ffmpeg_1597178665428/_build_env/bin/x86_64-conda_cos6-linux-gnu-cc --disable-doc --disable-openssl --enable-avresample --enable-gnutls --enable-hardcoded-tables --enable-libfreetype --enable-libopenh264 --enable-pic --enable-pthreads --enable-shared --disable-static --enable-version3 --enable-zlib --enable-libmp3lame
libavutil      56. 51.100 / 56. 51.100
libavcodec     58. 91.100 / 58. 91.100
libavformat    58. 45.100 / 58. 45.100
libavdevice    58. 10.100 / 58. 10.100
libavfilter     7. 85.100 /  7. 85.100
libavresample   4.  0.  0 /  4.  0.  0
libswscale      5.  7.100 /  5.  7.100
libswresample   3.  7.100 /  3.  7.100
```


### :mag: pre-commit

```bash
pre-commit install

pre-commit run --all-files
```

### :sunny: uv

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
