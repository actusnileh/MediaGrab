# app/infrastructure/download_infra.py

import os
import uuid
import yt_dlp
from typing import Tuple
from app.schema.video_schema import VideoSchema


class YtDLPDownloader:
    video_dir = "/app/videos"

    @staticmethod
    async def download_video(video: VideoSchema) -> Tuple[str, str]:
        video_uuid = str(uuid.uuid4())
        quality_value = video.quality.to_value()
        outtmpl = f"{YtDLPDownloader.video_dir}/{video_uuid}.%(ext)s"

        if video.only_audio:
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
            "cookiefile": "cookies.txt",
        }

        if video.sponsor_block:
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
            info = ydl.extract_info(video.url, download=True)
            extension = info.get("ext", "webm")
            file_name = f"{video_uuid}.{extension}"

        filepath = os.path.join(YtDLPDownloader.video_dir, file_name)

        return filepath, file_name
