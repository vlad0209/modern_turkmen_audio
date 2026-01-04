import torch
from transformers import AutoTokenizer, AutoModelForTextToWaveform
import streamlit as st
import scipy.io.wavfile

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tuk-script_latin")
model = AutoModelForTextToWaveform.from_pretrained("facebook/mms-tts-tuk-script_latin")

def text_to_speech(text):
    # Tokenize the text input
    inputs = tokenizer(text, return_tensors="pt")

    # Generate the speech waveform
    with torch.no_grad():
        output = model(**inputs).waveform
    
    # Convert tensor to numpy array and save
    waveform = output.squeeze().cpu().numpy()

    return waveform

st.title("Преобразование текста на туркменском в речь с использованием модели Facebook MMS-TTS")
text_input = st.text_area("Введите текст на туркменском языке латиницей, который вы хотите преобразовать в речь:")
output_file = "output.wav"

if 'generationRequestStatus' not in st.session_state:
    st.session_state.generationRequestStatus = 'idle'

if st.session_state.generationRequestStatus != 'pending':
        if st.button("Сгенерировать речь", use_container_width=True):
            if text_input:
                st.session_state.generationRequestStatus = 'pending'
                st.rerun()
            else:
                st.warning("Пожалуйста, введите текст.")
else:
    st.button("Processing...", icon="spinner", disabled=True, use_container_width=True)

if st.session_state.generationRequestStatus == 'pending':
      
    speech_waveform = text_to_speech(text_input)
          
    scipy.io.wavfile.write(output_file, model.config.sampling_rate, speech_waveform)
          
    # set session state to completed
    st.session_state.generationRequestStatus = 'completed'
    st.rerun()
      
elif st.session_state.generationRequestStatus == 'completed':
          # Отображение аудиоплеера
          st.audio(output_file, format="audio/wav")
          st.success("Генерация завершена!")
          # download link
          with open(output_file, "rb") as f:
              st.download_button(
                label="Скачать сгенерированный аудиофайл",
                data=f,
                file_name="output.wav",
                mime="audio/wav"
              )
            
    
