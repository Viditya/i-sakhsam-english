import os
import openai
import streamlit as st
import base64
from io import BytesIO
import wave
import speech_recognition as sr
import webbrowser

# Set your OpenAI API key
# openai.api_key = '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'
openai.api_key = os.environ['OPENAI_API_KEY']

def correct_text(user_text):
# Without assitant role to maintain continuity
    messages = [
    {"role": "system", "content": "Be my English teacher and an expert in Hindi translaation and tell me mistakes in the following sentence for 10 minutes. be detailed in response and point \
    out all the grammatical mistakes with correction. Convert the response in hindi and diplay it along with the original sentence in the corrected form in English."},
    {"role": "user", "content": "I is goiang"},
    {"role":"assistant","content":"""
    
    I is goiang. \n
    Mistakes:\n
    1. The subject pronoun 'I' should be capitalized.\n
    2. The verb 'is' should be replaced with 'am' to match the subject pronoun 'I'.\n
    3. The word 'goiang' is misspelled. It should be 'going'.\n
    Correct Sentence:\n
    I am going.\n
    मिस्टेक:\n
    1. सब्जेक्ट प्रोनाउन 'I' को कैपिटलाइज किया जाना चाहिए।\n
    2. क्रिया 'is' को 'am' से बदल देना चाहिए ताकि यह सब्जेक्ट प्रोनाउन 'I' के साथ मेल खाए।\n
    3. 'goiang' शब्द की वर्तनी गलत है। इसे 'going' करना चाहिए।\n

    सही वाक्य:\n
    I am going."""},
        {"role": "user", "content": user_text}
    ]

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=messages,
    temperature =0, 
    max_tokens = 500
    )

    # print(response["choices"][0].message["content"].strip())
    corrected_text = response["choices"][0].message["content"].strip()
    return corrected_text

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Recording...")
        audio = r.listen(source)
        st.write("Finished recording.")
        try:
            text = r.recognize_google(audio)
            st.write(correct_text(text))
        except:
            st.write("Sorry, could not recognize your voice.")


def main():
    st.title("Correct Text")
    st.sidebar.markdown("Voice Input")
    audio_input = st.sidebar.radio("Select Input Source:", ["Text", "Voice"])

    if audio_input == "Voice":
       if st.button("Record Audio"):
         record_audio()

    else:
        st.sidebar.markdown("Text Input")
        input_text = st.sidebar.text_area("Enter text to correct")
        if st.sidebar.button("Check the sentence"):
            corrected = correct_text(input_text)
            st.write(corrected)

if __name__ == "__main__":
    main()
