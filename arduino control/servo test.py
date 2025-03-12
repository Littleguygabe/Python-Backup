from pyfirmata import Arduino, SERVO

angle1 = 30
angle2 = 60
angle3 = 90

port = 'COM3'
board=Arduino(port)

board.digital[2].mode=SERVO
board.digital[3].mode=SERVO
board.digital[4].mode=SERVO


board.digital[2].write(30)
board.digital[3].write(60)
board.digital[4].write(90)


print('finished')