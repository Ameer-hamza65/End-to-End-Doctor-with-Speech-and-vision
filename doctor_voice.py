import os
from gtts import gTTS
import subprocess
import platform

def text_to_speech(input_text, output_file_path):
    audio = gTTS(text=input_text, lang='en', slow=False)
    mp3_path = output_file_path
    wav_path = "gtts_testing_autoplay.wav"  # Convert MP3 to WAV for PowerShell
    
    # Save MP3 file
    audio.save(mp3_path)
    
    # Convert MP3 to WAV (Windows fix)
    os_name = platform.system()
    if os_name == "Windows":
        try:
            subprocess.run(["ffmpeg", "-i", mp3_path, wav_path, "-y"], check=True)
            output_file_path = wav_path  # Use WAV file instead
        except Exception as e:
            print(f"Error converting MP3 to WAV: {e}")
    
    # Play the audio
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", output_file_path])
        elif os_name == "Windows":  # Windows (Now uses WAV file)
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{output_file_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(["mpg123", output_file_path])  # Alternative: 'ffplay', 'aplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Test the function
text = "Hi, my name is Ameer Hamza."
text_to_speech(input_text=text, output_file_path="gtts_testing_autoplay.mp3")
