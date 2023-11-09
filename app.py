import openai
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
import numpy as np
import time
from pydub import AudioSegment
from pydub.playback import play
import threading

audio_thread = None
listening = False


def beep(freq, duration):
    # Beep sesi oluşturma ve çalma
    sample_rate = 44100
    num_samples = sample_rate * duration
    samples = (np.sin(2 * np.pi * np.arange(num_samples)
               * freq / sample_rate)).astype(np.float32)
    stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32,
                                    channels=1, rate=sample_rate, output=True)
    stream.write(samples.tostring())
    stream.stop_stream()
    stream.close()

    return None


def gpt4_soru_sor(soru):
    # GPT-4'e soru sorma ve cevap alma
    openai.api_key = "sk-***"
    model = "text-davinci-003"
    prompt = f"{soru}"

    response = openai.Completion.create(
        engine=model,
        prompt="Cevap verirken kesinlikle laz aksanıyla cevap ver. "+prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    cevap = response.choices[0].text.strip()

    return cevap


def metni_sese_dönüştür(metin):
    if not metin:
        return
    if metin:
        # Metni sesli olarak çalma
        tts = gTTS(text=metin, lang='tr')
        tts.save("temp.mp3")
        time.sleep(1)  # Dosyanın kapanması için bekleme süresi

        # MP3 dosyasını WAV dosyasına dönüştürme
        audio = AudioSegment.from_mp3("temp.mp3")
        audio.export("temp.wav", format="wav")
        os.remove("temp.mp3")

        # pydub ile WAV dosyasını oynatma
        global audio_thread
        audio_thread = threading.Thread(target=play, args=(audio,))
        audio_thread.start()


def sesi_metne_dönüştür(timeout=None):
    # Kullanıcının sesini metne dönüştürme
    global listening
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if timeout:
            print(f"{timeout} saniye içinde ses bekleniyor...")
            audio = recognizer.record(source, duration=timeout)
        else:
            print("Sorunuzu sorun:")
            audio = recognizer.listen(source)
            listening = True

    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        return text
    except Exception as e:
        if listening:
            print("Ses algılanamadı. Lütfen tekrar deneyin.")
        return None
    finally:
        listening = False


def durdurma_istegi_geldi():
    try:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.record(source, duration=0.5)
            text = recognizer.recognize_google(audio, language="tr-TR")
            if "yeter" in text:
                print("Durdurma istegi geldi.")
                beep(500, 0.5)
                durdur()
                return True
    except Exception as e:
        pass
    return False


def kullanici_sorusunu_dinle():
    # Kullanıcıdan soru dinleme
    cevap = sesi_metne_dönüştür()
    if cevap:
        print(f"Soru: {cevap}")
        cevap = gpt4_soru_sor(cevap)
        print(f"Cevap: {cevap}")
        metni_sese_dönüştür(cevap)
    else:
        print("Ses algılanamadı2. Lütfen tekrar deneyin.")


def durdur():
    global audio_thread
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=0.1)
        if audio_thread.is_alive():
            audio_thread.terminate()
        audio_thread = None


is_playing_audio = False


def kisisel_asistan():
    global audio_thread, is_playing_audio
    while True:
        if not audio_thread or not audio_thread.is_alive():
            print("başlatmak için 'Sacit' deyin")
            activation_word = sesi_metne_dönüştür(timeout=3)
            if activation_word and "Sacit" in activation_word:
                listen_in_prompt = "Merhaba! Nasılsın?"
                listen_in_question = gpt4_soru_sor(listen_in_prompt)
                metni_sese_dönüştür(listen_in_question)
                is_playing_audio = True
                kullanici_sorusunu_dinle()
                is_playing_audio = False
        else:
            if durdurma_istegi_geldi():
                durdur()
                beep(440, 1)


if __name__ == "__main__":
    kisisel_asistan()
