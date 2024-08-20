from time import gmtime, strftime

import requests


class SponsorSegmentsInfra:
    def get_sponsor_segments(self, url: str):
        video_id = self.extract_video_id(url)

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
                    formatted_segment = f"{strftime('%H:%M:%S', gmtime(start_time))}\
- {strftime('%H:%M:%S', gmtime(end_time))}"
                    sponsor_segments.append(formatted_segment)

        return sponsor_segments

    def extract_video_id(self, url: str) -> str:
        return url.split("=")[-1]
