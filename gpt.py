"""
Jarvis Bot - AI-Powered Voice/Text Assistant (ChatGPT Edition)
Modules: pyautogui, beautifulsoup4, selenium, openai, pyttsx3, SpeechRecognition

Install dependencies:
    pip install pyautogui beautifulsoup4 selenium pyttsx3 SpeechRecognition
    pip install requests openai python-dotenv webdriver-manager

Folder structure:
    jarvis/
    ├── jarvis_bot.py
    └── .env              ← create this file with: OPENAI_API_KEY=your-key-here
"""

import os
import time
import subprocess
import requests
import pyttsx3
import pyautogui
import speech_recognition as sr
import openai
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Load API Key from .env ──────────────────────────────────────────
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError(
        "\n[ERROR] OPENAI_API_KEY not found!\n"
        "Create a .env file in the same folder as this script:\n"
        "  OPENAI_API_KEY=your-key-here\n"
        "Get a key at: https://platform.openai.com/api-keys"
    )

# ── OpenAI Setup ────────────────────────────────────────────────────
# Initialize the OpenAI Client
client = OpenAI(api_key=api_key)

# OpenAI requires us to maintain the conversation history manually
conversation_history = [
    {
        "role": "system", 
        "content": (
            "You are Jarvis, a smart and helpful AI assistant like the one in Iron Man. "
            "You are concise, confident, and slightly formal. "
            "Keep responses under 3 sentences unless the user asks for detail."
        )
    }
]

# We will use gpt-4o-mini as it is fast, highly capable, and cost-effective
MODEL_NAME = "gpt-4o-mini"


# ── Voice Engine Setup ──────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

def speak(text: str):
    """Speak and print Jarvis's response."""
    print(f"\nJarvis: {text}")
    engine.say(text)
    engine.runAndWait()


# ── Speech Recognition ──────────────────────────────────────────────
recognizer = sr.Recognizer()

def listen() -> str:
    """Listen via microphone and return the spoken text."""
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"You: {command}")
            return command
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("I didn't catch that. Please repeat.")
            return ""
        except Exception:
            return input("Type your command: ").lower().strip()


# ── ChatGPT Chat ────────────────────────────────────────────────────
def ask_chatgpt(user_message: str) -> str:
    """Send a message to ChatGPT and update conversation memory."""
    # Add the user's message to our history
    conversation_history.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation_history
        )
        reply = response.choices[0].message.content.strip()
        
        # Add the assistant's reply to our history so it remembers context
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
        
    except openai.RateLimitError:
        # Gracefully handle the 429 Quota Error for OpenAI
        # Note: You must fund your OpenAI developer account to use the API
        return "Sir, my cloud connection is currently throttled due to rate limits or billing. Please check your OpenAI account."
    except Exception as e:
        return f"System error: {str(e)}"

def classify_command(command: str) -> str:
    """
    Use ChatGPT to classify intent without adding it to the main conversation history.
    """
    prompt = (
        f"Classify this command into exactly one category.\n"
        f"Command: \"{command}\"\n"
        f"Categories: weather, news, wiki, search, youtube, "
        f"screenshot, open_app, type_text, exit, chat\n"
        f"Reply with only the category word, nothing else."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0 # Low temperature for more deterministic output
        )
        return response.choices[0].message.content.strip().lower()
    except Exception:
        # If rate limited during classification, default to chat
        return "chat"


# ── PyAutoGUI Features ──────────────────────────────────────────────
def open_application(app_name: str):
    speak(f"Opening {app_name}")
    apps = {
        "notepad":    "notepad.exe",
        "calculator": "calc.exe",
        "paint":      "mspaint.exe",
        "explorer":   "explorer.exe",
    }
    key = app_name.lower()
    if key in apps:
        subprocess.Popen(apps[key])
    else:
        pyautogui.hotkey("win")
        time.sleep(0.8)
        pyautogui.typewrite(app_name, interval=0.05)
        time.sleep(0.5)
        pyautogui.press("enter")

def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")

def type_text(text: str):
    speak(f"Typing: {text}")
    time.sleep(0.5)
    pyautogui.typewrite(text, interval=0.05)
#
#
# ── BeautifulSoup Features ──────────────────────────────────────────
def get_weather(city: str = "Chennai"):
    speak(f"Checking weather for {city}")
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        weather = requests.get(url, timeout=5).text.strip()
        speak(f"The weather in {city} is {weather}")
    except Exception:
        speak("Could not fetch weather right now.")

def get_news(topic: str = "technology"):
    speak(f"Fetching latest {topic} news")
    try:
        url = f"https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en"
        soup = BeautifulSoup(requests.get(url, timeout=6).content, "xml")
        headlines = [item.find("title").text for item in soup.find_all("item")[:3]]
        for i, h in enumerate(headlines, 1):
            speak(f"Headline {i}: {h}")
    except Exception:
        speak("Could not fetch news right now.")

def scrape_wikipedia(query: str):
    speak(f"Searching Wikipedia for {query}")
    try:
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        soup = BeautifulSoup(requests.get(url, timeout=6).text, "html.parser")
        for p in soup.select("div.mw-parser-output > p"):
            text = p.get_text().strip()
            if len(text) > 60:
                speak(text[:300])
                return
    except Exception:
        speak("Could not fetch Wikipedia data.")


# ── Selenium Features ───────────────────────────────────────────────
def get_driver(headless: bool = False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def google_search(query: str):
    speak(f"Searching Google for {query}")
    driver = get_driver(headless=True)
    try:
        driver.get("https://www.google.com")
        box = driver.find_element(By.NAME, "q")
        box.send_keys(query + Keys.RETURN)
        time.sleep(2)
        results = driver.find_elements(By.CSS_SELECTOR, "h3")[:3]
        for r in results:
            if r.text:
                speak(r.text)
    except Exception:
        speak("Google search failed.")
    finally:
        driver.quit()

def open_youtube(song: str):
    speak(f"Playing {song} on YouTube")
    driver = get_driver(headless=False)
    try:
        driver.get("https://www.youtube.com")
        box = driver.find_element(By.NAME, "search_query")
        box.send_keys(song + Keys.RETURN)
        time.sleep(2)
        first = driver.find_element(By.CSS_SELECTOR, "ytd-video-renderer #video-title")
        speak(f"Playing: {first.text}")
        first.click()
        time.sleep(30)
    except Exception:
        speak("Could not open YouTube.")
    finally:
        driver.quit()


# ── Smart Command Processor ─────────────────────────────────────────
def process_command(command: str):
    """Use ChatGPT to classify and route the command intelligently."""
    if not command:
        return

    # Fast exit — no API call needed
    if any(w in command for w in ["exit", "quit", "goodbye", "bye jarvis"]):
        speak("Goodbye, sir. Jarvis shutting down.")
        raise SystemExit

    # ChatGPT classifies the intent
    intent = classify_command(command)
    print(f"[Intent detected: {intent}]")

    if intent == "weather":
        words = command.split()
        city = words[-1].capitalize() if len(words) > 1 else "Chennai"
        get_weather(city)

    elif intent == "news":
        topic = "technology"
        for t in ["sports", "business", "science", "health", "india", "world"]:
            if t in command:
                topic = t
                break
        get_news(topic)

    elif intent == "wiki":
        query = (command.replace("who is", "").replace("what is", "")
                        .replace("tell me about", "").strip())
        scrape_wikipedia(query)

    elif intent == "search":
        query = (command.replace("search", "").replace("google", "")
                        .replace("look up", "").strip())
        google_search(query)

    elif intent == "youtube":
        song = (command.replace("play", "").replace("youtube", "")
                       .replace("on", "").strip())
        open_youtube(song)

    elif intent == "screenshot":
        take_screenshot()

    elif intent == "open_app":
        for app in ["notepad", "calculator", "paint", "explorer"]:
            if app in command:
                open_application(app)
                return
        speak("Which application would you like me to open?")

    elif intent == "type_text":
        text = command.replace("type", "").strip()
        type_text(text)

    elif intent == "exit":
        speak("Goodbye, sir.")
        raise SystemExit

    else:
        # Default: full ChatGPT conversation with memory
        reply = ask_chatgpt(command)
        speak(reply)


# ── Main Loop ───────────────────────────────────────────────────────
def run_jarvis(use_voice: bool = False):
    speak("Jarvis online. All systems ready.")
    while True:
        try:
            command = listen() if use_voice else input("\nYou: ").lower().strip()
            process_command(command)
        except SystemExit:
            break
        except KeyboardInterrupt:
            speak("Interrupted. Shutting down.")
            break
        except Exception as e:
            speak(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # use_voice=True  → microphone input
    # use_voice=False → keyboard input (easier for testing)
    run_jarvis(use_voice=False)