#Libraries
import RPi.GPIO as GPIO
import time
from RPIO import PWM
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_A1 = 2
GPIO_A2 = 3
GPIO_B1 = 14
GPIO_B2 = 15

GPIO_TRIGGER = 18
GPIO_ECHO = 24

servo = PWM.Servo()
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_A1, GPIO.OUT)
GPIO.setup(GPIO_A2, GPIO.OUT)
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #c
GPIO.setup(GPIO_ECHO, GPIO.IN)

def forward(speed):
    # set Trigger to HIGH
    #GPIO.output(GPIO_A1, True)
    GPIO.output(GPIO_A2, False)
    #GPIO.output(GPIO_B1, True)
    GPIO.output(GPIO_B2, False)

    servo.set_servo(GPIO_A1, speed)
    servo.set_servo(GPIO_B1, speed)
    return

def reverse():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, False)
    GPIO.output(GPIO_A2, True)
    GPIO.output(GPIO_B1, False)
    GPIO.output(GPIO_B2, True)
    return

def right():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, True)
    GPIO.output(GPIO_A2, False)
    GPIO.output(GPIO_B1, False)
    GPIO.output(GPIO_B2, True)
    return

def left():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, False)
    GPIO.output(GPIO_A2, True)
    GPIO.output(GPIO_B1, True)
    GPIO.output(GPIO_B2, False)
    return

def stop():
    GPIO.output(GPIO_A1, False)
    GPIO.output(GPIO_A2, False)
    GPIO.output(GPIO_B1, False)
    GPIO.output(GPIO_B2, False)
    return

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            forward(4000)
            time.sleep(3)
            forward(8000)
            time.sleep(3)
            forward(12000)
            time.sleep(3)
            # if-else to set forward or stop
            #if dist > 25:
            #    forward()
            #else:
            #    stop()
		#break
            #time.sleep(0.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
