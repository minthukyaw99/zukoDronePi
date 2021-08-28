import RPi.GPIO as GPIO
from time import sleep


import sys
import time

if len(sys.argv) != 2:
    print("Receive mavlink heartbeats on specified interface. "
          "Respond with a ping message")

pin = int(float(sys.argv[2]))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin, 50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)


ang = int(float(sys.argv[1]))
print "Typ = ", type(ang)
SetAngle(ang)
pwm.stop()
GPIO.cleanup()
