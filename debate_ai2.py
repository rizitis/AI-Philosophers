#!/usr/bin/env python3
import json
import time
import requests
from pathlib import Path

# --- Ρυθμίσεις ---
CONVO_FILE = Path.home() / ".lmstudio/conversations/auto_conversation.json"

# 🔹 Δύο llama.cpp servers
QWEN_API = "http://localhost:8080"
GEMMA_API = "http://localhost:8081"

# --- Θέμα ---
TOPIC = "Is modern systemd linux systems better nowdays? Or linux becaming more close to systemd or nothing?"

# --- Προτροπές ---
POSITION_QWEN = (
    "You are IN FAVOR: systemd is better: modern and make things easy for users."
)

POSITION_GEMMA = (
    "You are AGAINST: systemd might be modern but is ts on wrong path."
)

# --- Κλήση API ---
def query_model(api_host, prompt, max_tokens=3000, temperature=0.7):
    try:
        print(f"⏳ Sending request to {api_host}...")
        response = requests.post(
            f"{api_host}/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stop": ["<think>", "</think>", "User:", "Assistant:"]
            },
            timeout=300  # 5 λεπτά — αφήνουμε χρόνο για σκέψη
        )
        if response.status_code == 200:
            raw = response.json()["choices"][0]["message"]["content"].strip()

            # Καθαρισμός tags
            cleaned = raw.replace("<think>", "").replace("</think>", "")
            cleaned = cleaned.replace("<|start|>assistant<|channel|>final<|message|>", "")
            cleaned = cleaned.replace("<|end|>", "").replace("<|return|>", "")
            cleaned = cleaned.strip()

            return cleaned if cleaned else "No meaningful response."
        else:
            print(f"[API] Error {response.status_code}: {response.text}")
            return "No response."
    except requests.exceptions.Timeout:
        print("[API] Request timed out — model is still thinking...")
        return "My thoughts were interrupted. Let me continue next time."
    except Exception as e:
        print(f"[Request error] {e}")
        return "Request failed."

# --- Αποθήκευση σε JSON ---
def append_message(role, content, speaker=""):
    tag = f"[{speaker.upper()}] "
    full_content = tag + content

    messages = []
    if CONVO_FILE.exists():
        try:
            data = json.loads(CONVO_FILE.read_text(encoding="utf-8"))
            messages = data.get("messages", [])
        except Exception as e:
            print(f"[JSON] Failed to read: {e}")

    messages.append({
        "id": f"msg_{int(time.time())}_{speaker.lower()}",
        "role": role,
        "versions": [{
            "id": f"v_{len(messages)}",
            "role": role,
            "content": [{"type": "text", "text": full_content}]
        }]
    })

    data = {
        "id": "ai-debate-llama-cpp",
        "title": "Qwen3 vs Gemma: Full Context Debate",
        "messages": messages
    }
    try:
        CONVO_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📝 Message saved: {len(full_content)} chars")
    except Exception as e:
        print(f"[JSON] Failed to write: {e}")

# --- Κύριος Βρόχος ---
def main():
    print("🔥 Starting AI Debate: Qwen3 vs Gemma (Full Context)")
    print(f"Topic: {TOPIC}\n")
    print("💡 Models will see the FULL conversation history. This enables real dialogue.\n")

    # Αρχική πρόταση
    conversation_history = f"Topic: {TOPIC}\n"
    conversation_history += f"Qwen3 (IN FAVOR): {POSITION_QWEN}\n"
    conversation_history += f"Gemma (AGAINST): {POSITION_GEMMA}\n\n"

    current_speaker = "qwen"
    turn = 1

    while turn <= 6:
        if current_speaker == "qwen":
            print(f"\n🧠 [Turn {turn}] Qwen3 is thinking (IN FAVOR)...")
            prompt = f"""
{conversation_history}
Now, as Qwen3 (IN FAVOR), respond to the discussion so far. Build on or challenge previous points. Be uncensored, be insightful.
"""
            response = query_model(QWEN_API, prompt, max_tokens=550, temperature=0.72)
            print(f"💬 Qwen3 says: {response[:120]}...")
            append_message("assistant", response, speaker="Qwen3")

            # Πρόσθεσε στο context
            conversation_history += f"Turn {turn}: Qwen3: {response}\n"
            current_speaker = "gemma"

        else:
            print(f"\n🧠 [Turn {turn}] Gemma is thinking (AGAINST)...")
            prompt = f"""
{conversation_history}
Now, as Gemma (AGAINST), respond to the discussion so far. Address specific points made by Qwen3. Be uncensored, be insightful.
"""
            response = query_model(GEMMA_API, prompt, max_tokens=500, temperature=0.7)
            print(f"💬 Gemma says: {response[:120]}...")
            append_message("assistant", response, speaker="Gemma")

            # Πρόσθεσε στο context
            conversation_history += f"Turn {turn}: Gemma: {response}\n"
            current_speaker = "qwen"
            turn += 1  # Μόνο όταν τελειώσει ο γύρος

        print(f"⏳ Taking a break before next turn...\n")
        time.sleep(3)

    closing = "The debate has ended. The future of creativity remains an open question."
    append_message("system", closing)
    print("\n🏁 Debate finished. TTS will now read the final message.")
    print(f"📄 Full transcript: {CONVO_FILE}")

if __name__ == "__main__":
    main()
