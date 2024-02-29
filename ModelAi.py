import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import requests

def initialize_engine():
    """Initializes the text-to-speech engine and lists available voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name} ({voice.languages})")
    voice_id = input("Select a voice ID for Jarvis: ")
    try:
        selected_voice = voices[int(voice_id)]
        engine.setProperty('voice', selected_voice.id)
        print(f"Jarvis will speak in: {selected_voice.name}")
    except IndexError:
        print("Invalid voice ID. Using the default voice.")
    return engine

def speak(engine, text):
    """Speaks the given text using the selected engine."""
    engine.say(text)
    engine.runAndWait()

def listen(engine):
    """Listens to the microphone and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"Recognized: {command}")
        except Exception as e:
            print("I didn't get that. Try typing the command.")
            command = None
    return command

def text_input():
    """Gets text input from the user."""
    return input("Type your command: ")

def search_wikipedia(query):
    """Searches Wikipedia for the query and returns the summary."""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except Exception as e:
        return "An error occurred while searching Wikipedia."

def open_social_media(platform_name, url):
    """Opens a social media platform in the default web browser."""
    webbrowser.open(url)
    return f"Opening {platform_name}."

def get_current_location_and_open_in_maps():
    """Fetches the current location based on IP and opens it in Google Maps."""
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = data['loc']
        webbrowser.open(f"https://www.google.com/maps/?q={location}")
        return f"Opened your current location in Google Maps: {location}"
    except Exception as e:
        return "Failed to fetch or open current location."

def tell_time_and_date(engine):
    """Tells the current time and date."""
    now = datetime.datetime.now()
    date_time = now.strftime("It's %H hours and %M minutes on %A, %B %d, %Y.")
    speak(engine, date_time)

def handle_command(engine, command):
    """Handles the command."""
    if command:
        command = command.lower()
        social_media_commands = {
            'open youtube': ('YouTube', 'https://www.youtube.com'),
            'open google': ('Google', 'https://www.google.com'),
            'open facebook': ('Facebook', 'https://www.facebook.com'),
            'open twitter': ('Twitter', 'https://twitter.com'),
            'open instagram': ('Instagram', 'https://www.instagram.com')
        }

        if 'hello' in command:
            speak(engine, "Hello! How can I assist you today?")
        elif 'your name' in command:
            speak(engine, "I am Jarvis, your personal assistant.")
        elif 'wikipedia' in command or 'what is' in command or 'who is' in command:
            speak(engine, "Searching Wikipedia...")
            query = command.replace("wikipedia", "").replace("what is", "").replace("who is", "").strip()
            results = search_wikipedia(query)
            print(results)
            speak(engine, results)
        elif any(keyword in command for keyword in social_media_commands):
            for keyword, (name, url) in social_media_commands.items():
                if keyword in command:
                    message = open_social_media(name, url)
                    speak(engine, message)
                    break
        elif 'location' in command:
            message = get_current_location_and_open_in_maps()
            speak(engine, message)
        elif 'time' in command or 'date' in command:
            tell_time_and_date(engine)
        else:
            speak(engine, "I'm sorry, I don't know how to do that yet.")
    else:
        speak(engine, "Sorry, I didn't catch any command.")

def main():
    engine = initialize_engine()
    speak(engine, "Welcome! Would you like to type or speak your command?")
    mode = input("Type 'speak' to use voice or anything else to type commands: ")

    while True:
        if mode.lower() == 'speak':
            command = listen(engine)
        else:
            command = text_input()

        if command is not None and 'exit' in command.lower():
            speak(engine, "Goodbye!")
            break

        handle_command(engine, command)

if __name__ == "__main__":
    main()


