import cv2
import numpy as np
import math


camera = cv2.VideoCapture(0)
width = int(camera.get(3))
height = int(camera.get(4))
isBgCaptured = 1
bgSubThreshold = 50
learningRate = 0


def isHandInRect(frame, x, y, w, h):
    crop_img = frame[y:y+h, x:x+w]

    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (35, 35), 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cv2.imshow(str("{} {} {} {}").format(x, y, w, h), thresh1)

    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    hull = cv2.convexHull(cnt)
    hull = cv2.convexHull(cnt, returnPoints=False)

    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0

    if defects is not None:
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

            if angle <= 90:
                count_defects += 1

    return count_defects > 1


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


while(camera.isOpened()):
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    # frame = cv2.bilateralFilter(frame, 9, 350, 350)

    cv2.rectangle(frame, (200,200), (000,000), (0,255,0), 0)
    cv2.rectangle(frame, (width,height), (width-200,height-200), (0,255,0), 0)
    cv2.rectangle(frame, (200,height), (0,height-200), (0,255,0), 0)
    cv2.rectangle(frame, (width,200), (width-200,0), (0,255,0), 0)

    if isBgCaptured == 1:
        # frame = removeBG(frame)

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.GaussianBlur(frame, (5, 5), 0)
        # _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        if isHandInRect(frame, 0, 0, 200, 200):
            cv2.putText(frame,"Top Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        elif isHandInRect(frame, width-200, 0, 200, 200):
            cv2.putText(frame,"Top Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        elif isHandInRect(frame, 0, height-200, 200, 200):
            cv2.putText(frame,"Bottom Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        elif isHandInRect(frame, width-200, height-200, 200, 200):
            cv2.putText(frame,"Bottom Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        else:
            cv2.putText(frame,"Nothing", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)

    cv2.imshow('Main', frame)

    k = cv2.waitKey(10)
    if k == 27:
        camera.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('b'):
        # bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1