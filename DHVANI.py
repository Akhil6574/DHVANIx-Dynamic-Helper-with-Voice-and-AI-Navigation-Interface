import gtts
import os
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import re
import requests
from googletrans import Translator
from transformers import pipeline
from playsound import playsound
user_language = "en"
translator = Translator()
language_map = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "hindi": "hi",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "portuguese": "pt",
    "russian": "ru",
    "arabic": "ar",
    "bengali": "bn",
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "gujarati": "gu",
    "punjabi": "pa",
    "urdu": "ur",
    "kannada": "kn",
    "malayalam": "ml",
    "odia": "or",
    "assamese": "as",
    "sanskrit": "sa",
    "konkani": "kok",
    "maithili": "mai",
    "meitei": "mni",
    "bodo": "brx",
    "dogri": "doi",
    "santali": "sat",
    "kashmiri": "ks",
    "tulu": "tcy",
    "sindhi": "sd",
    "burmese": "my",
    "nepali": "ne",
    "swahili": "sw",
    "filipino": "tl",
    "persian": "fa",
    "turkish": "tr",
    "thai": "th",
    "vietnamese": "vi",
    "polish": "pl",
    "romanian": "ro",
    "ukrainian": "uk",
    "hebrew": "he",
    "dutch": "nl",
    "greek": "el",
    "swedish": "sv",
    "finnish": "fi",
    "norwegian": "no",
    "danish": "da",
    "hungarian": "hu",
    "czech": "cs",
    "slovak": "sk",
    "croatian": "hr",
    "bulgarian": "bg",
    "catalan": "ca",
    "irish": "ga",
    "latvian": "lv",
    "lithuanian": "lt",
    "welsh": "cy",
    "georgian": "ka",
    "armenian": "hy",
    "azerbaijani": "az"
}


def select_language_by_speech():
    global user_language
    speak("Please say your preferred language.", user_language)
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for language name...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Recognizing language name...")
            spoken_language = recognizer.recognize_google(audio).lower()  # Convert to lowercase for easier matching
            print(f"User said: {spoken_language}")
            
            if spoken_language in language_map:
                user_language = language_map[spoken_language]
                speak(f"You have selected {spoken_language.capitalize()} as your language.", user_language)
            else:
                speak(f"Sorry, I don't support {spoken_language} yet. Defaulting to English.", "en")
                user_language = "en"
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Defaulting to English.", "en")
            user_language = "en"
        except sr.RequestError as e:
            speak(f"Error with speech recognition service: {e}. Defaulting to English.", "en")
            user_language = "en"
def speak(audio, lang=user_language):
    try:
        if lang != "en":
            audio = translator.translate(audio, dest=lang).text
        print(f"Speaking in {lang}: {audio}")
        tts = gtts.gTTS(audio, lang=lang)
        tts.save("temp_audio.mp3")
        playsound("temp_audio.mp3")
        os.remove("temp_audio.mp3")
    except Exception as e:
        print("Error in translation or speech synthesis:", e)
        print("Fallback text:", audio)

def get_recipient_email():
    speak("Please spell out the email address of the recipient.", user_language)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for spelled-out email address...")
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=30)
            print("Recognizing email address...")
            recipient_email = recognizer.recognize_google(audio).lower()
            print(f"User said: {recipient_email}")

            # Replace 'at' with '@', 'dot' with '.', and remove spaces
            formatted_email = recipient_email.replace(" at ", "@").replace(" dot ", ".").replace(" ", "")
            print(f"Formatted email: {formatted_email}")

            # Validate email format using a regular expression
            if re.match(r"[^@]+@[^@]+\.[^@]+", formatted_email):
                speak(f"Got it, sending email to {formatted_email}.", user_language)
                return formatted_email
            else:
                speak("That doesn't seem like a valid email address. Please try again.", user_language)
                return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand the email address. Please try again.", user_language)
            return None
        except sr.RequestError as e:
            speak(f"Error with the speech recognition service: {e}. Please try again.", user_language)
            return None

        
def wish_me():
    select_language_by_speech()  # Ask for preferred language using speech input
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!", user_language)
    elif 12 <= hour < 17:
        speak("Good Afternoon!", user_language)
    elif 17 <= hour < 19:
        speak("Good Evening!", user_language)
    else:
        speak("Good Night!", user_language)
    speak("I am your virtual assistant Dhvani. How can I assist you today?", user_language)


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            translated = translator.translate(query, src=user_language, dest='en')
            print(translated.text)
            print(f"User said: {query} (Language: {user_language})")
            return translated.text
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return ""
def open_website_by_speech():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            speak("Please specify the website you want to open.", user_language)
            print("Listening for website name...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing website name...")
                website_name = recognizer.recognize_google(audio).lower()  # Convert to lowercase for easier matching
                print(f"User said: {website_name}")
            
            # Check if the user has mentioned a well-known site without 'www' or '.com'
                if not website_name.startswith("www."):
                    website_name = f"www.{website_name}.com"
            
                speak(f"Opening {website_name}", user_language)
                webbrowser.open(f"http://{website_name}")
                break
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand the website name.", user_language)
                continue
            except sr.RequestError as e:
                speak(f"Error with speech recognition service: {e}", user_language)
                continue

intent_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

intents = {
    "search Wikipedia": "Find information about something on Wikipedia.",
    "open": "Open anything.",
    "play music": "Play music from the computer.",
    "fetch weather": "Tell the weather for a specific location.",
    "tell the time": "Provide the current time.",
    "shutdown the system": "Shut down the computer.",
    "exit": "Exit the assistant program.",
    "send email": "Send an email to a specific person.",
    "about you": "Tell information about yourself.",
    "play video": "Play a video from the computer.",
    "change language": "Change the language of the assistant.",
}

def classify_intent(query, lang):
    intent_labels = list(intents.keys())
    result = intent_pipeline(query, candidate_labels=intent_labels, hypothesis_template="This request is about {}.")
    intent = result['labels'][0]
    confidence = result['scores'][0]
    print(f"Intent: {intent}, Confidence: {confidence}")
    if confidence < 0.4:
        speak("I'm not sure I understood. Let me search the internet for you.", lang)
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        return intent

def process_command(query):
    intent = classify_intent(query, user_language)
    if not intent or query == "none":
        speak("I'm not sure I understood. Can you please clarify?", user_language)
        return

    if intent == "search Wikipedia":
        speak("Searching Wikipedia...", user_language)
        query = query.replace("search Wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia", user_language)
            print(results)
            speak(results, user_language)
        except Exception as e:
            speak("Sorry, I couldn't find any results on Wikipedia.", user_language)

    elif intent == "open":
        open_website_by_speech()

    elif intent == "play music":
        music_dir = 'E:\\My MUSIC'
        try:
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music from your collection.", user_language)
        except Exception as e:
            speak("Sorry, I couldn't play music. so let me open spotify for you", user_language)
            webbrowser.open(f"http://{"www.spotify.com"}")

    elif intent == "fetch weather":
        location = query.split("in")[-1].strip()
        weather_info = fetch_weather(location)
        speak(weather_info, user_language)

    elif intent == "tell the time":
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}", user_language)

    elif intent == "shutdown the system":
        speak("Shutting down the system.", user_language)
        os.system("shutdown /s /t 1")

    elif intent == "exit":
        speak("Goodbye! Have a great day!", user_language)
        exit()

    elif intent == "send email":
        speak("What should I say?", user_language)
        content = take_command()  # Get email content
        to = None
        while not to:
            to = get_recipient_email()  # Get recipient's email dynamically through speech
        send_email(to, content)
    elif intent == "about you":
        speak("I am Dhvani, your multilingual virtual assistant!", user_language)

    elif intent == "play video":
        video_dir = "C:/video"
        try:
            videos = os.listdir(video_dir)
            os.startfile(os.path.join(video_dir, videos[0]))
            speak("Playing video from your collection.", user_language)
        except Exception as e:
            speak("Sorry, I couldn't play the video. so let me open youtube for you", user_language)
            webbrowser.open(f"http://{"www.youtube.com"}")
    elif intent == "change language":
        select_language_by_speech()
    

def fetch_weather(location):
    api_key = "53bda19ace9992895a060120b48f6886"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url).json()
        if response["cod"] != "404":
            weather = response["main"]
            temp = weather["temp"]
            description = response["weather"][0]["description"]
            return f"The temperature in {location} is {temp}°C with {description}."
        else:
            return "Location not found."
    except Exception as e:
        return "Unable to fetch weather information."


def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('dhvanixassistant@gmail.com', 'rfgy fpmj jbmk zwev')
        server.sendmail('dhvanixassistant@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully.", user_language)
    except Exception as e:
        speak("Sorry, I was unable to send the email.", user_language)
        print(e)


if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if query:
            process_command(query)
