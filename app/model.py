from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch
import torchaudio
import io
import numpy as np

class MusicGenerator:
    def __init__(self):
        self.model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
        self.processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model.to(self.device)

    def generate(self, prompt: str, duration: int = 10) -> io.BytesIO:
        try:
            duration = min(duration, 30)

            print(f"Generating audio with prompt: {prompt}")
            inputs = self.processor(
                text=[prompt],
                padding=True,
                return_tensors="pt",
            ).to(self.device)

            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                guidance_scale=3.0,
            )

            # Remover dimensões extras e mover para CPU
            audio_data = audio_values.cpu().float()

            # Garantir formato correto do tensor
            if len(audio_data.shape) == 3:
                audio_data = audio_data.squeeze(0)  # Remove dimensão do batch

            # Normalizar o áudio
            audio_max = torch.abs(audio_data).max()
            if audio_max > 0:
                audio_data = audio_data / audio_max

            # Salvar como WAV
            buffer = io.BytesIO()
            torchaudio.save(
                buffer,
                audio_data,
                sample_rate=32000,
                format="wav",
                bits_per_sample=16
            )
            buffer.seek(0)

            print(f"Generated audio size: {buffer.getbuffer().nbytes} bytes")
            return buffer

        except Exception as e:
            print(f"Error in generate: {str(e)}")
            raise
