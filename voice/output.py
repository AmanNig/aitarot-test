# 📁 voice/output.py
import os
from gtts import gTTS
# from playsound import playsound

def synthesize_voice(text, user_input_lang='en', filename="response_audio.mp3"):
    """
    Converts already translated (or original) text to speech using gTTS.
    """
    try:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"⚠️ Could not delete existing audio file: {e}")
                return None

        tts = gTTS(text=text, lang=user_input_lang)
        tts.save(filename)
        return filename

    except Exception as e:
        print("⚠️ Error generating voice:")
        print(e)
        return None

# def play_voice_response(audio_path):
#     """
#     Plays the audio file and handles replay logic.
#     """
#     if audio_path and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
#         playsound(audio_path)
#         while True:
#             replay = input("🔁 Do you want to replay the voice response? (y/n): ").strip().lower()
#             if replay == "y":
#                 playsound(audio_path)
#             else:
#                 break
#     else:
#         print("⚠️ Audio file not generated properly.")
