from curses import window
import cv2
import os
import pyautogui
from time import time
from windowcapture import WindowCapture

window_captured = 'main.py - code - Visual Studio Code'

wincap = WindowCapture(window_captured)

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot(window_captured)

    cv2.imshow('screenshot', screenshot)

    print('FPS {}'.format(1 / time() - loop_time))
    loop_time = time()

    if cv2.waitKey(25) & 0xFF == ord('x'):
        cv2.destroyAllWindows()
        break

