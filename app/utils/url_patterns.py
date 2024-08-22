import re


YOUTUBE_REGEX = re.compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$",
)

VK_REGEX = re.compile(
    r"^(?:https?:\/\/)?(?:www\.)?vk\.com\/video(?:-\d+_\d+)?(?:\?.*)?$",
)

RUTUBE_REGEX = re.compile(
    r"^(?:https?:\/\/)?(?:www\.)?rutube\.ru\/video\/[a-zA-Z0-9]+\/?(?:\?.*)?$",
)
