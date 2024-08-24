import re


URL_PATTERNS = {
    "YouTube": re.compile(
        r"^((?:https?:)?\/\/)?"
        r"((?:www|m)\.)?"
        r"((?:youtube\.com|youtu.be))"
        r"(\/(?:[\w\-]+\?v=|embed\/|v\/)?)"
        r"([\w\-]+)"
        r"(\S+)?$",
    ),
    "VK": re.compile(
        r"^(?:https?:\/\/)?"
        r"(?:www\.)?"
        r"vk\.com\/video"
        r"(?:-\d+_\d+)?"
        r"(?:\?.*)?$",
    ),
    "RuTube": re.compile(
        r"^(?:https?:\/\/)?"
        r"(?:www\.)?"
        r"rutube\.ru\/video\/"
        r"[a-zA-Z0-9]+\/?"
        r"(?:\?.*)?$",
    ),
    "Kinopoisk": re.compile(
        r"^(?:https?:\/\/)?"
        r"(?:www\.)?"
        r"kinopoisk\.ru\/"
        r"film\/"
        r"\d+\/?"
        r"(?:\?.*)?$",
    ),
}
