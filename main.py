import pyttsx3
import os
import queue
import sounddevice as sd
import vosk
import json
import random
import ctypes
import subprocess
import webbrowser
import pywhatkit

engine = pyttsx3.init()
engine.setProperty('rate', 130)  
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print("FRIDAY:", text)
    engine.say(text)
    engine.runAndWait()

model_path = "vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")


def browser_module(command):
    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query} on Google.")
        pywhatkit.search(query)

    elif "play" in command and "youtube" in command:
        video = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {video} on YouTube.")
        pywhatkit.playonyt(video)

    elif "open facebook" in command:
        speak("Opening Facebook.")
        webbrowser.open("https://www.facebook.com")

    elif "open instagram" in command:
        speak("Opening Instagram.")
        webbrowser.open("https://www.instagram.com")

    elif "open browser" in command or "open edge" in command or "open microsoft edge" in command:
        speak("Opening Microsoft Edge.")
        os.system("start msedge")

    else:
        speak("Sorry, I did not understand the browser command.")

def process_command(command):
    if "note" in command:
        os.system("notepad")
        speak("Opening Notepad.")
    elif "online music" in command:
        os.system("start Brave")
        speak("About to play")
    elif "browser" in command or "search" in command or "youtube" in command or "open google" in command:
        browser_module(command)
    elif "calculator" in command:
        os.system("calc")
        speak("Opening Calculator.")
    elif "camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        speak("Opening Camera.")
    elif "close all applications" in command or "close everything" in command:
        speak("Are you sure you want to close all open applications? Please say yes or no.")
        confirmation = listen()
        if "yes" in confirmation.lower():
            speak("Closing all open applications except this terminal.")
            os.system('powershell "Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and $_.ProcessName -notmatch \'(cmd|powershell|python|code|wt)\' } | ForEach-Object { Stop-Process -Id $_.Id -Force }"')
        else:
            speak("Okay, I will not close anything.")
    elif "shut down" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "lock screen" in command or "Freez Annie" in command:
        speak("Locking the screen.")
        ctypes.windll.user32.LockWorkStation()
    elif "play offline music" in command:
        music_dir = "C:\\Users\\Public\\Music"
        songs = [song for song in os.listdir(music_dir)]
        if songs:
            song = random.choice(songs)
        
            speak(f"Playing {song}")
            os.startfile(os.path.join(music_dir, song))
        else:
            speak("No music files found in the music directory.")
    elif "hello" in command:
        speak("Hello! how are you?")
    elif "what is your name" in command:
        speak("I am FRIDAY, your offline assistant.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        exit(0)
    else:
        speak("")

speak("Hello sir, FRIDAY activated. How can I help you?")
while True:
    print("Listening...")
    command = listen()
    print("You said:", command)
    process_command(command.lower())
