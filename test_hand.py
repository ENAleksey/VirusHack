from hand_tracking import getRectIdFromHandPos 
import cv2
import commands
from view import View

# camera = cv2.VideoCapture("http://192.168.100.12:8080/video")
camera = cv2.VideoCapture(0)
width = int(camera.get(3))
height = int(camera.get(4))
view = View()

prevRectId = None
prevScreen = None

isBgCaptured = 0
bgSubThreshold = 50
j=0


print("\nТекущий экран: " + view.screen.name)
for cmd, transition in view.screen.commands:
    print(cmd.action + " " + transition.name if transition else "None")

while(camera.isOpened()):
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    # frame = cv2.bilateralFilter(frame, 9, 350, 350)

    # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # if(j==0):
    #     bg=frame.copy().astype("float")
    # if(j<30):
    #     cv2.accumulateWeighted(frame,bg,0.5)
    #     j=j+1
    # frame=cv2.absdiff(frame,bg.astype("uint8"))
    
    # thre,frame=cv2.threshold(frame,25,255,cv2.THRESH_BINARY)

    # if isBgCaptured == 1:
        # frame = removeBG(frame)

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.GaussianBlur(frame, (5, 5), 0)
        # _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    rectId = getRectIdFromHandPos(frame, width, height)
    if rectId is not None:
        if rectId != prevRectId:
            prevRectId = rectId
            if rectId < len(view.screen.commands):
                cmd, transition = view.screen.commands[rectId]
                if transition:
                    print()
                    view.set_screen(transition)
                    print("Текущий экран: " + view.screen.name)
                    for cmd, transition in view.screen.commands:
                        print(cmd.action + " " + transition.name if transition else "None")

    # if rectId == 0:
    #     cv2.putText(frame,"Top Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    # elif rectId == 1:
    #     cv2.putText(frame,"Top Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    # elif rectId == 2:
    #     cv2.putText(frame,"Bottom Left", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    # elif rectId == 3:
    #     cv2.putText(frame,"Bottom Right", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)
    # else:
    #     cv2.putText(frame,"Nothing", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, 2)

    cv2.imshow('Main', frame)
    cv2.rectangle(frame, (200,200), (000,000), (0,255,0), 0)
    cv2.rectangle(frame, (width,height), (width-200,height-200), (0,255,0), 0)
    cv2.rectangle(frame, (200,height), (0,height-200), (0,255,0), 0)
    cv2.rectangle(frame, (width,200), (width-200,0), (0,255,0), 0)

    k = cv2.waitKey(10)
    if k == 27:
        camera.release()
        cv2.destroyAllWindows()
        break
    # elif k == ord('b'):
        # bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        # isBgCaptured = 1