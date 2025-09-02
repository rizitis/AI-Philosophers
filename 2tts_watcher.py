#!/usr/bin/env python3
import time
import json
from pathlib import Path
import sys

# Βεβαιώσου ότι μπορεί να βρει το local_tts2
sys.path.insert(0, ".")

try:
    from local_tts2 import speak_gpt_response, choose_language
except ImportError:
    print("[TTS] Error: local_tts2.py not found or has errors.")
    sys.exit(1)

# --- Ρυθμίσεις ---
CONVO_DIR = Path.home() / ".lmstudio/conversations"
CONVO_FILE = CONVO_DIR / "auto_conversation.json"  # Το ακριβές αρχείο που χρησιμοποιείς

current_lang = "en"
spoken_messages = set()

# --- Επιλογή φωνής ανά μοντέλο ---
def get_voice_for_text(text):
    if "[QWEN3]" in text.upper():
        return "am_michael"   # ή όποια φωνή θέλεις
    elif "[GEMMA]" in text.upper():
        return "af_sunny"   # ή άλλη
    return "af_heart"  # default

# --- Καθαρισμός ανεπιθύμητων tags ---
def clean_text(text):
    # Αφαίρεση μόνο των εσωτερικών tags, όχι των [QWEN3]/[GEMMA]
    text = text.replace("think", "").replace("thik", "")  # από το <think>
    text = text.replace("<|start|>assistant<|channel|>final<|message|>", "")
    text = text.replace("<|end|>", "").replace("<|return|>", "")
    text = text.strip()
    return text

# --- Βρες το αρχείο και διάβασε τα νέα μηνύματα ---
def get_new_messages():
    if not CONVO_FILE.exists():
        return []

    try:
        data = json.loads(CONVO_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[TTS] Failed to read JSON: {e}")
        return []

    new_texts = []

    for msg in data.get("messages", []):
        role = msg.get("role")
        if role != "assistant":
            continue  # Μόνο απαντήσεις

        for version in msg.get("versions", []):
            for content in version.get("content", []):
                if content.get("type") == "text":
                    raw_text = content.get("text", "").strip()
                    if not raw_text or raw_text in spoken_messages:
                        continue

                    cleaned = clean_text(raw_text)
                    if cleaned:
                        new_texts.append({
                            "text": cleaned,
                            "raw": raw_text,
                            "voice": get_voice_for_text(raw_text)
                        })
                        spoken_messages.add(raw_text)  # αποφυγή διπλότυπων

    return new_texts

# --- Κύριος watcher ---
def watcher():
    print(f"[TTS] Watching: {CONVO_FILE}")
    if not CONVO_DIR.exists():
        print(f"[TTS] Directory not found: {CONVO_DIR}")
        return

    while True:
        try:
            messages = get_new_messages()
            for msg in messages:
                print(f"[TTS] Speaking: {msg['text'][:80]}...")
                speak_gpt_response(msg["text"], lang=current_lang, voice=msg["voice"])
            time.sleep(0.7)  # γρήγορο poll

        except KeyboardInterrupt:
            print("\n[TTS] Exiting gracefully...")
            break
        except Exception as e:
            print(f"[TTS] Unexpected error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    watcher()
