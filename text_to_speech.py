import streamlit as st
from openai import OpenAI
import os
import openai
import pyaudio
import wave
from audio_recorder_streamlit import audio_recorder

openai_key = os.environ.get('OPENAI_API_KEY')
#openai_key = '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'#st.secrets["OPEN_AI_KEY"]
def text_to_speech(text, voice):
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )
    #response = openai.text_to_speech(text, voice)
    
    with open('output.mp3','wb') as f:
        f.write(response.content)
    return "output.mp3"

# create a function to display audio

def display_audio_file(audio_file):
    audio_file = open(audio_file, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
    
    
#creata function to display text
def display_text(text):
    st.write(text)
    
def display_voice_option():
    # st.write('Voice Options')
    # st.write('1. Default')
    # st.write('2. Voice 1')
    # st.write('3. Voice 2')
    # st.write('4. voice 3')
    # st.write('5. voice 4')
    voices = st.selectbox('select voice',['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']) 
    return voices

# create a function to dsiplay text input
def display_text_input():
    text = st.text_area("Enter Text to convert into speech")
    return text

# create a function to display the convert button

def display_convert_button():
    if st.button("convert"):
        return True
    return False
# create a function to display voice input
def display_convert_voice_button():
    if st.button("start recording voice"):
        return True
    return False

def display_voice_input():
    # Set up Streamlit app
    st.write("Sound Recorder")

    # Record sound from user input
    #recorded_audio = audio_recorder()
    recorded_audio = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
    if recorded_audio:
        st.audio(recorded_audio, format="audio/wav")
        # once a recording is completed, audio data will be saved to wav_audio_data   
        st.audio(recorded_audio.export().read())  # Play the audio

        # Optionally, save the audio to a file
        with open("recording.wav", "wb") as f:
            f.write(recorded_audio.export().read())

        st.button("Download Recording", on_click=lambda: st.download_button("recording.wav", data=recorded_audio.export().read(), file_ext="wav"))

        # Display the recorded sound
        audio_file = open("recording.wav", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav")

    return recorded_audio
def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    st.write("Recording...")

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Recording complete!")

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))   
    wf.close()  
    # Set up Streamlit app
    st.title("Sound Recorder")  

    # Display the recorded sound
    audio_file = open(filename +'.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/wav")
    return audio_file

def translate_audio(audio_file):
    st.write("converting to text")
    client = OpenAI()
    #audio_file = open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    st.write(transcription.text)
   
       # response_format="text"
    
# create a function to display the convert button




# create a function to display_main_app

def main():
    st.title('Test to Speech  App')
    text = display_text_input()
    voice = display_voice_option()
    convert = display_convert_button()
    if convert:
        audio_file = text_to_speech(text, voice)
        display_audio_file(audio_file)
    
    ()
    voice=display_convert_voice_button()
    
    if voice:
      #audio_file=display_voice_input()
      audio_file=record_audio("speech",duration=5)
      translate_audio(audio_file)
    
if __name__ == '__main__':
    main()
    
    
    