import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
from io import BytesIO
from pydub import AudioSegment

# Function to process text input
def process_text_input(text):
    # Placeholder for generative AI model response
    response = f"AI Response to: {text}"
    return response

# Function to process voice input
def process_voice_input(audio_file):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    audio.export("temp.wav", format="wav")
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    os.remove("temp.wav")
    return text

# Streamlit app
st.title("Voice and Text Based Input Interface for GenAI Chat")

# Text input
text_input = st.text_input("Enter your text here:")
if text_input:
    response = process_text_input(text_input)
    st.write(response)

# Voice input
audio_file = st.file_uploader("Upload your voice file here:", type=["wav", "mp3", "ogg"])
if audio_file:
    text_from_voice = process_voice_input(audio_file)
    st.write(f"Recognized Text: {text_from_voice}")
    response = process_text_input(text_from_voice)
    st.write(response)