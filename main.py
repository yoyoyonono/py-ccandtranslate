import threading
import deep_translator as dt
import speech_recognition as sr
import threading

my_voice_recognizer = sr.Recognizer()
others_recognizer = sr.Recognizer()

my_microphone = sr.Microphone(device_index=2)
others_microphone = sr.Microphone(device_index=15)
translator = dt.GoogleTranslator()

destination_langauge_translators = [dt.GoogleTranslator(target=x) for x in ('en', 'zh-tw', 'id', 'ja')]

def recognize(recognizer: sr.Recognizer, microphone: sr.Microphone, callback: callable, callback_agrs: tuple):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source=source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=30)
                callback(recognizer.recognize_google(audio), *callback_agrs)
            except Exception as e:
                print(e)

def translate(text: str, prefix: str, file_name: str):
    with open(file_name, 'w', encoding='utf-8') as f:
        for translator in destination_langauge_translators:
            print(f'{prefix}[{translator._target}]: {translator.translate(text=text)}', file=f)
    print(f'{prefix} translated')


my_thread = threading.Thread(target=recognize, args=(my_voice_recognizer,my_microphone, translate, ('me', 'my.txt')))
others_thread = threading.Thread(target=recognize, args=(others_recognizer,others_microphone, translate, ('others', 'others.txt')))

my_thread.start()
others_thread.start()