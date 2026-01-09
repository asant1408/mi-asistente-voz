# app.py
import streamlit as st
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Asistente Simple", layout="centered")
st.title("🎙️ Asistente de Voz Básico")
st.write("Escribe algo en español o inglés y escucha la respuesta.")

pregunta = st.text_input("💬 Tu mensaje:", "Hola")

if pregunta:
    # Respuesta simple según idioma detectado
    if any(palabra in pregunta.lower() for palabra in ["hola", "gracias", "buenos", "adiós"]):
        respuesta = "¡Hola! ¿En qué puedo ayudarte hoy?"
        lang = "es"
    elif any(palabra in pregunta.lower() for palabra in ["hello", "thank", "goodbye", "help"]):
        respuesta = "Hello! How can I help you today?"
        lang = "en"
    else:
        respuesta = "I received your message!"
        lang = "en"

    st.subheader(f"🤖 Respuesta ({lang}):")
    st.write(respuesta)

    # Convertir a voz
    tts = gTTS(text=respuesta, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name, format="audio/mp3")
