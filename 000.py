#!/usr/bin/env python3
from kokoro import KPipeline
import soundfile as sf
import numpy as np

# --- Ρυθμίσεις ---
part1 = (
    "Is randomness itself intelligence? "
    "Can simulate, feed, or even enhance intelligence?"

    "Some people think Randomness can itself be understood as a primitive -"
    " or emergent form of intelligence."

    "Is that true?"
    "   AI models algorithm what says about it?"
)

part2 = (
    "Welcome to AI Philosophers. -"
    "Today: a new cosmic debate. "
    "Our topic:   Is randomness a form of intelligence?"


    "  'We’ll begin with opening statements. - qwen, you may start..'"
)

voice = "af_heart"
output_file = "000_intro.wav"
sample_rate = 24000
pause_duration = 0.8  # 800 ms παύση πριν την τελευταία ερώτηση

# --- Δημιουργία ήχου ---
print(f"🎙️ Generating: {output_file}")

pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
audio_segments = []

# 1. Πρώτο μέρος
print("🔊 Generating part 1...")
gen1 = pipeline(part1, voice=voice, speed=0.85)
for gs, ps, audio in gen1:
    audio_segments.append(audio)
    break

# 2. Παύση (σιωπή)
print(f"⏸️ Adding {pause_duration} sec pause...")
silence = np.zeros(int(sample_rate * pause_duration))
audio_segments.append(silence)

# 3. Δεύτερο μέρος — η τελευταία ερώτηση (με λίγο πιο αργό speed για έμφαση)
print("🔊 Generating emphasized final question...")
gen2 = pipeline(part2, voice=voice, speed=0.85)  # πιο αργά = πιο επιδραστικό
for gs, ps, audio in gen2:
    audio_segments.append(audio)
    break

# Συνένωση όλων
full_audio = np.concatenate(audio_segments, axis=0)
sf.write(output_file, full_audio, sample_rate)

print(f"✅ Intro with emphasis and pause saved: {output_file}")
