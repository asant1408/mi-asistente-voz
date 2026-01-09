# app.py
import streamlit as st
from transformers import pipeline
import tempfile

st.set_page_config(page_title="Asistente Ligero", layout="centered")
st.title("🎙️ Asistente Multilingüe (Versión Ligera)")
st.write("Escribe una pregunta en español o inglés y obtén una respuesta.")

# Cargar modelo SIN torch (usa accelerate + CPU)
@st.cache_resource
def cargar_ia():
    # Este modelo es pequeño y funciona con accelerate
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        device=-1  # fuerza CPU
    )

try:
    ia = cargar_ia()
except Exception as e:
    st.error(f"Error al cargar el modelo: {str(e)}")
    st.stop()

# Entrada de texto (más estable que audio en esta versión)
pregunta = st.text_input("💬 Escribe tu pregunta:", "Hola, ¿cómo estás?")

if pregunta:
    # Detección básica de idioma
    if any(palabra in pregunta.lower() for palabra in ["hola", "gracias", "buenos", "mañana"]):
        prompt = f"Responde amablemente en español: {pregunta}"
        lang = "es"
    elif any(palabra in pregunta.lower() for palabra in ["hello", "thank", "good", "weather"]):
        prompt = f"Respond kindly in English: {pregunta}"
        lang = "en"
    else:
        prompt = f"Answer briefly: {pregunta}"
        lang = "en"
    
    with st.spinner("🧠 Pensando..."):
        try:
            respuesta = ia(prompt, max_length=80, do_sample=True)[0]['generated_text']
            st.subheader(f"🤖 IA ({lang}):")
            st.write(respuesta)
            
            # Convertir a voz
            from gtts import gTTS
            tts = gTTS(text=respuesta, lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                st.audio(tmp.name, format="audio/mp3")
        except Exception as e:
            st.error(f"Lo siento, hubo un error: {str(e)}")
            st.write("Intenta con una pregunta más simple.")
