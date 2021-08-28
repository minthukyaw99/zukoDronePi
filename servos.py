import socket
import json
import RPi.GPIO as GPIO
from time import sleep


class Servo:
    def __init__(self, pin):
        self.pin = pin
        self.setupServo()

    def setupServo(self):
        self.servo = GPIO.PWM(self.pin, 50)

    def start(self):
        self.servo.start(0)

    def stop(self):
        self.servo.stop()

    def setAngle(self, angle):
        print("pin is: ", self.pin)
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.servo.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        self.servo.ChangeDutyCycle(0)
        # self.servo.stop()
        # GPIO.cleanup()


UDP_PORT = 9001
UDP_IP = ""
DROP_SERVO_PIN = 37
TURN_SERVO_PIN = 35
UPDOWN_SERVO_PIN = 33

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

dropServo = Servo(DROP_SERVO_PIN)
turnServo = Servo(TURN_SERVO_PIN)
upDownServo = Servo(UPDOWN_SERVO_PIN)

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    servoMessage = json.loads(data)
    angle = servoMessage["degree"]
    servoId = servoMessage["servoId"]
    print("servo id is :", servoId)
    if servoId == 1:
        dropServo.start()
        dropServo.setAngle(angle)
        sleep(3)
        dropServo.start()
        dropServo.setAngle(0)
    elif servoId == 2:
        turnServo.start()
        turnServo.setAngle(angle)
    elif servoId == 3:
        upDownServo.start()
        upDownServo.setAngle(angle)

  #  GPIO.cleanup()

    print(servoMessage["degree"], addr)
