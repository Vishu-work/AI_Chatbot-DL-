import streamlit as st
import cohere
import datetime
import webbrowser
import subprocess


co = cohere.Client("s7qgwB0QeSCV0p1xjhDkOiDhwYQ9Sp1ejLQ9mjX7")

def say(text):
    st.success(f"🤖 Jarvis: {text}")

def chat(message):
    try:
        response = co.chat(message=message, chat_history=[])
        reply = response.text.strip()
        say(reply)
        return reply
    except Exception as e:
        st.error(f"❌ Error in AI response: {e}")
        return "Error"

def ai(message):
    try:
        response = co.chat(message=message, model="command-nightly")
        say(response.text)
    except Exception as e:
        st.error(f"❌ Error in AI response: {e}")

def open_camera_app():
    say("Opening camera app.")
    try:
        subprocess.run("start microsoft.windows.camera:", shell=True)
    except:
        say("Sorry, I couldn't open the camera app.")

sites = {
    "YouTube": "https://www.youtube.com",
    "Google": "https://www.google.com",
    "Wikipedia": "https://www.wikipedia.com",
    "X": "https://www.x.com",
    "WhatsApp": "https://www.whatsapp.com",
    "ChatGPT": "https://chat.openai.com",
    "CarWale": "https://www.carwale.com",
    "Spotify": "https://www.spotify.com",
    "LinkedIn": "https://www.linkedin.com"
}

st.title("🧠 Jarvis - AI Voice Assistant (Web Version)")
st.markdown("Interact with Jarvis using the buttons below:")

with st.form("jarvis_form"):
    user_query = st.text_input("Ask Jarvis something:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_query:
    found = False

    # Check if opening a site
    for name, url in sites.items():
        if f'open {name.lower()}' in user_query.lower():
            say(f"Opening {name}")
            webbrowser.open(url)
            found = True
            break

    if 'the time' in user_query.lower():
        now = datetime.datetime.now().strftime('%I:%M %p')
        say(f"The time is {now}")
        found = True

    elif 'open camera app' in user_query.lower():
        open_camera_app()
        found = True

    elif 'using artificial intelligence' in user_query.lower():
        ai(user_query)
        found = True

    elif 'reset chat' in user_query.lower():
        st.session_state["chat_history"] = []
        say("Chat history reset.")
        found = True

    elif 'jarvis quit' in user_query.lower():
        say("Goodbye!")
        st.stop()

    if not found:
        chat(user_query)

