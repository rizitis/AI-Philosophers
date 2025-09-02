#!/usr/bin/env python3
from pydub import AudioSegment
from pathlib import Path
import time
import re

# --- Ρυθμίσεις ---
OUTPUT_DIR = Path("Podcasts")
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = int(time.time())
output_file = OUTPUT_DIR / f"ai_debate_{timestamp}.wav"

# --- Αρχεία intro και outro ---
INTRO_FILE = Path("000_intro.wav")
OUTRO_FILE = Path("999_outro.wav")

# --- Δημιουργία podcast ---
print("🎙️ Creating AI Debate Podcast...")
podcast = AudioSegment.empty()  # ξεκινάμε άδειο

# -- Music -- #
if Path("theme_intro.wav").exists():
    theme = AudioSegment.from_wav("theme_intro.wav")
    podcast += theme
    podcast += AudioSegment.silent(duration=500)  # μικρή παύση πριν τη φωνή

# --- Προσθήκη intro ---
if INTRO_FILE.exists():
    print(f"✅ Loading intro: {INTRO_FILE}")
    intro_audio = AudioSegment.from_wav(INTRO_FILE)
    intro_audio = intro_audio.set_frame_rate(48000)
    podcast += intro_audio
    podcast += AudioSegment.silent(duration=500)  # μικρή παύση μετά το intro
else:
    print(f"🟡 Warning: {INTRO_FILE} not found. Skipping intro.")
    podcast += AudioSegment.silent(duration=1000)  # 1 sec σιωπή αντί για intro

# --- Φόρτωση και ταξινόμηση των απαντήσεων ---
wav_files = sorted(
    Path(".").glob("tts_output_*.wav"),
    key=lambda f: int(re.search(r"(\d+)", f.name).group(1))
)

if not wav_files:
    print("❌ No tts_output_*.wav files found. Nothing to merge.")
    exit(1)

for wav_file in wav_files:
    print(f"➕ Adding: {wav_file}")
    audio = AudioSegment.from_wav(wav_file)
    audio = audio.set_frame_rate(48000)
    podcast += audio
    podcast += AudioSegment.silent(duration=300)  # παύση μεταξύ απαντήσεων

# --- Προσθήκη outro ---
if OUTRO_FILE.exists():
    print(f"✅ Loading outro: {OUTRO_FILE}")
    outro_audio = AudioSegment.from_wav(OUTRO_FILE)
    outro_audio = outro_audio.set_frame_rate(48000)
    podcast += outro_audio
else:
    print(f"🟡 Warning: {OUTRO_FILE} not found. Skipping outro.")
    podcast += AudioSegment.silent(duration=1000)  # 1 sec σιωπή στο τέλος

# --- Προσθήκη outro music ---
if Path("theme_outro.wav").exists():
    theme_outro = AudioSegment.from_wav("theme_outro.wav")
    podcast += theme_outro
    print("✅ Added theme outro")

# --- Εξαγωγή ---
print(f"🔊 Exporting to {output_file}...")
podcast.export(output_file, format="wav", parameters=["-ar", "48000"])
print(f"✅ Podcast successfully saved: {output_file}")
