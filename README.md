# AI Philosophers

> Conduct AI voice debates using two LLMs running entirely on a Slackware64 Current system. No external services, no cloud, no APIs — everything is local, private, and open source.

---

## Requirements

- A modern cpu + 64 GB ram **or** NVIDIA GPU + Cuda 12+

---

## SetUp (cpu + ram)

1. Create project folder `mkdir ~/AI-DEBATES`
2. Change in project's folder `cd ~/AI-AI-DEBATES || exit 1`
3. clone llama.cpp `git clone https://github.com/ggerganov/llama.cpp`
4. Change in to start building `cd llama.cpp || exit`
```
  Before build read: `https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md`
```
5. > cmake -B build -DGGML_VULKAN=1 <br>
	> cmake --build build --config Release
 
6. Download your models from `https://huggingface.co/` (I use lm-studio so I have them in lm-studio path...) In any case here python scripts are ready for [gemma-3n-E4B-it-text-GGUF](https://huggingface.co/lmstudio-community/gemma-3n-E4B-it-text-GGUF) and [Qwen3-Coder-30B-A3B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF)
7. Change to project folder and clone this repo `cd ~/AI-DEBATES && git clone https://github.com/rizitis/AI-Philosophers.git`
8. Change in `cd AI-Philosophers || exit`
9. Install [kokoro](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) `pip install -q kokoro>=0.9.2 soundfile` 
10. To install voices for kokoro `python fones.py`
11. Install last requirements `pip install numpy scipy pydub requests`

---

## HOWTO

Every debate must have a topic, a theme, the question in other words. Scripts in AI-Philosophers are prepared for the question 
> Is randomness a form of intelligence?

You can use for the very first time exactly as is and when you understand and get used how scripts working make your own topics (your own debates)
<p>
There are 3 keys in order to run this project:

1. Your hardaware to support the heavy job or running locally llms (depeent on your system specs llama.cpp must be builded)
2. understand how scripts works...
3. Run them in correct order manually

---

### Start debate progress

**STEPS**

1. Assume 3 keys have met in your system, now you must start llama servers, in order to do this change in llama bin folder. If you used the exaclty command I used to build llama.cpp that is folder is in `~/AI-DEBATES/llama.cpp/build-cpu/bin`<br>
In this folder open a terminal (konsole) and split it in half (left/right or up/down)

In every terminal start one server:  
```
GGML_VULKAN_DISABLE=1  ./llama-server   -m ~/.cache/lm-studio/models/lmstudio-community/gemma-3n-E4B-it-text-GGUF/gemma-3n-E4B-it-Q4_K_M.gguf   --port 8081  -c 32768 -t 20   --temp 0.7
```


```
GGML_VULKAN_DISABLE=1 ./llama-server   -m /home/omen/.cache/lm-studio/models/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf   --port 8080 -c 32768 -t 20 --temp 0.7
```

#### Note for step-1:
- `-c 32768` is **very** high (the maximu) and the minimum is 8192 which is suggested.
- `-t 20` are cpu threads, edit for your needs.
- **Dont** touch `--ports` else scripts need modification. 
 
2. If you dont have lm-studio installed just create a fake dir in you home (I suggest to install it exist in SBo) <br>
`mkdir -p ~/.lmstudio/conversations/`<br>
In this folder ther will be a file auto_conversation.json which store debate dialogs. 

#### Note for step-2
Every time you create a new debate the json file must be deleted or removed from there.

3. `python debate_ai2.py` will start the debate  

#### Note for step-3
**Be careful** close all gui apps, and watch your system this operation is very heavy it **might break your hardware at all** <br>
I suggest: `watch -n 2 'sensors | grep "^Core"'`and `top` commands in separate terminal and if needed kill everything before its to late...  

4. When debate_ai2.py finish llms have created a 6 round debate<br>  
To hear it run `2tts_watcher.py`


### TIPS

- You have the ability to change voices in kokoro
```
ls -l ~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices/
``` 

- Read 000.py and 999.py these scripts create TTS for your needs. An intro.wav and outro.wav
- theme scripts are creating music inro and outro ;)
- Finally you can merge all .wav files and create a podcast! <br>
If you want to merge all wav files just run `merge_podcast.py`

This is how i create my podcast ;) 

#### 🎙️ Listen to My Podcast
[![Listen on Spotify](./The-Last_Question.png)](https://open.spotify.com/show/73zozGGkK6KNED4kj7Y11v)

---

### CREDITS

This AI podcast was created using:

- Models: Qwen3, Gemma
- TTS: Kokoro-82M by hexgrad
- Voice models: af_bella, am_adam, af_heart, etc.
- Tools: llama.cpp, Hugging Face, PyTorch, ffmpeg
- All processing done locally on Slackware64 Current.

Inspired by open-source, curiosity, and the future of AI.

---

# ⚠️ Important Disclaimer

**This software comes with NO WARRANTY, express or implied.**

**Use at your own risk.**

This program is powerful and may interact deeply with your operating system and hardware. **It has the potential to cause:**
- System instability or crashes
- Hardware stress or overheating
- Data loss or corruption
- Unauthorized changes to system settings
- High resource usage (CPU, GPU, RAM, disk)

---

## 🛑 Who Should Use This?

This tool is intended for:
- Advanced users
- Developers
- System testers
- Researchers

❌ **Not recommended** for beginners or mission-critical systems.

---

## 📝 By Using This Software, You Agree That:

1. You understand the risks involved.
2. You are using this software voluntarily and responsibly.
3. You have **backed up your important data** before running it.
4. You will test it first in a safe environment (e.g., virtual machine or non-production device).
5. The author(s) are **not liable** for any damage to your hardware, software, data, or system.

---

## 🔐 Your Responsibility

> 💡 **You assume full responsibility** for any consequences resulting from the use or misuse of this software.

The creator(s) of this project are not responsible for:
- System failures
- Hardware damage
- Data loss
- Security vulnerabilities introduced
- Any indirect or consequential losses

---

## 🛡 Recommended Precautions

✅ Always:
- Read the documentation first  
- Run in a sandbox or VM if unsure  
- Monitor system temperature and performance  
- Keep backups of critical data  
- Review source code (if open) before execution  

---

## 📄 License & Attribution

This software is provided under the [MIT License](./LICENSE) but includes **no liability** for damages. See the full license for details.

---

> 🔔 **Final Note:**  
> Just because it runs, doesn't mean it's safe.  
> If you don't know what this program does — **do not run it.**
