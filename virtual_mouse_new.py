import time

import autopy
import cv2
import numpy as np
import pyautogui

import new_detect as nd

##########################
wCam, hCam = 640, 480
frameR = 100          # frame reduction (active area inside the camera frame)
smoothening = 7
clickDist = 40        # pinch distance (px) that counts as a click
clickDelay = 0.4      # seconds between clicks
scrollAmount = 40     # bigger = faster scrolling
scrollDelay = 0.08    # seconds between scroll steps
##########################

# pyautogui's failsafe aborts the program when the cursor hits a screen corner,
# which can easily happen when you steer the cursor with your hand.
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
lastClick = 0
lastScroll = 0

cap = cv2.VideoCapture(1)  # use 0 if your default camera is the one you want
cap.set(3, wCam)
cap.set(4, hCam)
detector = nd.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    if not success:
        continue
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)
    mode = ""

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # index fingertip

        # 2. Check which fingers are up (thumb is ignored, it is unreliable)
        fingers = detector.fingersUp()
        now = time.time()

        # 3. Only index finger up: move mode
        if fingers[1:] == [1, 0, 0, 0]:
            mode = "Move"
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # clamp so autopy never gets an out-of-bounds point
            mx = min(max(wScr - clocX, 0), wScr - 1)
            my = min(max(clocY, 0), hScr - 1)
            autopy.mouse.move(mx, my)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 4. Index + middle up: click mode (pinch the two fingertips together)
        elif fingers[1:] == [1, 1, 0, 0]:
            mode = "Click"
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < clickDist:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                if now - lastClick > clickDelay:
                    autopy.mouse.click()
                    lastClick = now

        # 5. Three fingers up: scroll up
        elif fingers[1:] == [1, 1, 1, 0]:
            mode = "Scroll Up"
            if now - lastScroll > scrollDelay:
                pyautogui.scroll(scrollAmount)
                lastScroll = now

        # 6. Four fingers up: scroll down
        elif fingers[1:] == [1, 1, 1, 1]:
            mode = "Scroll Down"
            if now - lastScroll > scrollDelay:
                pyautogui.scroll(-scrollAmount)
                lastScroll = now

    # 7. Frame rate and current mode
    cTime = time.time()
    fps = 1 / max(cTime - pTime, 1e-6)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cv2.putText(img, mode, (20, hCam - 20), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 2)

    # 8. Display, press ESC to quit
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()