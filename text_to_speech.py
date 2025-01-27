import streamlit as st
import pyttsx3
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading
import base64
import tempfile

# Function to convert text to speech
def text_to_speech(text, language, speech_rate, voice):
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set language
        engine.setProperty('language', language)

        # Set speech rate
        engine.setProperty('rate', int(150 * speech_rate))  # Adjust rate as needed

        # Select voice based on user choice
        if voice == "Male":
            try:
                engine.setProperty('voice', "VOICE_ID_FOR_MALE_VOICE")  # Replace with the appropriate voice ID
            except:
                st.warning("Male voice not available, using default voice.")
        elif voice == "Female":
            try:
                engine.setProperty('voice', "VOICE_ID_FOR_FEMALE_VOICE")  # Replace with the appropriate voice ID
            except:
                st.warning("Female voice not available, using default voice.")

        # Create a temporary file to save the speech output
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            engine.save_to_file(text, temp_file.name)
            engine.runAndWait()

            # Read the temporary file and return the speech output
            with open(temp_file.name, 'rb') as audio_file:
                output = BytesIO(audio_file.read())
                output.seek(0)

        return output
    except Exception as e:
        st.error(f"An error occurred during text-to-speech conversion: {e}")
        return None

# Remaining code remains the same...

# Function to save audio file
def save_audio_file(audio_file, filename, format):
    audio_file.seek(0)
    audio_data = audio_file.read()
    b64_audio = base64.b64encode(audio_data).decode()

    file_download_link = f'<a href="data:audio/{format};base64,{b64_audio}" download="{filename}.{format}">Download Audio File</a>'
    st.markdown(file_download_link, unsafe_allow_html=True)

# Function to play audio
def play_audio(audio_file):
    audio_file.seek(0)
    audio = AudioSegment.from_file(audio_file, format="mp3")
    play(audio)

# Function to play audio in a separate thread
def play_audio_thread(audio_file):
    threading.Thread(target=play_audio, args=(audio_file,)).start()

# Streamlit interface
st.set_page_config(page_title="Text to Speech Conversion", page_icon=":speaker:")
st.title("Text to Speech Conversion")
st.write("Enter the text you want to convert to speech")

# Text input
user_text = st.text_area("Type your text here", height=200)

# Language selection
language_options = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese (Mandarin)': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Portuguese': 'pt',
    'Italian': 'it',
    'Dutch': 'nl',
    'Khmer': 'km',
}
language = st.selectbox("Select language", list(language_options.keys()), index=0)

# Speech rate adjustment
speech_rate = st.slider("Speech Rate", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Voice selection
voice_options = ["Default", "Male", "Female"]
voice = st.selectbox("Select Voice", voice_options)

audio_file = None  # Initialize audio_file

# Convert to speech button
if st.button("Convert to Speech"):
    if user_text:
        with st.spinner('Converting text to speech...'):
            audio_file = text_to_speech(user_text, language_options[language], speech_rate, voice)
            if audio_file:
                # Display the input text
                st.subheader("Input Text")
                st.write(user_text)

                # Display the audio player
                st.subheader("Audio Player")
                audio_bytes = audio_file.getvalue()
                st.audio(audio_bytes, format='audio/mp3')

                # Play the audio in a separate thread
                play_audio_thread(audio_file)

                # Save the audio file
                st.subheader("Download Audio")
                save_audio_file(audio_file, "speech_output", "mp3")

                # Store audio file in session state for further use
                st.session_state['audio_file'] = audio_file
    else:
        st.warning("Please enter some text to convert to speech.")

# Additional information and instructions
st.write("---")
st.info("This app allows you to convert text to speech in various languages. You can adjust the speech rate and select a voice (Default, Male, Female).")

# Sidebar for additional options
st.sidebar.title("Additional Options")

# Save audio file format selection
audio_formats = ["mp3", "wav", "ogg"]
save_format = st.sidebar.selectbox("Save Audio Format", audio_formats)

# Additional information in the sidebar
st.sidebar.write("---")
st.sidebar.info("Use the options above to customize your text-to-speech experience.")

# Save audio file with custom filename
if st.sidebar.button("Save Audio with Custom Name"):
    custom_filename = st.sidebar.text_input("Enter Custom Filename", key="custom_filename")
    if custom_filename and 'audio_file' in st.session_state:
        save_audio_file(st.session_state['audio_file'], custom_filename, save_format)
    else:
        st.sidebar.warning("Please enter a filename and ensure audio has been generated.")

# Text-to-speech history
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'audio_file' in st.session_state:
    st.session_state['history'].append({
        'text': user_text,
        'language': language,
        'speech_rate': speech_rate,
        'voice': voice,
        'audio_data': st.session_state['audio_file'].getvalue()
    })

st.write("---")
st.subheader("Text-to-Speech History")
for i, entry in enumerate(st.session_state['history'], start=1):
    with st.expander(f"Entry {i}"):
        st.write(f"**Text:** {entry['text']}")
        st.write(f"**Language:** {entry['language']}")
        st.write(f"**Speech Rate:** {entry['speech_rate']}")
        st.write(f"**Voice:** {entry['voice']}")
        st.audio(entry['audio_data'], format='audio/mp3')