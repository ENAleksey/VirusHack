from vosk import Model, KaldiRecognizer
import datetime as dt
from fuzzywuzzy import fuzz
import pyaudio
import re


class Command:
    def __init__(self, synonyms, action, writing_stream):
        self.synonyms = synonyms
        self.action = action
        self.stream = writing_stream

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
            if fuzz.ratio(word, phrase) >= 80:
                return True
        return False


class addItem(Command):
    def form_message(self, params):
        message = Command.form_message(self)
        message['itemCode'] = params.get('itemCode') or -1
        message['quantity'] = params.get('quantity') or 1
        return message


class addLoyalty(Command):
    def form_message(self, params):
        message = Command.form_message(self)
        message['itemCode'] = params.get('itemCode') or -1
        message['type'] = params.get('type') or -1
        return message


class cancel(Command):
    def form_message(self, params):
        message = Command.form_message(self)
        return message


def check_command(phrase):
    test = addItem(['добавить', 'добавь'], 'addItem', '')
    phrase = phrase.split()
    for word in phrase:
        if test.recognize(word):
            print(test.form_message({'itemCode': 123}))
    return


p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 16000
CHUNK = 8000
stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream.start_stream()

model = Model("models/ru")
rec = KaldiRecognizer(model, RATE)
while True:
    data = stream.read(CHUNK)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        temp = rec.Result()
        temp = re.findall(r'"text" : ".*"', temp)
        temp = ''.join(temp)[10:-1]
        check_command(temp)
    else:
        print(rec.PartialResult())
