from pytube import YouTube
import requests
from common.settings import settings


def get_information_youtube(url):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    author = yt.author
    title = yt.title
    return thumbnail_url, author, title


def get_information_vk(url):
    video_id = url.split("video")[-1].split("%")[0]

    params = {"videos": video_id, "access_token": settings.vk_token, "v": "5.131"}
    response = requests.get("https://api.vk.com/method/video.get", params=params)
    data = response.json()

    if "response" in data and "items" in data["response"]:
        video_info = data["response"]["items"][0]
        preview_url = video_info["image"]
        title = video_info["title"]
        return preview_url, title
    else:
        return None
