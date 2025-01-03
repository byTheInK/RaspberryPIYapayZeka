import os
import json
import re
from time import sleep
from subprocess import DEVNULL, run
import MODULES.AI as AI
from MODULES.VOICE import voice
import distro

WINDOWS = os.name == "nt"
CLEAR_PREFIX = "cls" if WINDOWS else "clear"

SES_KAYIT_KAYIT_SURESI: int = 6 # Saniye biçiminde bir tam sayı giriniz VARSAYILAN = 6
SES_KAZANC_BOYUTU: int = 10 # Sesin ne kadar yükseleceğini belirler VARSAYILAN = 10
SES_FREKANS_DEGERI: int = 44100 # Sesin frekansını belirler VARSAYILAN DEĞER = 44100
BASLANGICTA_HAFIZAYI_SIL: bool = False # Kod başladığında hafızayı siler veya silmez(False=hayır,True=evet) VARSAYILAN = False
HAFIZAYI_AKILDA_TUTMA_SINIRI: bool = 2000 # Aklında en son kaç mesajı tutabileceğini ayarlar VARSAYILAN = 20
HATA_AYIKLAMA: bool = False # Hata ayıklama modunu açar veya kapatır VARSAYILAN = False
SABIT_DEGERLER: dict = {"Language":"Türkçe"} # Buraya yapay zekanın asla unutmaması gereken değerleri yazınız

# yedek.json dosyasının üzerinde yazılır
# > # < ifadesi olduğu satırı yorum yapar yani koda etki etmez.
# BASLANGICTA_HAFIZAYI_SIL ifadesini açarsan OTHER klasöründe yedek.json dosyasının içerisinde verilerini tekrar bulabilirsin
# Hafızasında ne kadar fazla mesaj tutarsa o kadar yavaş yanıt verir ve alan kaplar
# Frekans değeriyle oynarsanız yapay zeka sesi anlamayabilir bu nedenle 44100 değerinde tutulması önerilir
with open("API", "r") as file:
    GROQ_API_KEY = file.read()
    print("Yapay zeka kuruldu.")

textEngine = AI.text(GROQ_API_KEY, "memory.json", SABIT_DEGERLER, HAFIZAYI_AKILDA_TUTMA_SINIRI)
voiceEngine = voice(GROQ_API_KEY)
print("OS =", "Windows" if WINDOWS else "Linux: {}".format(distro.name()))

def kill_vlc():
    if WINDOWS:
        run(["taskkill", "/F", "/IM", "vlc.exe"], check=True, stderr=DEVNULL)
    else:
        run(["pkill", "vlc"], check=True, stderr=DEVNULL)

def mainVoice():
    if BASLANGICTA_HAFIZAYI_SIL:
        with open("memory.json", "r+") as memory_file:
            memory_file_content = memory_file.read().strip()
            if memory_file_content:
                memory_data = json.loads(memory_file_content)
            else:
                memory_data = None
            with open("OTHER\\yedek.json" if WINDOWS else "OTHER/yedek.json", "w") as f:
                if memory_data is not None:
                    json.dump(memory_data, f, indent=4)
            if memory_data is not None:
                memory_file.seek(0)
                memory_file.truncate()

    while True:
        print("Ses Kaydı Başladı")
        voiceEngine.record(freq=SES_FREKANS_DEGERI, duration=SES_KAYIT_KAYIT_SURESI, volume=SES_KAZANC_BOYUTU)
        print("Ses Kaydı Bitti")

        question = voiceEngine.speechToText("SOUNDS\\tts.wav" if WINDOWS else "SOUNDS/tts.wav")

        if question == " Altyazı M.K.":
            question = ""

        print(f"Algılanan: {question}")

        response = textEngine.createResponseWithData(question, "user")
        Edited_R = re.sub(r'[^\w\s,.!?]', '', response)

        voiceEngine.textToSpeech(Edited_R, "SOUNDS\\tts.mp3")
        os.system("start SOUNDS\\tts.mp3" if WINDOWS else "vlc-wrapper --play-and-exit SOUNDS/tts.mp3")
        print("CEVAP:\n", response)

        print("SORU:\n", question)

        sleep(voiceEngine.get_length("SOUNDS\\tts.mp3"))
        kill_vlc()

if __name__ == "__main__":
    mainVoice()