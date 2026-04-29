# 🤖 Jarvis Bot: AI-Powered Desktop Assistant

Jarvis Bot is a locally hosted, Python-based desktop assistant inspired by Iron Man's iconic AI. By combining the conversational intelligence of OpenAI's GPT models with web scraping and system automation libraries, Jarvis goes beyond answering questions—it actively interacts with your computer and the web.

## ✨ Features

- **Smart Conversational AI:** Powered by OpenAI's `gpt-4o-mini` with conversation memory for natural, context-aware dialogue.
- **Intelligent Intent Routing:** Dynamically classifies commands to execute the right action instead of relying on strict, hard-coded keywords.
- **Voice & Text Modes:** Speak to Jarvis using your microphone or type commands via the terminal.
- **System Automation:** Can open local applications (Notepad, Calculator, etc.), take screenshots, and type text autonomously.
- **Web Browsing & Scraping:** 
  - 🌦️ Fetches real-time weather.
  - 📰 Reads the latest news headlines.
  - 🔍 Summarizes Wikipedia articles.
  - 🌐 Performs Google searches.
  - 🎥 Opens and plays specific videos on YouTube.

## 🛠️ Tech Stack

- **AI & Logic:** `openai`
- **Voice I/O:** `SpeechRecognition`, `pyttsx3`
- **Automation:** `pyautogui`, `subprocess`
- **Web Control:** `selenium`, `webdriver-manager`
- **Web Scraping:** `beautifulsoup4`, `requests`

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:
* Python 3.8 or higher installed on your machine.
* A working microphone (if using Voice Mode).
* Google Chrome installed (for Selenium web automation).
* An [OpenAI API Key](https://platform.openai.com/api-keys).

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/jarvis-bot.git](https://github.com/yourusername/jarvis-bot.git)
   cd jarvis-bot
