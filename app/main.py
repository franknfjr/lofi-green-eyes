from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.model import MusicGenerator
from pydub import AudioSegment
import io
import traceback

class MusicRequest(BaseModel):
    prompt: str
    duration: int = 10

app = FastAPI()
model = MusicGenerator()

@app.post("/generate")
async def generate_music(request: MusicRequest):
    try:
        print(f"Processing request - prompt: {request.prompt}, duration: {request.duration}")
        wav_buffer = model.generate(request.prompt, request.duration)

        print("Converting to MP3...")
        wav_buffer.seek(0)
        # Garantir que o áudio tem um canal (mono)
        audio = AudioSegment.from_wav(wav_buffer).set_channels(1)

        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3", bitrate="192k", parameters=["-ac", "1"])
        mp3_buffer.seek(0)

        size = mp3_buffer.getbuffer().nbytes
        print(f"Generated MP3 size: {size} bytes")

        if size == 0:
            raise ValueError("Generated audio is empty")

        filename = f"lofi_{request.prompt[:30].replace(' ', '_')}.mp3"

        return StreamingResponse(
            mp3_buffer,
            media_type="audio/mpeg",
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
