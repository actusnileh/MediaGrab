import re
from abc import (
    ABC,
    abstractmethod,
)

import isodate
import requests

from app.core.config import configs
from app.infrastructure.sponsorblock_infra import SponsorSegmentsInfra


class VideoInfra(ABC):
    @abstractmethod
    def get_information(self, url: str):
        pass

    @abstractmethod
    def get_sponsor_segments(self, url: str):
        pass


class YouTubeInfra(VideoInfra):
    def get_information(self, url: str):
        video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url).group(1)

        params = {
            "part": "snippet,contentDetails",
            "id": video_id,
            "key": configs.youtube_token,
        }
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params=params,
        )
        response.raise_for_status()

        data = response.json()

        if "items" in data and len(data["items"]) > 0:
            video_info = data["items"][0]
            snippet = video_info["snippet"]
            content_details = video_info["contentDetails"]

            preview_url = snippet["thumbnails"]["high"]["url"]
            author = snippet["channelTitle"]
            title = snippet["title"]
            length_str = content_details["duration"]

            length = isodate.parse_duration(length_str).total_seconds()

            return preview_url, author, title, length

    def get_sponsor_segments(self, url: str):
        return SponsorSegmentsInfra().get_sponsor_segments(url)


class VkInfra(VideoInfra):
    def get_information(self, url: str):
        video_id = url.split("video")[-1].split("%")[0]

        params = {"videos": video_id, "access_token": configs.vk_token, "v": "5.131"}
        response = requests.get("https://api.vk.com/method/video.get", params=params)
        data = response.json()

        if "response" in data and "items" in data["response"]:
            video_info = data["response"]["items"][0]
            preview_url = video_info["image"][-1]["url"]
            author = "Вконтакте"
            title = video_info["title"]
            length = video_info["duration"]
            return preview_url, author, title, length
        else:
            return None

    def get_sponsor_segments(self, url: str):
        return []
