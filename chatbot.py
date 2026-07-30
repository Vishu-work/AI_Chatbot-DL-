import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import subprocess
import cohere

# Initialize Cohere client
co = cohere.Client("YOUR_API_KEY")

# Text-to-Speech
def say(text):
    print(f"🤖 Jarvis: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech Recognition
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("🧠 Recognizing...")
        command = r.recognize_google(audio)
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        say("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        say("Sorry, I could not reach the speech recognition service.")
        return ""

# Chat using Cohere
def chat(message):voice
    try:
        response = co.chat(message=message, chat_history=[])
        reply = response.text.strip()
        say(reply)
        return reply
    except Exception as e:
        print("❌ Error:", e)
        say("Something went wrong.")
        return "Error"

# AI Mode with specific model
def ai(message):
    try:
        response = co.chat(message=message, model="command-nightly")
        say(response.text)
    except Exception as e:
        print("❌ Error:", e)
        say("Something went wrong.")

# Open Camera App
def open_camera_app():
    say("Opening camera app.")
    try:
        subprocess.run("start microsoft.windows.camera:", shell=True)
    except:
        say("Sorry, I couldn't open the camera app.")

# Common websites
sites = {
    'youtube': 'https://www.youtube.com',
    'google': 'https://www.google.com',
    'wikipedia': 'https://www.wikipedia.com',
    'x': 'https://www.x.com',
    'whatsapp': 'https://www.whatsapp.com',
    'chatgpt': 'https://chat.openai.com',
    'carwale': 'https://www.carwale.com',
    'spotify': 'https://www.spotify.com',
    'linkedin': 'https://www.linkedin.com'
}

# Start Jarvis
say("Hello, I am Jarvis A.I. What can I do for you?")
say("Do you want to chat using voice or text?")
mode = input("Choose mode ('voice' or 'text'): ").strip().lower()

if mode not in ['voice', 'text']:
    say("Invalid choice. Defaulting to voice mode.")
    mode = 'voice'

say(f"{mode.capitalize()} mode activated.")

# Main loop
while True:
    if mode == "voice":
        query = listen().lower().strip()
    else:
        query = input("You: ").lower().strip()

    found = False

    # Mode toggling
    if "switch to voice mode" in query:
        mode = "voice"
        say("Switched to voice mode.")
        continue

    elif "switch to text mode" in query:
        mode = "text"
        say("Switched to text mode.")
        continue

    # Open websites
    for name, url in sites.items():
        if f'open {name}' in query:
            say(f"Opening {name}")
            webbrowser.open(url)
            found = True
            break

    # Time
    if "the time" in query:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        say(f"The time is {current_time}")
        found = True

    # Date
    elif "the date" in query or "what is the date" in query:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        say(f"Today's date is {current_date}")
        found = True

    # Day
    elif "what day" in query or "which day" in query or "what is the day" in query:
        current_day = datetime.datetime.now().strftime('%A')
        say(f"Today is {current_day}")
        found = True

    # Camera
    elif "open camera app" in query:
        open_camera_app()
        found = True

    # AI Command
    elif "using artificial intelligence" in query:
        ai(message=query)
        found = True

    # Exit
    elif "jarvis quit" in query or 'bye' in query:
        say("Goodbye!")
        break

    # Reset
    elif "reset chat" in query:
        say("Chat reset.")
        found = True

    # Default chat if nothing else matched
    if not found and query != "":
        print("💬 Chatting...")
        chat(message=query)
