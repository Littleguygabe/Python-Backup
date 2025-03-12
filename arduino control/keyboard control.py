from random import random
from pyfirmata import Arduino, SERVO, util
from time import sleep
import random
import time
import keyboard

angle = 120
angle2 = 0
angle3 = 0
angle4 = 0
port = 'COM3'
board=Arduino(port)
pin1 = 2 #left quad
pin2 = 3 # right quad
pin3 = 4 #left control
pin4 = 5 #right control

interval = 2

board.digital[pin1].mode=SERVO
board.digital[pin2].mode=SERVO
board.digital[pin3].mode=SERVO

print('ready')
while True:
    try:
        if keyboard.is_pressed('right'):
            if angle<180:
                angle=angle+interval
                board.digital[pin1].write(angle)
                print(f'pin angle: {angle}')
                time.sleep(0.01)
        if keyboard.is_pressed('left'):
            if angle>0:
                angle = angle-interval
                board.digital[pin1].write(angle)
                print(f'pin angle: {angle}')
                time.sleep(0.01)

        if keyboard.is_pressed('up'):
            if angle2<120:
                angle2=angle2+interval
                board.digital[pin2].write(angle2)
                print(f'pin2 angle: {angle2}')
                time.sleep(0.01)
            
        if keyboard.is_pressed('down'):
            if angle2>0:
                angle2 = angle2-interval
                board.digital[pin2].write(angle2)
                print(f'pin2 angle: {angle2}')
                time.sleep(0.01) 

        if keyboard.is_pressed('esc'):
            break
    except:
        break