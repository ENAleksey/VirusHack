from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import datetime as dt
from fuzzywuzzy import fuzz
import pyaudio


class Command:
    def __init__(self, synonyms, action, stream):
        self.synonyms = synonyms
        self.action = action
        self.stream = stream

    @staticmethod
    def get_eventID():
        return "sco" + str(dt.datetime.now().timestamp())

    def form_message(self):
        message = {
            "action": self.action,
            "eventId": self.get_eventID()
        }
        return message

    def recognize(self, phrase):
        for word in self.synonyms:
            if fuzz.ratio(word, phrase) >= 75:
                print(fuzz.ratio(word, phrase))
                return True
        return False


class addItem(Command):
    def form_message(self, params):
        message = Command.form_message(self)
        message['itemCode'] = params['itemCode'] if 'itemCode' in params else -1
        message['quantity'] = params['quantity'] if 'quantity' in params else 1
        return message


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model("models/ru")
rec = KaldiRecognizer(model, 16000)
pr = ""
while True:
    data = stream.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        temp = rec.Result()
        temp = temp[temp.find("text"):]
        temp = temp[temp.find(":") + 3:]
        pr = temp[:temp.find(r'"')]
        print(pr)
    else:
        print(rec.PartialResult())

print(rec.FinalResult())
test = addItem(['жили', 'хусев'], 'addItem', '')
pr = pr.split()
for p in pr:
    if test.recognize(p):
        print(test.form_message({'itemCode': 123}))
