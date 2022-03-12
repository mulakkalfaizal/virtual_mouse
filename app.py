import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from pynput.mouse import Button, Controller
import time

wCam, hCam = 640, 480
pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mouse = Controller()
detector = HandDetector(detectionCon=0.8, maxHands=1)

wScr, hScr = 2880, 1800
frameR = 100
smoothening = 5
plocX, plocY = 0, 0
cloxX, clocY = 0, 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # print(len(hands))
    if len(hands) != 0:
        # print(detector.fingersUp(hands[0]))
        lmlist = hands[0]["lmList"]
        x1, y1 = lmlist[8][0:2]
        x2, y2 = lmlist[12][0:2]

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0]:
            print("Moving mode activated")

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # print(f'{x1=} => {x3=}')
            # print(f'{y1=} => {y3=}')

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # move mouse to right when i move hand right and left when left
            mouse.position = (wScr - clocX, clocY)

            # Draw a cricle on the index finger tip
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            plocX, plocY = clocX, clocY

        if detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:
            print("Clicking Mode activated")

            length, info, img = detector.findDistance(lmlist[8][0:2], lmlist[12][0:2], img)
            # print(length)
            if length < 35:
                print("Clicking ..")
                #mouse.click(Button.left, 2)
        #
        #
        #     ix1, iy1 = lmlist[8][0:2]
        #     mx1, my1 = lmlist[12][0:2]
        #
        #     print(f"Index finger Lm: x ->{ix1} :: y->{iy1}")
        #     print(f"Middle finger Lm: x ->{mx1} :: y->{my1}")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
