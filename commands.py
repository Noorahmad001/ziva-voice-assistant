# ============================================================
# commands.py — Ziva's Command Handler
# Add new websites: add a line to WEBSITES dict
# Add new apps: add a line to APPS dict
# Add new commands: add an elif block in handle_command()
# ============================================================

import webbrowser
import subprocess
import os
import datetime
import random
import urllib.request
import urllib.parse
import json
from speaker import speak


# -------------------------------------------------------
# WEBSITES — what user says : URL to open
# -------------------------------------------------------
WEBSITES = {
    "youtube":       "https://www.youtube.com",
    "google":        "https://www.google.com",
    "github":        "https://www.github.com",
    "whatsapp":      "https://web.whatsapp.com",
    "gmail":         "https://mail.google.com",
    "instagram":     "https://www.instagram.com",
    "twitter":       "https://www.twitter.com",
    "facebook":      "https://www.facebook.com",
    "netflix":       "https://www.netflix.com",
    "reddit":        "https://www.reddit.com",
    "linkedin":      "https://www.linkedin.com",
    "amazon":        "https://www.amazon.com",
    "stackoverflow": "https://stackoverflow.com",
    "chatgpt":       "https://chat.openai.com",
    "spotify":       "https://open.spotify.com",
}

# -------------------------------------------------------
# APPS — what user says : windows executable
# -------------------------------------------------------
APPS = {
    "notepad":       "notepad.exe",
    "calculator":    "calc.exe",
    "paint":         "mspaint.exe",
    "explorer":      "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager":  "taskmgr.exe",
    "word":          "winword",
    "excel":         "excel",
    "powerpoint":    "powerpnt",
}


# -------------------------------------------------------
# CHROME
# -------------------------------------------------------
def open_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            speak("Opening Chrome.")
            return
    speak("I couldn't find Chrome installed on your computer.")


# -------------------------------------------------------
# SEARCH
# -------------------------------------------------------
def search_web(command):
    query = ""
    if "search for" in command:
        query = command.split("search for", 1)[1].strip()
    elif "search" in command:
        query = command.split("search", 1)[1].strip()
    if query:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Searching Google for {query}.")
    else:
        speak("What would you like me to search for?")


# -------------------------------------------------------
# TIME & DATE
# -------------------------------------------------------
def tell_time():
    now = datetime.datetime.now()
    speak(f"The current time is {now.strftime('%I:%M %p')}.")

def tell_date():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A, %B %d, %Y')}.")


# -------------------------------------------------------
# NEWS — fetches top headlines using RSS (no API key needed)
# -------------------------------------------------------
def tell_news():
    """
    Fetches top 5 news headlines from Google News RSS feed.
    No API key needed — uses free RSS feed.
    Reads headlines out loud using speak().
    """
    try:
        speak("Let me get the latest news headlines for you.")

        # Google News RSS — free, no key needed
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=8)
        content = response.read().decode("utf-8")

        # Parse headlines from RSS XML manually (no extra library needed)
        headlines = []
        items = content.split("<item>")
        for item in items[1:6]:  # Get first 5 news items
            if "<title>" in item:
                title = item.split("<title>")[1].split("</title>")[0]
                # Clean up CDATA wrapper if present
                title = title.replace("<![CDATA[", "").replace("]]>", "").strip()
                # Remove source name at end (e.g. "- BBC News")
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0].strip()
                if title:
                    headlines.append(title)

        if headlines:
            speak(f"Here are the top {len(headlines)} news headlines.")
            for i, headline in enumerate(headlines, 1):
                speak(f"Headline {i}: {headline}")
        else:
            speak("I couldn't find any headlines right now. Please check your internet connection.")

    except Exception as e:
        print(f"[News Error]: {e}")
        speak("Sorry, I couldn't fetch the news right now. Please check your internet connection.")


# -------------------------------------------------------
# WEATHER — fetches real weather using wttr.in (no API key needed)
# -------------------------------------------------------
def tell_weather(command):
    """
    Gets real weather for any city using wttr.in — completely free, no API key.
    Tells temperature, condition (sunny/cloudy/rainy) out loud.
    """
    # Extract city name from command
    city = ""
    for keyword in ["weather in", "weather of", "weather for", "weather"]:
        if keyword in command:
            city = command.split(keyword, 1)[1].strip()
            break

    # Clean up common words that follow
    for word in ["today", "now", "currently", "please", "tell me"]:
        city = city.replace(word, "").strip()

    if not city:
        speak("Which city would you like the weather for? Please say the city name.")
        return

    try:
        speak(f"Getting weather for {city}, please wait.")

        # wttr.in returns JSON weather data — free, no API key needed
        city_encoded = urllib.parse.quote(city)
        url = f"https://wttr.in/{city_encoded}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=8)
        data = json.loads(response.read().decode("utf-8"))

        # Extract weather details from JSON
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]
        wind_kmph = current["windspeedKmph"]

        # Build a natural spoken response
        weather_report = (
            f"The weather in {city} is currently {description}. "
            f"Temperature is {temp_c} degrees Celsius, "
            f"feels like {feels_like} degrees. "
            f"Humidity is {humidity} percent "
            f"and wind speed is {wind_kmph} kilometres per hour."
        )

        print(f"[Weather]: {weather_report}")
        speak(weather_report)

    except urllib.error.URLError:
        speak("I couldn't connect to the weather service. Please check your internet.")
    except (KeyError, IndexError):
        speak(f"I couldn't find weather data for {city}. Please check the city name.")
    except Exception as e:
        print(f"[Weather Error]: {e}")
        speak(f"Sorry, I couldn't get the weather for {city} right now.")


# -------------------------------------------------------
# MAIN COMMAND PROCESSOR
# -------------------------------------------------------
def handle_command(command, username):
    """
    Receives the recognized voice command and runs the right action.
    Returns True to keep Ziva running, False to stop her.
    """
    if not command:
        speak("I didn't catch that. Please try again.")
        return True

    print(f"[Command]: '{command}'")

    # ---- GREETINGS ----
    if any(w in command for w in ["hello", "hi", "hey"]):
        speak(f"Hello {username}! How can I help you?")

    # ---- TIME ----
    elif "time" in command:
        tell_time()

    # ---- DATE ----
    elif any(w in command for w in ["date", "today", "what day"]):
        tell_date()

    # ---- NEWS ----
    elif any(w in command for w in ["news", "headlines", "what's happening", "latest news"]):
        tell_news()

    # ---- WEATHER ----
    elif "weather" in command:
        tell_weather(command)

    # ---- SEARCH ----
    elif "search" in command:
        search_web(command)

    # ---- CHROME ----
    elif "chrome" in command:
        open_chrome()

    # ---- WEBSITES ----
    elif any(site in command for site in WEBSITES):
        for site, url in WEBSITES.items():
            if site in command:
                speak(f"Opening {site}.")
                webbrowser.open(url)
                break

    # ---- APPS ----
    elif any(app in command for app in APPS):
        for app, cmd in APPS.items():
            if app in command:
                speak(f"Opening {app}.")
                try:
                    subprocess.Popen([cmd])
                except Exception:
                    try:
                        os.startfile(cmd)
                    except Exception as e:
                        speak(f"Sorry, I couldn't open {app}.")
                        print(f"[Error]: {e}")
                break

    # ---- JOKES ----
    elif "joke" in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What do you call a fish without eyes? A fsh!",
            "Why did the Python programmer wear glasses? Because they couldn't C sharp!",
        ]
        joke = random.choice(jokes)
        speak(joke)

    # ---- WHO ARE YOU ----
    elif any(w in command for w in ["who are you", "your name", "what are you"]):
        speak(f"I am Ziva, your personal voice assistant. Always here for you, {username}!")

    # ---- STOP / EXIT ----
    elif any(w in command for w in ["stop", "exit", "quit", "bye", "goodbye", "sleep", "shutdown"]):
        speak(f"Goodbye {username}! I'll be here whenever you need me.")
        return False

    # ---- UNKNOWN ----
    else:
        speak(f"Sorry {username}, I don't know that command yet. Try saying open YouTube, get the news, or weather in Delhi.")
        print(f"[No match found for]: '{command}'")

    return True