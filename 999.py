#!/usr/bin/env python3
from kokoro import KPipeline
import soundfile as sf
import numpy as np

# --- Ρυθμίσεις ---
TEXT = """
Thank you, QWEN and GEMMA, for your thoughtful perspectives.

Randomness challenges our definition of intelligence. On one hand, it is directionless, chaotic, and seems the opposite of deliberate thought. On the other, it is the source of novelty, creativity, and evolution itself. Perhaps intelligence and randomness are not opposites, but two sides of the same coin. And so we are left with a question humanity may never fully answer: Is intelligence the mind shaping chaos, or chaos itself shaping the mind?

'Thank you for engaging with these questions that may never have a final answer. '
'Farewell!'
""".strip()

VOICE = "af_sarah"
OUTPUT_FILE = "999_outro.wav"
SAMPLE_RATE = 24000

# --- Δημιουργία ήχου ---
print("🙏 Generating AI Prayer...")

pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
generator = pipeline(TEXT, voice=VOICE, speed=0.85, split_pattern=r"\n\n|\n")  # χωρίζει σε παραγράφους

# Συγκέντρωση όλων των audio chunks
audio_segments = []

for i, (gs, ps, audio) in enumerate(generator):
    print(f"📝 Generated chunk {i+1}")
    audio_segments.append(audio)

# Συνένωση όλων των segments
if audio_segments:
    full_audio = np.concatenate(audio_segments, axis=0)
    sf.write(OUTPUT_FILE, full_audio, SAMPLE_RATE)
    print(f"✅ AI Prayer saved: {OUTPUT_FILE}")
else:
    print("❌ Failed to generate audio.")
