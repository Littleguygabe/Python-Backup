#https://www.youtube.com/watch?v=C_5L2H41u-M

from turtle import width
import webbrowser
from cv2 import COLOR_BGR2HSV
import numpy as np
import cv2
from win32api import GetSystemMetrics
from mss import mss
from time import time
import pyautogui

webbrowser.open_new_tab('https://chromedino.com/color/')

lower = np.array([7,50,20])
upper = np.array([15,250,255])

lower2 = np.array([40,50,20])
upper2 = np.array([80,250,255])
 
w_max = GetSystemMetrics(0)
h_max = GetSystemMetrics(1)
 
sct = mss()    

xpos = 212
ypos = 616
height = 110
width = 672
loop_time = time()
while(True):
    bbox = {'top': xpos, 'left':ypos, 'width': width, 'height': height} # setting the boundary box
    screen = sct.grab(bbox) 
    screen_np = np.array(screen)

    #mask for dino
    mask_hsv_dino = cv2.cvtColor(screen_np, COLOR_BGR2HSV)
    dino_binary_mask = cv2.inRange(mask_hsv_dino, lower, upper)

    mask_hsv_cactus = cv2.cvtColor(screen_np, COLOR_BGR2HSV)
    cactus_binary_mask = cv2.inRange(mask_hsv_cactus, lower2, upper2)

    contours_dino, hierarchy_dino = cv2.findContours(dino_binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len!=0:
        for contour_dino in contours_dino:
            if cv2.contourArea(contour_dino) > 500:
                x, y, w, h = cv2.boundingRect(contour_dino)
                cv2.rectangle(screen_np , (x,y), (x+w, y+h), (0, 0, 255), 3)

    contours_cactus, hierarchy_cactus = cv2.findContours(cactus_binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len!=0:
        for contour_cactus in contours_cactus:
            if cv2.contourArea(contour_cactus) > 500:
                x, y, w, h = cv2.boundingRect(contour_cactus)
                cv2.rectangle(screen_np , (x,y), (x+w, y+h), (0, 255, 100), 3)

    # show the dinosaur binary mask
    cv2.imshow('dino binary mask', dino_binary_mask)

    # show the original screen capture
    cv2.imshow('original', screen_np)

    # show the cactus binary mask
    cv2.imshow('cactus binary mask', cactus_binary_mask)

    keyboard = cv2.waitKey(1) & 0xFFc


    keyboard = cv2.waitKey(1) & 0xFF

    # show current mask fps
    #print('FPS {}'.format(1 / time() - loop_time))
    #loop_time = time()

    for i in range(145,155):  # horizontal check
        pixel = cactus_binary_mask[90,i]  # [y , x]
        if pixel != 0:
            print('pixel detected @ 90, ' + str(i))
            pyautogui.press('space')

    if cv2.waitKey(25) & 0xFF == ord('x'):
        cv2.destroyAllWindows()
        break
