# Text-to-Speech Web Application

This is a **Text-to-Speech (TTS) web application** built using **Streamlit** and **pyttsx3**. The application allows users to convert text into speech in various languages, adjust the speech rate, and choose between different voice options.

## Features

- Convert text to speech in multiple languages.
- Adjust speech rate for a customized experience.
- Choose between Default, Male, and Female voices.
- Play the generated speech directly in the app.
- Download the generated speech in **MP3, WAV, or OGG** formats.
- Store and view previous text-to-speech conversions in the history section.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository/text-to-speech-app.git
   ```
2. Navigate to the project directory:
   ```sh
   cd text-to-speech-app
   ```

## Dependencies

Ensure you have the following Python packages installed:

- `streamlit`
- `pyttsx3`
- `pydub`
- `base64`
- `tempfile`
- `threading`

You can install them using:
```sh
pip install streamlit pyttsx3 pydub
```

## Usage

Run the application with the following command:
```sh
streamlit run app.py
```

### How to Use
1. Enter your text in the provided text area.
2. Select the language from the dropdown menu.
3. Adjust the speech rate using the slider.
4. Choose between **Default, Male, or Female** voices.
5. Click **Convert to Speech** to generate the audio.
6. Play the generated speech directly in the app.
7. Download the audio file in the preferred format.
8. View previously generated speech entries in the history section.

## Supported Languages

The application supports the following languages:

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (Mandarin) (zh-cn)
- Japanese (ja)
- Korean (ko)
- Portuguese (pt)
- Italian (it)
- Dutch (nl)
- Khmer (km)

## Known Issues
- Some voices may not be available on all systems. If a selected voice is unavailable, the app will default to the system voice.
- The `pyttsx3` library does not natively support changing languages; additional configurations may be needed.

