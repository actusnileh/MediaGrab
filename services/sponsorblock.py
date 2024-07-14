import requests


def get_sponsor_segments(url) -> list[list[float]]:
    video_id = url.split("=")[-1]

    response = requests.get(
        f"https://sponsor.ajay.app/api/skipSegments?videoID={video_id}"
    )
    if response.status_code == 200:
        segments = response.json()
        sponsor_segments = [
            segment["segment"]
            for segment in segments
            if segment["category"] == "sponsor"
        ]
        return sponsor_segments
    return []
