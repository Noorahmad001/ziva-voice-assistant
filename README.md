# Ziva — Personal Voice Assistant

Ziva is a Python-based personal voice assistant built for Windows. It activates on a
wake word, listens to voice commands, and responds with a female voice. It can open
websites, launch applications, search the web, read live news headlines, and report
real-time weather for any city — all through natural speech.

---

## Overview

This project was built entirely from scratch as a personal productivity tool and
learning project. The goal was to create something that works like Siri or Alexa
but runs locally on a Windows laptop, requires no paid APIs, and can be packaged
into a standalone executable that starts automatically when the computer boots.

The assistant remembers the user's name on first run and uses it in every
conversation. It runs silently in the background and is always ready the moment
you say its name.

---

## Features

- Wake word activation — say "Ziva" to activate, no button or shortcut needed
- Personalized responses — remembers your name permanently across sessions
- Female voice output using Microsoft Zira (Windows built-in)
- Opens websites by voice command
- Launches Windows applications by voice command
- Web search via Google
- Live news — reads top 5 headlines from Google News out loud
- Live weather — temperature, humidity, wind speed and conditions for any city
- Tells current time and date
- Tells jokes on request
- Runs continuously in the background
- Auto-starts when Windows boots (via startup folder or Task Scheduler)
- Can be packaged as a standalone .exe file using PyInstaller

---

## Project Structure

```
ZivaAssistant/
├── main.py              Entry point — connects all modules and runs the loop
├── listener.py          Microphone capture and Google Speech recognition
├── speaker.py           Text-to-speech engine using pyttsx3
├── commands.py          All voice command logic and actions
├── ziva_config.py       Global settings — edit this to customize Ziva
├── user_data.json       Stores the user's name permanently
├── build_exe.bat        One-click script to build Ziva.exe
├── add_to_startup.bat   One-click script to add Ziva to Windows startup
├── requirements.txt     All Python dependencies
└── README.md            Project documentation
```

---

## Tech Stack

| Component            | Library / Service         | Reason                                      |
|----------------------|---------------------------|---------------------------------------------|
| Microphone capture   | sounddevice + numpy       | Works on Python 3.14, no build errors       |
| Speech recognition   | SpeechRecognition (Google)| Accurate, free, no API key required         |
| Text to speech       | pyttsx3                   | Offline, uses Windows built-in voices       |
| News headlines       | Google News RSS           | Free, no API key, always up to date         |
| Weather data         | wttr.in                   | Free, no API key, returns structured JSON   |
| Web automation       | webbrowser + subprocess   | Built into Python, no dependencies          |
| EXE packaging        | PyInstaller               | Converts project to standalone executable   |

---

## Installation

### Requirements

- Windows 10 or Windows 11
- Python 3.10, 3.11, 3.12, or 3.13
- Internet connection (required for speech recognition, news, and weather)

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ZivaAssistant.git
cd ZivaAssistant
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run Ziva

```bash
python main.py
```

On first run, Ziva will ask for your name and save it. On every run after that,
she will greet you by name and go straight to listening.

---

## Voice Commands

```
Wake word          "Ziva"
Open websites      "open YouTube"
                   "open WhatsApp"
                   "open Gmail"
                   "open Instagram"
                   "open GitHub"
                   "open Netflix"
                   "open Spotify"
                   "open Reddit"
                   "open LinkedIn"
Open applications  "open Notepad"
                   "open Calculator"
                   "open Chrome"
                   "open Paint"
                   "open File Explorer"
                   "open Task Manager"
Web search         "search for Python tutorials"
                   "search for latest iPhone"
Weather            "weather in Delhi"
                   "weather in London"
                   "weather in New York"
News               "get me the news"
                   "latest headlines"
                   "what is happening"
Time and date      "what time is it"
                   "what is today's date"
Jokes              "tell me a joke"
Identity           "who are you"
Stop               "goodbye"  /  "stop"  /  "exit"
```

---

## Building the EXE

To convert Ziva into a standalone executable that runs without Python installed,
double-click `build_exe.bat` from inside the project folder.

The script will:
1. Install PyInstaller automatically if not already present
2. Clean any previous build files
3. Build a single-file executable
4. Place the output at `dist/Ziva.exe`

The resulting `Ziva.exe` can be copied to any Windows computer and run directly
without requiring Python, VS Code, or any other tool to be installed.

---

## Auto-Start on Boot

### Method 1 — Automatic (Recommended)

After building the EXE, double-click `add_to_startup.bat`.

Ziva will be copied to the Windows Startup folder and will launch automatically
every time the computer starts — silently, in the background.

To remove Ziva from startup:
1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Delete `Ziva.exe` from the folder that opens

### Method 2 — Task Scheduler (More Control)

1. Open Task Scheduler from the Start Menu
2. Click "Create Basic Task"
3. Name: Ziva Assistant
4. Trigger: When the computer starts
5. Action: Start a program
6. Browse to `dist/Ziva.exe`
7. Click Finish

---

## Adding New Commands

**Add a new website**

Open `commands.py`, find the `WEBSITES` dictionary, and add one line:

```python
"canva": "https://www.canva.com",
```

**Add a new application**

Find the `APPS` dictionary and add one line:

```python
"vlc": "vlc.exe",
```

**Add a fully custom command**

Find the `handle_command()` function and add a new elif block:

```python
elif "battery" in command:
    speak("Checking your battery level.")
    os.system("powercfg /batteryreport")
```

No other file needs to be changed.

---

## Configuration

All settings are stored in `ziva_config.py`. Edit this file to customize Ziva.

```python
VOICE_RATE = 170          # Speaking speed — higher is faster
VOICE_VOLUME = 1.0        # Volume from 0.0 to 1.0
MIC_ENERGY_THRESHOLD = 300  # Microphone sensitivity — lower is more sensitive
MIC_PHRASE_LIMIT = 8      # Max seconds to record a single command
WAKE_WORD = "ziva"        # The word that activates Ziva
```

---

## Troubleshooting

| Problem                        | Solution                                                        |
|-------------------------------|------------------------------------------------------------------|
| Ziva does not wake up          | Ensure internet is connected — Google Speech API requires it    |
| Voice is male                  | Go to Settings, Speech, and install Microsoft Zira voice        |
| App does not open              | Verify the executable name in the APPS dictionary               |
| Weather city not found         | Say the full city name clearly and check spelling               |
| sounddevice install error      | Run `pip install sounddevice numpy` separately                  |
| EXE does not start             | Run from Command Prompt first to see the error message          |
| Mic too sensitive or not hearing| Adjust MIC_ENERGY_THRESHOLD in ziva_config.py                  |

---
## License

MIT License. Free to use, modify, and distribute.

---

## Author

Your Name
GitHub: https://github.com/YOUR_USERNAME
LinkedIn: https://linkedin.com/in/YOUR_USERNAME