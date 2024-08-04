import requests
from pytube import YouTube

from common.settings import settings


def get_information_youtube(url):
    yt = YouTube(url)
    return yt.thumbnail_url, yt.author, yt.title, yt.length


def get_information_vk(url):
    video_id = url.split("video")[-1].split("%")[0]

    params = {"videos": video_id, "access_token": settings.vk_token, "v": "5.131"}
    response = requests.get("https://api.vk.com/method/video.get", params=params)
    data = response.json()

    if "response" in data and "items" in data["response"]:
        video_info = data["response"]["items"][0]
        preview_url = video_info["image"][-1]["url"]
        title = video_info["title"]
        length = video_info["duration"]
        return preview_url, title, length
    else:
        return None
