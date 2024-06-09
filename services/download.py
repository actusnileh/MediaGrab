import os
import yt_dlp

from api.schemas.download_schema import VideoSchema


def download_video(video_data: VideoSchema) -> str:
    quality_value = video_data.quality.to_value()

    if video_data.only_audio:
        quality_str = "bestaudio/best"
        ydl_opts = {
            "format": quality_str,
            "outtmpl": "videos/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "merge_output_format": "mp3",
        }
    else:
        quality_str = f"bestvideo[height<={quality_value}]+bestaudio/best[height<={quality_value}]"
        ydl_opts = {
            "format": quality_str,
            "outtmpl": "videos/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_data.url, download=True)
        video_dir = "/app/videos"
        file_name = (
            f"{info['title']}.mp3".replace("?", "？")
            if video_data.only_audio
            else f"{info['title']}.mp4".replace("?", "？")
        )
        filename = os.path.join(video_dir, file_name)

    return filename
