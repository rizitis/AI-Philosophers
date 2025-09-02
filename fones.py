#!/usr/bin/env python3
from kokoro import KPipeline
import soundfile as sf

# Όλες οι φωνές που υποστηρίζει το Kokoro
VOICES = [
    "af_alloy",
    "af_aoede",
    "af_bella",
    "af_heart",
    "af_kore",
    "af_nicole",
    "af_sarah",
    "af_sky",
    "am_adam",
    "am_michael",
    "bm_daniel"
]

text = "This is a test of the Kokoro TTS voice system."

# Φτιάξε ένα pipeline (αρκεί ένα)
pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")

for voice in VOICES:
    try:
        print(f"🔊 Testing voice: {voice}")
        gen = pipeline(text, voice=voice, speed=1.0)
        for i, (gs, ps, audio) in enumerate(gen):
            filename = f"test_{voice}.wav"
            sf.write(filename, audio, 24000)
            print(f"✅ Saved: {filename}")
            break  # αρκεί μία φράση
    except Exception as e:
        print(f"❌ Failed to generate with {voice}: {e}")
