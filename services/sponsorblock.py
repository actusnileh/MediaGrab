import requests
import moviepy.editor as mpy


def get_sponsor_segments(url):
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


def cut_video_segments(video_path, segments_to_cut):
    video = mpy.VideoFileClip(video_path)
    clips = []
    previous_end = 0

    for segment in segments_to_cut:
        start_time, end_time = segment
        if previous_end < start_time:
            clips.append(video.subclip(previous_end, start_time))
        previous_end = end_time

    if previous_end < video.duration:
        clips.append(video.subclip(previous_end, video.duration))

    final_clip = mpy.concatenate_videoclips(clips)

    final_clip.write_videofile(video_path.replace(".mp4", "_sb.mp4"), codec="libx264")
    return video_path.replace(".mp4", "_sb.mp4")
