import os
import sys
import json
import pyaudio
import pyautogui
import openai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import multiprocessing
from commands import VoiceCommand


def gpt4_soru_sor(soru):
    openai.api_key = "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"
    prompt = f"{soru}"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=1,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    cevap = response.choices[0].message.content.strip()

    return cevap


def text_to_speech(text):
    # Türkçe dil desteği için tr parametresi kullanılıyor
    tts = gTTS(text=text, lang="tr")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)


class RealTimeSpeechRecognition:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def start(self):
        print("Mikrofonu dinliyorum...")

        try:
            soru_bekleme_modu = False
            soru_metni = ""
            with sr.Microphone() as source:
                while True:
                    audio_data = self.recognizer.listen(
                        source, timeout=2, phrase_time_limit=4)
                    try:
                        text = self.recognizer.recognize_google(
                            audio_data, language="tr")
                        print("Söylediğiniz:", text)
                        print("Soru Bekleme:", soru_bekleme_modu)

                        if text.lower().startswith("soru soruyorum"):
                            print("Soru Bekleme Modu Açılıyor...")
                            soru_bekleme_modu = True
                            soru_metni = ""
                        elif soru_bekleme_modu:
                            if text:
                                soru_metni += " " + text
                                cevap = gpt4_soru_sor(soru_metni)
                                print("GPT-3.5-turbo'nun cevabı:", cevap)
                                text_to_speech_process = multiprocessing.Process(
                                    target=text_to_speech, args=(cevap,))
                                text_to_speech_process.start()
                                soru_bekleme_modu = False
                        else:
                            voice_command = VoiceCommand(text)
                            voice_command.handle_command()
                    except sr.UnknownValueError:
                        print("Konuşma algılanmadı.")
                    except sr.RequestError as e:
                        print(
                            f"Google Speech Recognition API'den hata alındı: {e}")

        except KeyboardInterrupt:
            print("Programdan çıkılıyor...")


if __name__ == "__main__":
    real_time_speech_recognition = RealTimeSpeechRecognition()
    real_time_speech_recognition.start()
