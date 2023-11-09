import pyautogui
import webbrowser
import subprocess


class VoiceCommand:

    def __init__(self, text):
        self.text = text.lower()

    def handle_command(self):
        if "müzik" in self.text:
            self.play_pause_music()
        if "masaüstü" in self.text:
            self.show_desktop()
        if "sesi artır" in self.text:
            self.increase_volume()
        if "sesi azalt" in self.text:
            self.decrease_volume()
        if "yazılım geliştirmeye başlayalım" in self.text:
            self.yazilim_geliştirmeye_baslayalim()
        if "ekşi" in self.text and "aç" in self.text:
            self.open_eksisozluk()

    def play_pause_music(self):
        pyautogui.press("playpause")
        print("Müzik durduruldu/başlatıldı.")

    def show_desktop(self):
        pyautogui.hotkey("win", "d")
        print("Masaüstü Win+D etkinleştirildi.")

    def increase_volume(self):
        pyautogui.press("volumeup")
        print("Ses seviyesi artırıldı.")

    def decrease_volume(self):
        pyautogui.press("volumedown")
        print("Ses seviyesi azaltıldı.")

    def mute_unmute_volume(self):
        pyautogui.press("volumemute")
        print("Ses açıldı/kapatıldı.")

    def open_eksisozluk(self):
        webbrowser.open("https://www.eksisozluk2023.com", new=2)
        print("Ekşi Sözlük yeni sekmede açıldı.")

    def yazilim_geliştirmeye_baslayalim(self):
        try:
            subprocess.Popen("code")
            print("Visual Studio Code açıldı.")
        except Exception as e:
            print(f"Visual Studio Code açılırken hata oluştu: {e}")
