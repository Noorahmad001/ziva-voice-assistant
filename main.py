# ============================================================
# main.py — Ziva's Main Brain
# Run this file to start Ziva: python main.py
# ============================================================

import json
import os
import time
import ziva_config as config
from speaker import speak
from listener import listen, listen_for_wake_word
from commands import handle_command


def load_username():
    """Load saved username from user_data.json. Returns '' if not found."""
    try:
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.USER_DATA_FILE)
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                return json.load(f).get("username", "").strip()
    except Exception as e:
        print(f"[Error loading username]: {e}")
    return ""


def save_username(name):
    """Save username permanently to user_data.json."""
    try:
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.USER_DATA_FILE)
        with open(data_file, "w") as f:
            json.dump({"username": name}, f, indent=4)
        print(f"[Saved username]: {name}")
    except Exception as e:
        print(f"[Error saving username]: {e}")


def first_time_setup():
    """Ask user for their name on first run. Save and return it."""
    speak(f"Hello! I am {config.ASSISTANT_NAME}, your personal voice assistant.")
    speak("What is your name? Please say it clearly.")

    name = ""
    for attempt in range(3):
        name = listen(prompt_text="Say your name now...")
        if name:
            name = name.replace("my name is", "").replace("i am", "").replace("call me", "").strip().title()
            speak(f"Nice to meet you, {name}! I will remember your name.")
            break
        else:
            speak("I didn't catch that. Please try again." if attempt < 2 else "I'll call you Friend for now.")

    if not name:
        name = "Friend"

    save_username(name)
    return name


def wake_word_loop(username):
    """
    Main loop — runs forever.
    Listens for wake word, then listens for command, then executes it.
    Never crashes — all errors are caught and recovered.
    """
    print(f"\n{'='*45}")
    print(f"  Ziva is ready! Say 'Ziva' to wake her up.")
    print(f"  Press Ctrl+C to stop.")
    print(f"{'='*45}\n")

    while True:
        try:
            # Step 1: Listen for wake word (may also capture inline command)
            wake_detected, inline_command = listen_for_wake_word()
            if wake_detected:
                print("[Wake word detected!]")

                if inline_command:
                    # User said wake word + command together (e.g. "Ziva open youtube")
                    print(f"[Inline command]: {inline_command}")
                    speak(f"Sure {username}!")
                    command = inline_command
                else:
                    # Step 2: Respond and wait for separate command
                    speak(f"Yes {username}, tell me.")
                    time.sleep(0.5)

                    # Step 3: Listen for command
                    command = listen(prompt_text="Listening for your command...")

                # Step 4: Execute command
                if command:
                    keep_running = handle_command(command, username)
                    if not keep_running:
                        break
                else:
                    speak("I didn't catch a command. Say Ziva whenever you need me!")

        except KeyboardInterrupt:
            speak(f"Shutting down. Goodbye {username}!")
            print("\n[Ziva stopped.]")
            break

        except Exception as e:
            # Never let Ziva crash — just log and continue
            print(f"[Error recovered]: {e}")
            time.sleep(0.5)


def main():
    print("=" * 45)
    print("       ZIVA VOICE ASSISTANT")
    print("=" * 45)

    username = load_username()

    if not username:
        username = first_time_setup()
    else:
        speak(f"Welcome back, {username}! Ziva is online and ready.")

    wake_word_loop(username)


if __name__ == "__main__":
    main()