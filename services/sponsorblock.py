import requests
from time import strftime, gmtime


def get_sponsor_segments(url) -> str:
    video_id = url.split("=")[-1]

    response = requests.get(
        f"https://sponsor.ajay.app/api/skipSegments?videoID={video_id}"
    )

    sponsor_segments = []

    if response.status_code == 200:
        segments = response.json()
        for segment in segments:
            if segment["category"] in ["sponsor", "selfpromo", "interaction"]:
                start_time = segment["segment"][0]
                end_time = segment["segment"][1]
                formatted_segment = [
                    strftime("%H:%M:%S", gmtime(start_time)),
                    strftime("%H:%M:%S", gmtime(end_time)),
                ]
                sponsor_segments.append(formatted_segment)
    if sponsor_segments:
        text = "Найдены рекламные интеграции на промежутках:\n"
        text += "\n".join(" - ".join(segment) for segment in sponsor_segments)
    else:
        text = "Рекламные интеграции не найдены"
    return text


print(get_sponsor_segments("https://www.youtube.com/watch?v=SAFEqxF9A0U"))
