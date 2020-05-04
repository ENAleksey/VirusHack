from hand_tracking import HandTracker
import cv2
import commands
from view import View
import time


view = View()
handTracker = HandTracker(1, True)
camera = cv2.VideoCapture(0)
width = int(camera.get(3))
height = int(camera.get(4))
prevRectId = None
currTime = None
endTime = None


def renderDebugView(rectId):
    screens = len(view.screen.commands)
    colorRed = (0,0,255)
    colorGreen = (0,255,0)

    cv2.rectangle(camera_debug, (200,200), (000,000), colorRed, 0)
    cv2.rectangle(camera_debug, (width,200), (width-200,0), colorRed, 0)
    cv2.rectangle(camera_debug, (200,height), (0,height-200), colorRed, 0)
    cv2.rectangle(camera_debug, (width,height), (width-200,height-200), colorRed, 0)

    if screens > 0:
        cmd, transition = view.screen.commands[0]
        cv2.putText(camera_debug, cmd.action, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        cv2.rectangle(camera_debug, (200,200), (000,000), colorGreen, 2)

    if screens > 1:
        cmd, transition = view.screen.commands[1]
        cv2.putText(camera_debug, cmd.action, (50+width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        cv2.rectangle(camera_debug, (width,200), (width-200,0), colorGreen, 2)

    if screens > 2:
        cmd, transition = view.screen.commands[2]
        cv2.putText(camera_debug, cmd.action, (50, 50+height-200), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        cv2.rectangle(camera_debug, (200,height), (0,height-200), colorGreen, 2)

    if screens > 3:
        cmd, transition = view.screen.commands[3]
        cv2.putText(camera_debug, cmd.action, (50+width-200, 50+height-200), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
        cv2.rectangle(camera_debug, (width,height), (width-200,height-200), colorGreen, 2)

    if rectId == 0:
        cv2.putText(camera_debug, "Top Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    elif rectId == 1:
        cv2.putText(camera_debug, "Top Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    elif rectId == 2:
        cv2.putText(camera_debug, "Bottom Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    elif rectId == 3:
        cv2.putText(camera_debug, "Bottom Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    else:
        cv2.putText(camera_debug, "Nothing", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)

    cv2.imshow('Camera', camera_debug)


print("\nТекущий экран: " + view.screen.name)
for cmd, transition in view.screen.commands:
    print(cmd.action + " - " + transition.name if transition else "None")

while(camera.isOpened()):
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    camera_debug = frame

    rectId = handTracker.getRectIdFromHandPos(frame, width, height)

    # Debug
    renderDebugView(rectId)

    if rectId is not None:
        if rectId != prevRectId:
            # prevRectId = rectId
            if rectId < len(view.screen.commands):
                cmd, transition = view.screen.commands[rectId]
                if transition:
                    # Delay
                    if endTime is None:
                        currTime = time.time()
                        endTime = currTime + 0.5

                    if currTime < endTime:
                        currTime = time.time()
                    else:
                        print()
                        view.set_screen(transition)
                        for cmd, transition in view.screen.commands:
                            print(cmd.action + " - " + transition.name if transition else "None")
                        endTime = None
                        prevRectId = rectId

    key = cv2.waitKey(10)
    if key == 27:
        camera.release()
        view.destroy()
        cv2.destroyAllWindows()
        break