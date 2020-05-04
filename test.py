from vosk import Model, KaldiRecognizer
import pyaudio
import re

import commands

# command usage example
if commands.addItem.recognize('добавить'):
    stream = open('queue.json', 'wt')
    m1 = commands.addItem.get_message(itemCode=1201249)
    m2 = commands.addItem.get_message(itemCode=42613, quantity=3)

    stream.write(str(m1))  # use json.dump() instead of str
    stream.write('\n')
    stream.write(str(m2))


p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 16000
CHUNK = 8000
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
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
        # check_command(temp)
    else:
        print(rec.PartialResult())
