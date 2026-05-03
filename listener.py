import io
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import ziva_config as config

SAMPLE_RATE = 16000
CHANNELS = 1
recognizer = sr.Recognizer()

# Google sometimes mishears "Ziva" as these words — all accepted as wake word
WAKE_VARIANTS = [
    "ziva", "jeeva", "jiva", "shiva", "siva", "seva",
    "zeeva", "diva", "viva", "zia", "eva", "hiva",
    "geeva", "leeva", "reeva", "reva", "rewa", "heeva"
]


def _to_audio(recording):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())
    buf.seek(0)
    with sr.AudioFile(buf) as source:
        return recognizer.record(source)


def _has_speech(recording):
    """Check if recording contains speech using windowed energy detection.

    Uses 0.5-second sliding windows so even brief speech in a long
    recording is detected (the old overall-mean approach missed this).
    """
    window_size = int(0.5 * SAMPLE_RATE)  # 0.5 second windows
    step = window_size // 2
    flat = recording.flatten()

    for i in range(0, len(flat) - window_size + 1, step):
        window = flat[i:i + window_size]
        if np.abs(window).mean() > config.MIC_ENERGY_THRESHOLD:
            return True

    # Fallback: check if peak amplitude is well above threshold
    if np.abs(flat).max() > config.MIC_ENERGY_THRESHOLD * 4:
        return True

    return False


def _recognize(audio):
    try:
        return recognizer.recognize_google(audio, language=config.RECOGNITION_LANGUAGE).lower().strip()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("[Listener]: No internet.")
        return ""


def _is_wake_word(text):
    """Check if text contains any known variant of wake word Ziva."""
    if not text:
        return False
    words = text.split()
    for word in words:
        # Check exact match against all variants
        if word in WAKE_VARIANTS:
            print(f"[Wake matched]: '{word}'")
            return True
        # Check if word starts with ji, je, zi, ze, sh (catches new variants)
        if word.startswith(("zi", "ze", "ji", "je", "sh", "si", "se")):
            print(f"[Wake prefix matched]: '{word}'")
            return True
    return False


def _extract_command_after_wake(text):
    """Extract any command that follows the wake word in the same utterance.

    E.g. 'ziva open youtube' → 'open youtube'
         'hey jeeva'         → ''
    """
    if not text:
        return ""
    words = text.split()
    for i, word in enumerate(words):
        if word in WAKE_VARIANTS:
            return " ".join(words[i + 1:]).strip()
        if word.startswith(("zi", "ze", "ji", "je", "sh", "si", "se")):
            return " ".join(words[i + 1:]).strip()
    return ""


def listen(prompt_text=None, timeout=None, phrase_limit=None):
    """Record mic and return recognized text. Called after wake word."""
    if phrase_limit is None:
        phrase_limit = config.MIC_PHRASE_LIMIT
    if prompt_text:
        print(f"[Listening]: {prompt_text}")
    try:
        recording = sd.rec(
            int(phrase_limit * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )
        sd.wait()
        if not _has_speech(recording):
            print("[Listener]: Silence, skipping.")
            return ""
        text = _recognize(_to_audio(recording))
        if text:
            print(f"[You said]: {text}")
        return text
    except Exception as e:
        print(f"[Listener Error]: {e}")
        return ""


def listen_for_wake_word():
    """Listen for 3 seconds. Return (True, command_text) or (False, '').

    If user says 'Ziva open youtube', returns (True, 'open youtube').
    If user says just 'Ziva', returns (True, '').
    If no wake word, returns (False, '').
    """
    try:
        recording = sd.rec(
            int(3 * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )
        sd.wait()

        if not _has_speech(recording):
            return False, ""

        text = _recognize(_to_audio(recording))

        if text:
            print(f"[Background heard]: {text}")

        if _is_wake_word(text):
            inline_command = _extract_command_after_wake(text)
            return True, inline_command

        return False, ""

    except Exception as e:
        print(f"[Wake Error]: {e}")
        return False, ""