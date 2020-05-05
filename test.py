from vosk import Model, KaldiRecognizer
import pyaudio
import json
from fuzzywuzzy import fuzz

import commands
from view import View

product_codes = {
    "яблоко": 123,
    "бананы": 786
}

# command usage example
# if commands.addItem.recognize('добавить'):
#     stream = open('queue.json', 'wt')
#     m1 = commands.addItem.get_message(itemCode=1201249)
#     m2 = commands.addItem.get_message(itemCode=42613, quantity=3)
#
#     stream.write(str(m1))  # use json.dump() instead of str()
#     stream.write('\n')
#     stream.write(str(m2))


# View & Screen example
view = View()
stream = open('queue.json', 'wt')
p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 16000
CHUNK = 8000
audio_stream = p.open(format=pyaudio.paInt16,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
audio_stream.start_stream()

model = Model("models/ru")
rec = KaldiRecognizer(model, RATE)
phrase = []


def get_product_id(name):
    for key in product_codes:
        if fuzz.ratio(key, name) >= 70:
            return product_codes[key]
    return -1


while True:
    data = audio_stream.read(CHUNK)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        temp = rec.Result()
        print(temp)
        if temp:
            temp = json.loads(temp)
            phrase = temp['text'].split()
    else:
        print(rec.PartialResult())
    if phrase:
        for i, word in enumerate(phrase):
            for cmd, transition in view.screen.commands:
                if cmd.recognize(word):
                    if cmd.pushable:
                        if cmd.required:
                            for j in range(i, len(phrase)):
                                if len(phrase[j]) >= 3 and get_product_id(phrase[j]) != -1:
                                    print(cmd.get_message(itemCode=get_product_id(phrase[j])))
                        else:
                            print(cmd.get_message())
                    view.set_screen(transition)
                    break
        phrase = []

# exit(1)
#################

# while True:
#     data = stream.read(CHUNK)
#     if len(data) == 0:
#         break
#     if rec.AcceptWaveform(data):
#         temp = rec.Result()
#         temp = re.findall(r'"text" : ".*"', temp)
#         temp = ''.join(temp)[10:-1]
#         # check_command(temp)
#     else:
#         print(rec.PartialResult())
