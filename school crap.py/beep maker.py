import winsound
import time

def playc():
    winsound.Beep(261,200)
    
def playd():
    winsound.Beep(293,200)
    
def playe():
    winsound.Beep(329,200)
    
def playf():
    winsound.Beep(349,200)
    
def playg():
    winsound.Beep(392,200)
    
def playa():
    winsound.Beep(440,200)
    
def playb():
    winsound.Beep(493,200)

def rest():
    winsound.Beep(37,200)

playe()
time.sleep(0.2)
playg()
time.sleep(0.1)
playe()
time.sleep(0.1)
playe()
playa()
time.sleep(0.1)
playe()
time.sleep(0.1)
playd()

time.sleep(0.2)
playe()
time.sleep(0.2)
playg()
time.sleep(0.1)
playe()
time.sleep(0.1)
playe()
playc()
time.sleep(0.1)
playe()
time.sleep(0.1)
playd()