from inputs import get_gamepad
import math
import threading
import sys
import time

from pyfirmata import Arduino, SERVO

angletendon1 = 0
anglequad1 = 0

""" port = 'COM3'
board = Arduino(port)

t1pin = 2
q1pin = 3

interval = 2

board.digital[t1pin].mode=SERVO
board.digital[q1pin].mode=SERVO """

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        lx = self.LeftJoystickX
        ly = self.LeftJoystickY
        rx = self.RightJoystickX
        ry = self.RightJoystickY
        #a = self.A
        x = self.X # b=1, x=2
        #rb = self.RightBumper
        return [round(lx), round(ly),round(rx),round(ry),x]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state




if __name__ == '__main__':
    joy = XboxController()
    while True:
        leftx = joy.read()[0]
        lefty = joy.read()[1]

        rightx = joy.read()[2]
        righty = joy.read()[3]

        xpress = joy.read()[4]

        print(joy.read())

"""         if lefty == 1:
            if angletendon1<120:
                angletendon1=angletendon1+interval
                board.digital[q1pin].write(angletendon1)
                print(f'pin2 angle: {angletendon1}')
                time.sleep(0.01)

        elif lefty == -1:
            if angletendon1>0:
                angletendon1 = angletendon1-interval
                board.digital[q1pin].write(angletendon1)
                print(f'pin2 angle: {angletendon1}')
                time.sleep(0.01) 

        elif leftx == -1:
            if anglequad1<180:
                anglequad1=anglequad1+interval
                board.digital[t1pin].write(anglequad1)
                print(f'pin angle: {anglequad1}')
                time.sleep(0.01)

        elif leftx== 1:
            if anglequad1>0:
                anglequad1 = anglequad1-interval
                board.digital[t1pin].write(anglequad1)
                print(f'pin angle: {anglequad1}')
                time.sleep(0.01)

        elif xpress == 1:
            sys.exit() """
