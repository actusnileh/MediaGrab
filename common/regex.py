import re


URL_PATTERNS = {
    "youtube": re.compile(
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    ),
    "vk": re.compile(r"^(?:https?:\/\/)?(?:www\.)?vk\.com\/video-\d+_\d+$"),
}

EMAIL_PATTERN = re.compile(r"^[\w.-]+@\w+\.[a-z]+(\.[a-z]+)*$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,30}$")
PASSWORD_PATTERN = re.compile(r"[A-Za-z\d@$!%*?&]{6,}")
