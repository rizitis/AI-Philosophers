#!/usr/bin/env python3
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import tempfile
import os

# --- Ρυθμίσεις ---
OUTPUT_FILE = "theme_intro.wav"
DURATION = 10  # δευτερόλεπτα
SAMPLE_RATE = 24000  # συμβατό με Kokoro TTS
FREQUENCY_DRONE = 55.0  # A1 - βαθύς "παλμός"
FREQUENCY_PAD = 110.0   # A2 - ambient pad
GAIN_DRONE = -12  # dB
GAIN_PAD = -16
GAIN_PULSES = -10

# --- Δημιουργία ηχητικών σημάτων ---

def sine_wave(freq, duration, sample_rate, volume_db=-20):
    """Δημιουργεί sine wave"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Από dB σε amplitude
    amplitude = 10 ** (volume_db / 20)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    # Fade in/out
    fade_len = int(sample_rate * 0.5)
    if len(wave) > fade_len * 2:
        wave[:fade_len] *= np.linspace(0, 1, fade_len)
        wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    return wave

def digital_pulse(duration, sample_rate, volume_db=-10):
    """Ψηφιακός παλμός με glitch"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.random.normal(0, 1, len(t)) * (10 ** (volume_db / 20))
    wave *= np.sin(2 * np.pi * 1500 * t)  # high-frequency burst
    fade_len = int(sample_rate * 0.1)
    wave[:fade_len] *= np.linspace(0, 1, fade_len)
    wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    return wave

# --- Δημιουργία επιπέδων ---
print("🎵 Generating ambient theme music...")

# 1. Βαθύς drone (σαν heartbeat του AI)
drone = sine_wave(FREQUENCY_DRONE, DURATION, SAMPLE_RATE, GAIN_DRONE)

# 2. Ambient pad (σαν "ψηφιακός ουρανός")
pad = sine_wave(FREQUENCY_PAD, DURATION, SAMPLE_RATE, GAIN_PAD)
pad *= np.sin(np.linspace(0, np.pi, len(pad)))  # slow rise-fall

# 3. Ψηφιακοί παλμοί (κάθε 3-5 δευτερόλεπτα)
pulses = np.zeros(int(SAMPLE_RATE * DURATION))
pulse_duration = 0.15
for i in range(0, DURATION * SAMPLE_RATE, np.random.randint(3000, 6000)):
    if i + int(pulse_duration * SAMPLE_RATE) < len(pulses):
        pulse = digital_pulse(pulse_duration, SAMPLE_RATE, GAIN_PULSES)
        pulses[i:i+len(pulse)] += pulse[:len(pulses)-i]

# --- Συνδυασμός ---
combined = drone + pad + pulses
combined /= 3  # normalize
combined = np.int16(combined / np.max(np.abs(combined)) * 32767)  # to 16-bit

# --- Αποθήκευση ---
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    temp_file = tmp.name
    wavfile.write(temp_file, SAMPLE_RATE, combined)

# Μετατροπή σε pydub για crossfade και export
audio = AudioSegment.from_wav(temp_file)
audio = audio.fade_in(2000).fade_out(3000)  # smooth edges

audio.export(OUTPUT_FILE, format="wav")
os.unlink(temp_file)

print(f"✅ Theme music created: {OUTPUT_FILE}")
print(f"🔊 Duration: {DURATION}s | Sample Rate: {SAMPLE_RATE} Hz")
