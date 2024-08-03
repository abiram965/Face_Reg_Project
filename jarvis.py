import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return recognizer.recognize_google(audio)

command = listen()
print(f"You said: {command}")

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

speak("Hello, I am Jarvis. How can I help you?")
if "hello" in command:
    speak("Hello! How can I assist you?")
elif "open browser" in command:
   
    pass

import requests

def get_weather(city):
    api_key = "YOUR_WEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    temperature = data["main"]["temp"]
    speak(f"The current temperature in {city} is {temperature} degrees Celsius.")
while True:
    command = listen().lower()
    if "exit" in command:
        speak("Goodbye!")
        break
    # Add the command handling logic here
