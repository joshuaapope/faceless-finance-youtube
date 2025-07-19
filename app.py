import streamlit as st
import openai
import requests
from gtts import gTTS
import os
from io import BytesIO
from pydub import AudioSegment

st.title("📈 Faceless Finance YouTube Script & Voiceover Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]

topic = st.text_input("🔍 Enter a personal finance topic:")

if st.button("Generate Script + Voiceover"):
    if topic:
        with st.spinner("Creating video script..."):
            prompt = f"Create a longform YouTube video script (~1500 words) about {topic} that is informative, engaging, and easy to follow for a broad audience. Make it sound like a calm, American male narrator."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            script = response.choices[0].message.content
            st.subheader("📝 Generated Script:")
            st.write(script)

            st.subheader("🔊 Generating Voiceover...")
            tts = gTTS(script, lang='en', tld='com')
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            st.audio(audio_fp, format='audio/mp3')

            with open("voiceover.mp3", "wb") as f:
                f.write(audio_fp.getbuffer())
            st.success("✅ Voiceover complete!")
    else:
        st.warning("Please enter a topic.")

