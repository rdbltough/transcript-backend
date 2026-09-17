from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

app = FastAPI()

@app.get("/transcript")
def get_transcript(video_id: str):
    try:
        raw = YouTubeTranscriptApi().fetch(video_id)
        segments = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in raw
        ]
        return {"video_id": video_id, "segments": segments}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/formats")
def get_formats(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        formats = []
        for f in info.get("formats", []):
            if not f.get("url"):
                continue
            has_video = f.get("vcodec") != "none"
            has_audio = f.get("acodec") != "none"
            f_type = "video" if has_video else ("audio" if has_audio else "unknown")
            label_bits = []
            if f.get("height"):
                label_bits.append(f"{f['height']}p")
            if f.get("abr"):
                label_bits.append(f"{int(f['abr'])}kbps")
            label = " ".join(label_bits) if label_bits else f.get("format_note", f["format_id"])
            formats.append({
                "format_id": f["format_id"],
                "label": label,
                "type": f_type,
                "ext": f.get("ext", ""),
                "url": f["url"],
            })
        return {"video_id": video_id, "title": info.get("title", ""), "formats": formats}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
