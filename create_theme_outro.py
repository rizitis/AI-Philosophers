#!/usr/bin/env python3
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import tempfile
import os

# --- Ρυθμίσεις ---
OUTPUT_FILE = "theme_outro.wav"
DURATION = 25  # λίγο πιο αργό για fade out
SAMPLE_RATE = 24000
FREQUENCY_DRONE = 41.2  # E1 - ακόμα πιο βαθύς (AI υποβύθιση)
FREQUENCY_PAD = 82.4   # E2 - ambient pad που "χάνεται"
GAIN_DRONE = -10
GAIN_PAD = -14
GAIN_PULSES = -12

# --- Συνάρτηση sine wave με βαθύτερο fade ---
def sine_wave(freq, duration, sample_rate, volume_db=-20):
    t = np.linspace(0, duration, int(sample_rate * duration))
    amplitude = 10 ** (volume_db / 20)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    # Μεγάλο fade out
    fade_len = int(sample_rate * 4)
    if len(wave) > fade_len:
        wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    return wave

def digital_pulse(duration, sample_rate, volume_db=-10):
    """Ψηφιακός παλμός που "χάνεται" στο θόρυβο"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.random.normal(0, 0.7, len(t)) * (10 ** (volume_db / 20))
    wave *= np.sin(2 * np.pi * 2000 * t)
    # Μόνο fade out
    fade_len = int(sample_rate * 0.3)
    if len(wave) > fade_len:
        wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    return wave

# --- Δημιουργία επιπέδων ---
print("🎵 Generating ambient outro music...")

# 1. Βαθύς drone (AI υποβύθιση)
drone = sine_wave(FREQUENCY_DRONE, DURATION, SAMPLE_RATE, GAIN_DRONE)

# 2. Ambient pad (χαμηλώνει σταδιακά)
pad = sine_wave(FREQUENCY_PAD, DURATION, SAMPLE_RATE, GAIN_PAD)
# Ελαφρύ amplitude modulation για "χαμό"
pad *= np.linspace(1.0, 0.3, len(pad))

# 3. Ψηφιακοί παλμοί — σποραδικοί, ασθενείς
pulses = np.zeros(int(SAMPLE_RATE * DURATION))
pulse_duration = 0.1
pulse_times = np.random.exponential(8.0, 5)  # 5 παλμοί, τυχαία
for delay_sec in pulse_times:
    idx = int(delay_sec * SAMPLE_RATE)
    if idx + int(pulse_duration * SAMPLE_RATE) < len(pulses):
        pulse = digital_pulse(pulse_duration, SAMPLE_RATE, GAIN_PULSES)
        pulses[idx:idx+len(pulse)] += pulse[:len(pulses)-idx]

# --- Συνδυασμός ---
combined = 0.6 * drone + 0.5 * pad + 0.3 * pulses
combined /= np.max(np.abs(combined))  # normalize
combined = np.int16(combined * 32767)

# --- Αποθήκευση ---
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    temp_file = tmp.name
    wavfile.write(temp_file, SAMPLE_RATE, combined)

# Fade in/out με pydub
audio = AudioSegment.from_wav(temp_file)
audio = audio.fade_in(1000).fade_out(6000)  # μεγάλο fade out (6 δευτερόλεπτα)

audio.export(OUTPUT_FILE, format="wav")
os.unlink(temp_file)

print(f"✅ Outro theme created: {OUTPUT_FILE}")
print(f"🔊 Duration: {DURATION}s | Sample Rate: {SAMPLE_RATE} Hz")
