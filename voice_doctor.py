import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text,output_filepath):
    language="en"
    
    audioobj=gTTS(
        text=input_text,
        lang=language,
        slow=False

    )
    audioobj.save(output_filepath)

input_text="Hi, this is a test of the text to speech conversion using gTTS. "
# text_to_speech_with_gtts(input_text,"output.mp3")


#step2: setup text to speech using ElevenLabs
from dotenv import load_dotenv

load_dotenv()




from gtts import gTTS
from pydub import AudioSegment
import platform
import subprocess

def text_to_speech_with_gtts(input_text, output_filepath_mp3):
    # Step 1: Generate MP3 from text
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath_mp3)

    # Step 2: Convert MP3 to WAV
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(output_filepath_mp3)
    sound.export(output_filepath_wav, format="wav")

    # Step 3: Play WAV based on OS
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.run([
                "powershell",
                "-c",
                f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'
            ])
        elif os_name == "Darwin":
            subprocess.run(["afplay", output_filepath_wav])
        elif os_name == "Linux":
            subprocess.run(["aplay", output_filepath_wav])
        else:
            raise OSError("Unsupported operating system.")
    except Exception as e:
        print(f"❌ Audio playback failed: {e}")

# Test it
# text_to_speech_with_gtts("Hello from AI with Hassan!", "voice_test.mp3")
