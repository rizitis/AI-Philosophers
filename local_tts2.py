#!/usr/bin/env python3
# local_tts.py
import os
import platform
import re
from kokoro import KPipeline
import soundfile as sf

# --- Υποστηριζόμενες γλώσσες ---
SUPPORTED_LANGS = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
}

# --- Αρχικοποίηση pipelines ---
PIPELINES = {
    lang: KPipeline(lang_code=code, repo_id="hexgrad/Kokoro-82M")
    for lang, code in [
        ("en", "a"),
        ("es", "e"),
        ("fr", "f"),
        ("de", "b"),
        ("it", "i"),
        ("pt", "p")
    ]
}

# --- Αποθήκευση αρχείων ---
WAV_COUNTER = 0

def get_next_filename():
    global WAV_COUNTER
    filename = f"tts_output_{WAV_COUNTER}.wav"
    WAV_COUNTER += 1
    return filename

# --- Αναπαραγωγή ήχου (cross-platform) ---
def play_audio(filename):
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return

    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(filename)
        elif system == "Darwin":  # macOS
            os.system(f"afplay '{filename}'")
        else:  # Linux
            if os.system(f"aplay -q '{filename}'") != 0:
                if os.system(f"ffplay -nodisp -autoexit -loglevel quiet '{filename}'") != 0:
                    print(f"🔊 Audio ready: {filename}")
    except Exception as e:
        print(f"❌ Failed to play {filename}: {e}")

# --- Κύρια συνάρτηση TTS ---
def text_to_speech(text, lang="en", voice="af_heart"):
    if lang not in PIPELINES:
        print(f"⚠️ Language '{lang}' not supported. Using English.")
        lang = "en"

    pipeline = PIPELINES[lang]

    # 🔽 Καθαρισμός: αφαίρεση asterisks
    text = text.replace("*", "")

    # Καθαρισμός από tags για την ομιλία (αλλά μετά την ανίχνευση)
    clean_text = re.sub(r"\[QWEN3\]|\[GEMMA\]", "", text)
    clean_text = re.sub(r"<\|.*?\|>", "", clean_text)
    clean_text = re.sub(r"(\s*\.\.\.\s*)+", " ", clean_text)
    clean_text = re.sub(r"(<\|start\|>.*?<\|message\|>)", "", clean_text)
    clean_text = re.sub(r"(\s)+", " ", clean_text)
    clean_text = clean_text.strip()

    if not clean_text:
        print("🔇 Empty text after cleaning — skipping TTS.")
        return

    print(f"🗣️ Using voice: {voice} | Text: {clean_text[:60]}...")

    try:
        generator = pipeline(clean_text, voice=voice, speed=1.0, split_pattern=r"\n+")
        for i, (gs, ps, audio) in enumerate(generator):
            filename = get_next_filename()
            sf.write(filename, audio, 24000)
            print(f"💾 Saved: {filename}")
            play_audio(filename)

            #if os.path.exists(filename):
             #   os.remove(filename)
              #  print(f"🗑️ Deleted: {filename}")
    except Exception as e:
        print(f"❌ TTS failed for voice '{voice}': {e}")

# --- Κύρια συνάρτηση για απάντηση AI ---
def speak_gpt_response(text, lang="en", voice="af_heart"):
    # 🔍 Ανίχνευση φωνής ΠΡΙΝ το καθάρισμα
    if "[QWEN3]" in text.upper():
        used_voice = "bm_daniel"
        prefix = "Qwen3 says: "
    elif "[GEMMA]" in text.upper():
        used_voice = "af_bella"
        prefix = "Gemma says: "
    else:
        used_voice = "af_heart"
        prefix = "AI says: "

    # Προσθήκη πρόθεματος
    final_text = prefix + text

    # Κλήση TTS
    text_to_speech(final_text, lang=lang, voice=used_voice)

    # --- Επιλογή γλώσσας ---
def choose_language(current_lang="en"):
    print("🌍 Available languages:")
    for code, name in SUPPORTED_LANGS.items():
        print(f"  {code}: {name}")
    lang = input(f"🌐 Select language code (current '{current_lang}'): ").strip().lower()
    if lang not in SUPPORTED_LANGS:
        print("❌ Invalid choice. Keeping current language.")
        return current_lang
    print(f"✅ Language set to: {SUPPORTED_LANGS[lang]}")
    return lang

# --- Παράδειγμα ---
if __name__ == "__main__":
    lang = "en"
    sample_text = "[QWEN3] AI is not replacing humans — it's empowering them."
    speak_gpt_response(sample_text, lang=lang)
