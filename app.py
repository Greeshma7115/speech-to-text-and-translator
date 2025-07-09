#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os
import tempfile

# Initialize
recognizer = sr.Recognizer()
translator = Translator()

# Language options
language_map = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Tamil': 'ta',
    'French': 'fr',
    'German': 'de',
    'Spanish': 'es',
    'Japanese': 'ja',
    'Chinese': 'zh-cn'
}

# App title
st.title("🎤 Speech Recognition & Translation App")

# Input mode
input_mode = st.radio("Choose Input Mode:", ("Microphone", "Upload File"))

# Translation option
translate = st.checkbox("Translate recognized text?")
target_lang_name = None
target_lang_code = None
if translate:
    target_lang_name = st.selectbox("Select Target Language", list(language_map.keys()))
    target_lang_code = language_map[target_lang_name]

# Function to recognize audio
def recognize_audio(audio):
    try:
        text = recognizer.recognize_google(audio)
        st.success("✅ Recognized Text:")
        st.write(text)

        if translate and target_lang_code:
            translated = translator.translate(text, dest=target_lang_code)
            st.success(f"🌍 Translated to {target_lang_name}:")
            st.write(translated.text)

    except sr.UnknownValueError:
        st.error("Could not understand audio.")
    except sr.RequestError as e:
        st.error(f"API error: {e}")

# Microphone input
if input_mode == "Microphone":
    if st.button("🎙️ Start Recording"):
        with sr.Microphone() as source:
            st.info("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            recognize_audio(audio)

# File upload input
elif input_mode == "Upload File":
    uploaded_file = st.file_uploader("Upload an audio file (.wav, .mp3, .flac)", type=["wav", "mp3", "flac"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            file_ext = uploaded_file.name.split('.')[-1]
            if file_ext == 'mp3':
                sound = AudioSegment.from_file(uploaded_file, format='mp3')
                sound.export(tmp_file.name, format='wav')
            elif file_ext == 'flac':
                sound = AudioSegment.from_file(uploaded_file, format='flac')
                sound.export(tmp_file.name, format='wav')
            else:
                tmp_file.write(uploaded_file.read())

            tmp_file_path = tmp_file.name

        # Process the audio file
        with sr.AudioFile(tmp_file_path) as source:
            audio = recognizer.record(source)
            recognize_audio(audio)

        # Clean up
        os.remove(tmp_file_path)

