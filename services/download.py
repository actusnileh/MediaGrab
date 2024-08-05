import os
import uuid

import yt_dlp
from yt_dlp.utils import DownloadError, YoutubeDLError

from api.schemas.download_schema import VideoSchema


async def download_video(video_data: VideoSchema) -> str:
    try:
        video_uuid = str(uuid.uuid4())
        quality_value = video_data.quality.to_value()
        outtmpl = f"videos/{video_uuid}.%(ext)s"

        if video_data.only_audio:
            format_option = "m4a/bestaudio/best"
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                }
            ]
        else:
            format_option = f"bestvideo[height<={quality_value}]+bestaudio/best"
            postprocessors = []

        ydl_opts = {
            "format": format_option,
            "outtmpl": outtmpl,
            "postprocessors": postprocessors,
        }

        if video_data.sponsor_block:
            ydl_opts["postprocessors"].extend(
                [
                    {
                        "key": "SponsorBlock",
                        "api": "https://sponsor.ajay.app",
                        "categories": [
                            "sponsor",
                            "selfpromo",
                            "interaction",
                        ],
                        "when": "after_filter",
                    },
                    {
                        "key": "ModifyChapters",
                        "force_keyframes": False,
                        "remove_chapters_patterns": [],
                        "remove_ranges": [],
                        "remove_sponsor_segments": set(
                            ["sponsor", "selfpromo", "interaction"]
                        ),
                        "sponsorblock_chapter_title": "[SponsorBlock]: %(category_names)l",
                    },
                    {
                        "key": "FFmpegMetadata",
                        "add_chapters": True,
                        "add_infojson": None,
                        "add_metadata": False,
                    },
                ]
            )
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_data.url, download=True)
            extension = info.get("ext", "webm")
            file_name = f"{video_uuid}.{extension}"

        video_dir = "/app/videos"
        filepath = os.path.join(video_dir, file_name)

        if video_data.cut:
            pass

        return filepath, file_name
    except DownloadError as e:
        print(f"Download error: {e}")
        raise YoutubeDLError from e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise Exception from e
