from hand_tracking import HandTracker
import cv2
import commands
from view import View, addItemScreen, paymentScreen
import time
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from fuzzywuzzy import fuzz


view = View()
handTracker = HandTracker(1, False)
camera = cv2.VideoCapture(0)
width = int(camera.get(3))
height = int(camera.get(4))
prevRectId = None
currTime = None
endTime = None
p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 16000
CHUNK = 8000
audio_stream = p.open(format=pyaudio.paInt16,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

model = Model("models/ru")
rec = KaldiRecognizer(model, RATE)
phrase = []

product_codes = {
    "яблоко": 123,
    "бананы": 786
}

loyalty_codes = {
    "Выручайка": 67,
    "Промо": 21,
    "Скидки": 17
}


def renderDebugView(rectId):
    global camera_debug
    screens = len(view.screen.commands)
    colorRed = (0,0,255)
    colorGreen = (0,255,0)

    cv2.rectangle(camera_debug, (200,200), (000,000), colorRed, 0)
    cv2.rectangle(camera_debug, (width,200), (width-200,0), colorRed, 0)
    cv2.rectangle(camera_debug, (200,height), (0,height-200), colorRed, 0)
    cv2.rectangle(camera_debug, (width,height), (width-200,height-200), colorRed, 0)

    if screens > 0:
        cmd, transition = view.screen.commands[0]
        if cmd:
            cv2.rectangle(camera_debug, (200,200), (000,000), colorGreen, 2)
            cv2.putText(camera_debug, cmd.action, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    if screens > 1:
        cmd, transition = view.screen.commands[1]
        if cmd:
            cv2.rectangle(camera_debug, (width,200), (width-200,0), colorGreen, 2)
            cv2.putText(camera_debug, cmd.action, (10+width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    if screens > 2:
        cmd, transition = view.screen.commands[2]
        if cmd:
            cv2.rectangle(camera_debug, (200,height), (0,height-200), colorGreen, 2)
            cv2.putText(camera_debug, cmd.action, (10, 50+height-200), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    if screens > 3:
        cmd, transition = view.screen.commands[3]
        if cmd:
            cv2.rectangle(camera_debug, (width,height), (width-200,height-200), colorGreen, 2)
            cv2.putText(camera_debug, cmd.action, (10+width-200, 50+height-200), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)

    if rectId == 0:
        cv2.putText(camera_debug, "Top Left", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    elif rectId == 1:
        cv2.putText(camera_debug, "Top Right", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    elif rectId == 2:
        cv2.putText(camera_debug, "Bottom Left", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    elif rectId == 3:
        cv2.putText(camera_debug, "Bottom Right", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)
    else:
        cv2.putText(camera_debug, "Nothing", (250, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)

    cv2.imshow('Camera', camera_debug)


def recognize_voice():
    audio_stream.start_stream()
    while True:
        data = audio_stream.read(CHUNK)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            temp = rec.Result()
            print(temp)
            if temp:
                temp = json.loads(temp)
                return temp['text'].split()
        else:
            print(rec.PartialResult())


def get_product_id(name):
    for key in product_codes:
        if fuzz.ratio(key, name) >= 70:
            return product_codes[key]
    return -1


def get_loyalty_id(name):
    for key in loyalty_codes:
        if fuzz.ratio(key, name) >= 70:
            return product_codes[key]
    return -1


while(camera.isOpened()):
    cv2.imshow('view', view.im)
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    camera_debug = frame

    rectId = handTracker.getRectIdFromHandPos(frame, width, height)

    # Debug
    renderDebugView(rectId)

    if rectId is None:
        prevRectId = None
        endTime = None
    else:
        if rectId != prevRectId:
            if rectId < len(view.screen.commands):
                cmd, transition = view.screen.commands[rectId]

                # Delay
                if endTime is None:
                    currTime = time.time()
                    endTime = currTime + 0.5

                if currTime < endTime:
                    currTime = time.time()
                else:
                    view.set_screen(transition)
                    cv2.waitKey(100)
                    if cmd:
                        if cmd.action == 'addItem':
                            # распознаём
                            res = recognize_voice()
                            while not res:
                                res = recognize_voice()
                            audio_stream.stop_stream()
                            res = list(filter(lambda x: len(x) >= 3, res))
                            with open('queue.json', 'at') as f:
                                try:
                                    json.dump(cmd.get_message(itemCode=get_product_id(res[0])), f)
                                    f.write('\n')
                                except:
                                    continue
                            # cmd.get_message(code)
                            view.set_screen(addItemScreen)
                        elif cmd.action == 'addLoyalty':
                            res = recognize_voice()
                            while not res:
                                res = recognize_voice()
                            audio_stream.stop_stream()
                            res = list(filter(lambda x: len(x) >= 3, res))

                            print(cmd.get_message(itemCode=get_loyalty_id(res[0])))
                            # cmd.get_message(code)
                            view.set_screen(paymentScreen)
                        elif cmd.action == 'deletePosition':
                            pass
                        elif cmd.action == 'payment':
                            pass
                        # распознаем
                        # print(cmd.get_message()) # Крашится! Лёха, пофикси!
                    endTime = None
                    prevRectId = rectId

    key = cv2.waitKey(10)
    if key == 27:
        camera.release()
        view.destroy()
        cv2.destroyAllWindows()
        break
