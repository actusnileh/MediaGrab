import yt_dlp

from api.schemas.youtube import YoutubeVideoSchema


def download_video(video_data: YoutubeVideoSchema):
    quality_value = video_data.quality.value

    if video_data.only_audio:
        quality_str = "bestaudio/best"
        ydl_opts = {
            "format": quality_str,
            "outtmpl": "%(title)s.%(ext)s",
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
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_data.url])

    return "%(title)s.mp3" if video_data.only_audio else "%(title)s.mp4"
