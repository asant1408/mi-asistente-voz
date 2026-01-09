# app.py
import streamlit as st
from transformers import pipeline
import tempfile
import os

# Configuración de la página
st.set_page_config(page_title="Mi Asistente de Voz", layout="centered")
st.title("🎙️ Mi Asistente Multilingüe")
st.write("Sube un audio corto (WAV o MP3) y te responderé en el mismo idioma.")

# Cargar modelo de IA (ligero y multilingüe)
@st.cache_resource
def cargar_ia():
    return pipeline("text2text-generation", model="google/flan-t5-small", max_length=80)

ia = cargar_ia()

# Subida de audio
audio_file = st.file_uploader("🗣️ Sube tu audio", type=["wav", "mp3"])

if audio_file is not None:
    # Guardar temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.getvalue())
        audio_path = tmp.name

    # Aquí iría Whisper... pero para simplificar el despliegue,
    # por ahora simulamos con entrada de texto.
    # (Más abajo te explico cómo añadir Whisper después)
    
    st.info("⚠️ Nota: Esta versión usa entrada de texto para evitar errores de despliegue.")
    texto_usuario = st.text_input("O escribe lo que dirías:", "Hola, ¿cómo estás?")
    
    if texto_usuario:
        # Detectar idioma básico (simplificado)
        if any(palabra in texto_usuario.lower() for palabra in ["hola", "gracias", "buenos"]):
            lang = "es"
            prompt = f"Responde amablemente en español: {texto_usuario}"
        elif any(palabra in texto_usuario.lower() for palabra in ["hello", "thank you", "good"]):
            lang = "en"
            prompt = f"Respond kindly in English: {texto_usuario}"
        else:
            lang = "en"
            prompt = f"Respond: {texto_usuario}"
        
        # Generar respuesta
        respuesta = ia(prompt)[0]['generated_text']
        
        st.subheader(f"🤖 IA ({lang}):")
        st.write(respuesta)
        
        # Convertir a voz
        try:
            from gtts import gTTS
            tts = gTTS(text=respuesta, lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                tts.save(tmp_audio.name)
                st.audio(tmp_audio.name, format="audio/mp3")
        except:
            st.warning("🔊 Audio no disponible en esta plataforma, pero la respuesta está arriba.")
