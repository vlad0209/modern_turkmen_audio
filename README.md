# Modern Turkmen Audio

A Turkmen Text-to-Speech (TTS) application that converts Turkmen text (Latin script) to natural-sounding audio using Facebook's MMS-TTS model.

## Features

- **Web Interface**: Interactive Streamlit web app for easy text-to-speech conversion
- **Command-line Tool**: CLI tool for batch processing and automation
- **High-Quality Audio**: Uses Facebook's MMS-TTS model trained on Turkmen language
- **Multiple Output Formats**: Supports both WAV and MP3 audio formats
- **Download Support**: Generate and download audio files directly from the web interface

## Requirements

- Python 3.14 (or compatible version)
- PyTorch
- Transformers
- Streamlit
- SciPy
- FFmpeg (optional, for MP3 output in CLI tool)

## Installation

1. Clone the repository:
```bash
cd /Users/vlad/Projects/modern_turkmen_audio
```

2. Create and activate virtual environment:
```bash
python3 -m venv tts-env
source tts-env/bin/activate
```

3. Install dependencies:
```bash
pip install torch transformers streamlit scipy
```

4. (Optional) Install FFmpeg for MP3 support:
```bash
brew install ffmpeg  # macOS
```

## Usage

### Web Interface

Run the Streamlit web application:

```bash
streamlit run text-speech.py
```

The app will open in your default browser. Simply:
1. Enter Turkmen text in Latin script
2. Click "Сгенерировать речь" (Generate Speech)
3. Listen to the generated audio
4. Download the audio file if needed

### Command-line Interface

Convert text to speech from the command line:

```bash
python turkmen_tts.py "Salam, näme edýäňiz?"
```

Specify custom output filename:

```bash
python turkmen_tts.py "Türkmen dili gowy däl" -o greeting.mp3
```

By default, the output filename is automatically generated from the first 3 words of the input text.

## Project Structure

```
modern_turkmen_audio/
├── text-speech.py      # Streamlit web application
├── turkmen_tts.py      # Command-line TTS tool
├── tts-env/            # Python virtual environment
└── README.md           # This file
```

## Model Information

This project uses the [facebook/mms-tts-tuk-script_latin](https://huggingface.co/facebook/mms-tts-tuk-script_latin) model from Hugging Face:

- **Model**: MMS-TTS (Massively Multilingual Speech)
- **Language**: Turkmen (tuk)
- **Script**: Latin
- **Provider**: Meta AI (Facebook)

## Supported Text

The model accepts Turkmen text written in Latin script. For best results:
- Use standard Turkmen Latin alphabet
- Include proper punctuation
- Avoid mixing scripts or languages

## Examples

**Command-line:**
```bash
python turkmen_tts.py "Men Türkmenistandan gelýärin"
python turkmen_tts.py "Hoş gördük" -o welcome.wav
```

**Web Interface:**
Simply enter text like "Salam, ýagdaýyňyz nähili?" and click generate.

## Output

- **Default format (CLI)**: MP3 (falls back to WAV if FFmpeg not available)
- **Web interface**: WAV format
- **Sampling rate**: 16kHz (model default)

## Troubleshooting

**Issue**: Model download fails  
**Solution**: Ensure you have internet connection. The model will be downloaded automatically on first run.

**Issue**: FFmpeg not found  
**Solution**: MP3 output requires FFmpeg. Install it or the tool will save as WAV instead.

**Issue**: Out of memory  
**Solution**: Try shorter text inputs or use a machine with more RAM.

## License

This project uses the MMS-TTS model from Meta AI. Please refer to the [model card](https://huggingface.co/facebook/mms-tts-tuk-script_latin) for model licensing information.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- Meta AI for the MMS-TTS model
- Hugging Face for model hosting and Transformers library
- Streamlit for the web framework
