from datetime import datetime
from fastapi.routing import APIRouter


router = APIRouter()


@router.get("/")
async def get_root():
    return {
        "api_name": "MediaGrab API",
        "version": "1.0.0",
        "description": "This API allows users to download and retrieve information about videos.",
        "developer": "https://github.com/actusnileh",
        "endpoints": [
            {"path": "/docs", "description": "Get documentation and usage examples."},
            {
                "path": "/video_audio",
                "description": "Download video/audio from YouTube and VK with the ability to select the video quality.",
                "parameters": [
                    {
                        "name": "url",
                        "type": "string",
                        "description": "URL of the video to download.",
                    },
                    {
                        "name": "quality",
                        "type": "string",
                        "description": "Desired quality of the video (lowest, low, medium, high, highest).",
                    },
                    {
                        "name": "only_audio",
                        "type": "boolean",
                        "description": "Allows to extract the audio track from a video.",
                    },
                    {
                        "name": "sponsor_block",
                        "type": "boolean",
                        "description": "Extracts sponsor integrations from video.",
                    },
                ],
            },
            {
                "path": "/information",
                "description": "Get information about the video.",
                "parameters": [
                    {
                        "name": "url",
                        "type": "string",
                        "description": "URL of the video to download.",
                    },
                ],
            },
            {
                "path": "/help",
                "description": "Returns a list of available functions and their descriptions for working with videos.",
            },
        ],
        "timestamp": datetime.now().isoformat(),
    }
