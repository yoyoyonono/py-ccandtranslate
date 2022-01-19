import speech_recognition as sr

for x,y in enumerate(sr.Microphone.list_microphone_names()):
    print(x,y)