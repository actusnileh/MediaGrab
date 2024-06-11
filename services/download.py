import os
import uuid
import yt_dlp

from api.schemas.download_schema import VideoSchema
from services.sponsorblock import cut_video_segments, get_sponsor_segments


def download_video(video_data: VideoSchema) -> str:
    video_uuid = str(uuid.uuid4())

    quality_value = video_data.quality.to_value()

    if video_data.only_audio:
        quality_str = "bestaudio/best"
        ydl_opts = {
            "format": quality_str,
            "outtmpl": f"videos/{video_uuid}.%(ext)s",
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
            "outtmpl": f"videos/{video_uuid}.%(ext)s",
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_data.url, download=True)
        video_dir = "/app/videos"
        file_name = (
            f"{video_uuid}.mp3" if video_data.only_audio else f"{video_uuid}.mp4"
        )
        filepath = os.path.join(video_dir, file_name)
        if video_data.sponsor_block:
            segments = get_sponsor_segments(video_data.url)
            sb_filepath = cut_video_segments(filepath, segments)
            if os.path.exists(filepath):
                os.remove(filepath)
                os.rename(sb_filepath, filepath)
    return filepath, file_name
