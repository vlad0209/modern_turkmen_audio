import argparse
from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
import numpy as np
import tempfile
import os

def generate_default_filename(text):
    """Generate default filename from first 3 words of input text."""
    words = text.split()[:3]
    filename = "_".join(word.lower() for word in words)
    # Remove any characters that might be problematic in filenames
    filename = "".join(c for c in filename if c.isalnum() or c in "_-")
    return f"{filename}.mp3" if filename else "output.mp3"

def main():
    parser = argparse.ArgumentParser(description='Convert Turkmen text to speech using MMS-TTS model')
    parser.add_argument('text', help='Turkmen text to convert to speech')
    parser.add_argument('-o', '--output', help='Output MP3 file name (default: based on first 3 words of input)')
    
    args = parser.parse_args()
    
    # Generate default filename if not provided
    if not args.output:
        args.output = generate_default_filename(args.text)
    
    print(f"Loading MMS-TTS Turkmen model...")
    model = VitsModel.from_pretrained("facebook/mms-tts-tuk-script_latin")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tuk-script_latin")
    
    print(f"Converting text to speech: '{args.text}'")
    inputs = tokenizer(args.text, return_tensors="pt")
    
    with torch.no_grad():
        output = model(**inputs).waveform
    
    # Convert tensor to numpy array and save
    waveform = output.squeeze().cpu().numpy()
    
    # Determine output format and filename
    output_file = args.output
    if not output_file.endswith(('.mp3', '.wav')):
        output_file += '.mp3'
    
    if output_file.endswith('.mp3'):
        # Try to create MP3 using FFmpeg via temporary WAV
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav.close()
        
        try:
            # Save as WAV first using scipy
            scipy.io.wavfile.write(temp_wav.name, model.config.sampling_rate, waveform)
            
            # Convert WAV to MP3 using ffmpeg
            cmd = f'ffmpeg -i "{temp_wav.name}" -codec:a mp3 -b:a 128k "{output_file}" -y -loglevel quiet'
            result = os.system(cmd)
            
            if result == 0:
                print(f"Audio saved to: {output_file}")
            else:
                print("FFmpeg not available. Saving as WAV instead...")
                wav_output = output_file.replace('.mp3', '.wav')
                scipy.io.wavfile.write(wav_output, model.config.sampling_rate, waveform)
                print(f"Audio saved to: {wav_output}")
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_wav.name):
                os.unlink(temp_wav.name)
    else:
        # Save directly as WAV
        scipy.io.wavfile.write(output_file, model.config.sampling_rate, waveform)
        print(f"Audio saved to: {output_file}")

if __name__ == "__main__":
    main()

