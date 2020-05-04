import cv2
import numpy as np
import math



learningRate = 0



def isHandInRect(frame, x, y, w, h):
    crop_img = frame[y:y+h, x:x+w]

    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (35, 35), 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cv2.imshow(str("{} {} {} {}").format(x, y, w, h), thresh1)

    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
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


def getRectIdFromHandPos(frame, w, h):
    if isHandInRect(frame, 0, 0, 200, 200):
        return 0
    elif isHandInRect(frame, w-200, 0, 200, 200):
        return 1
    elif isHandInRect(frame, 0, h-200, 200, 200):
        return 2
    elif isHandInRect(frame, w-200, h-200, 200, 200):
        return 3
    else:
        return None


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res