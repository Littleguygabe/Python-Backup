#https://www.youtube.com/watch?v=C_5L2H41u-M

import numpy as np
import cv2
from win32api import GetSystemMetrics
from mss import mss
 
w_max = GetSystemMetrics(0)
h_max = GetSystemMetrics(1)
 
sct = mss()
 
x = 0
y = 0
h = 670
w = 600
while(True):
    bbox = {'top': x, 'left':y, 'width': w, 'height': h}
    screen = sct.grab(bbox) 
    screen_np = np.array(screen)

    hsv = cv2.cvtColor(screen_np, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([110, 170, 20]) #snake
    upper_bound = np.array([112, 175, 255]) #snake

    lower_bound2 = np.array([5, 150, 20]) #apple
    upper_bound2 = np.array([10, 230, 255]) #apple  

    snake_mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result_snake = cv2.bitwise_and(screen_np, screen_np, mask=snake_mask)

    apple_mask = cv2.inRange(hsv, lower_bound2, upper_bound2)
    result_apple = cv2.bitwise_and(screen_np, screen_np, mask=apple_mask)

    cv2.imshow('hsv', hsv)
    cv2.imshow('snake', snake_mask)
    cv2.imshow('apple', apple_mask)

    keyboard = cv2.waitKey(1) & 0xFF
 
    if keyboard == 119 and (x-10 >= 0): # w - up  
        x = x - 10
    if keyboard == 115 and (x + 10 <= h_max - h): # s - down
        x = x + 10
        # print("h_max" + str(h_max))
        # print("x" + str(x))
        # print("h" + str(h))
    if keyboard == 97 and (y-10 >= 0): # a - left
        y = y - 10
    if keyboard == 100 and (y + 10 <= w_max - w): #d - right
        y = y + 10
    if keyboard == 102 and (h+10 <= h_max - x): # f - height up 
        h = h + 10
        # print("h_max" + str(h_max))
        # print("x" + str(x))
        # print("h" + str(h))
    if keyboard == 103 and (w+10 <= w_max - y): # g - width up
        w = w + 10
    if keyboard == 104 and (h-10 >= 50): # h - height down 
        h = h - 10
    if keyboard == 106 and (w-10 >= 50): # j - width down
        w = w - 10
 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break