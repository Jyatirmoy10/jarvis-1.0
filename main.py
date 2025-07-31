import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
import sys

# Import AI function from client.py
from client import ask_jarvis

# Load environment variables
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Speak text via gTTS + pygame"""
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print(f"[main.py] Speak error: {e}", file=sys.stderr)

def processCommand(c):
    cl = c.lower()
    if "open google" in cl:
        webbrowser.open("https://google.com")
    elif "open facebook" in cl:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in cl:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in cl:
        webbrowser.open("https://linkedin.com")
    elif cl.startswith("play"):
        song = cl.split(" ", 1)[1] if len(cl.split()) > 1 else None
        link = musicLibrary.music.get(song) if song else None
        speak(f"Playing {song}" if link else f"Song {song} not found.")
        if link:
            webbrowser.open(link)
    elif "news" in cl:
        if not NEWSAPI_KEY:
            speak("News API key is missing. Cannot fetch news.")
            return
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWSAPI_KEY}", timeout=5)
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                if not articles:
                    speak("No news articles found.")
                for article in articles:
                    speak(article.get('title', 'No title'))
            else:
                speak(f"Failed to fetch news. Status code {r.status_code}.")
        except Exception as e:
            print(f"[main.py] News fetch error: {e}", file=sys.stderr)
            speak("Error fetching news.")
    else:
        output = ask_jarvis(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yeah, I am listening...")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"[main.py] Error: {e}", file=sys.stderr)

