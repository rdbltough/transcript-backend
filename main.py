"""
YouTube Transcript Backend
--------------------------
Fetches YouTube transcripts (in whatever language is available — not just
English) using the youtube-transcript-api library, and returns them as
JSON. The Android app calls this instead of scraping YouTube directly.

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Then test: http://localhost:8000/transcript?video_id=dQw4w9WgXcQ
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

app = FastAPI(title="YouTube Transcript Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/transcript")
def get_transcript(video_id: str = Query(..., min_length=11, max_length=11)):
    try:
        transcript_list_obj = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prefer English if available, otherwise grab whatever language
        # the video actually has captions in (manually created or auto-
        # generated) — this is what makes non-English videos work.
        try:
            transcript = transcript_list_obj.find_transcript(["en"])
        except NoTranscriptFound:
            transcript = next(iter(transcript_list_obj))

        fetched = transcript.fetch()
        language_code = transcript.language_code

    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Captions are disabled for this video.")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No transcript found for this video.")
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video is unavailable.")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch transcript: {e}")

    segments = [
        {
            "text": entry["text"],
            "start": entry["start"],
            "duration": entry["duration"],
        }
        for entry in fetched
    ]
    return {"video_id": video_id, "language_code": language_code, "segments": segments}
