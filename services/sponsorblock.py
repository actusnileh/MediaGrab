import requests
import moviepy.editor as mpy


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


async def cut_video_segments(video_path, segments_to_cut):
    video = mpy.VideoFileClip(video_path)
    clips = []
    previous_end = 0

    subclip_cache = {}

    for segment in segments_to_cut:
        start_time, end_time = segment
        if previous_end < start_time:
            if (previous_end, start_time) not in subclip_cache:
                subclip_cache[(previous_end, start_time)] = video.subclip(
                    previous_end, start_time
                )
            clips.append(subclip_cache[(previous_end, start_time)])
        previous_end = end_time

    if previous_end < video.duration:
        if (previous_end, video.duration) not in subclip_cache:
            subclip_cache[(previous_end, video.duration)] = video.subclip(
                previous_end, video.duration
            )
        clips.append(subclip_cache[(previous_end, video.duration)])

    final_clip = mpy.concatenate_videoclips(clips, method="compose")

    output_path = video_path.replace(".mp4", "_sb.mp4")
    final_clip.write_videofile(
        output_path, codec="libx264", preset="ultrafast", threads=4
    )

    return output_path
