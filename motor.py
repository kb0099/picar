#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_A1 = 18
GPIO_A2 = 24
GPIO_B1 = 1
GPIO_B2 = 2
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_A1, GPIO.OUT)
GPIO.setup(GPIO_A2, GPIO.OUT)
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)
 
def forward():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, True)
    GPIO.output(GPIO_A2, False)
    GPIO.output(GPIO_B1, True)
    GPIO.output(GPIO_B2, False)
    return

def reverse():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, False)
    GPIO.output(GPIO_A2, True)
    GPIO.output(GPIO_B1, False)
    GPIO.output(GPIO_B2, True)
    return

def turn1():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, True)
    GPIO.output(GPIO_A2, False)
    GPIO.output(GPIO_B1, False)
    GPIO.output(GPIO_B2, True)
    return

def turn2():
    # set Trigger to HIGH
    GPIO.output(GPIO_A1, False)
    GPIO.output(GPIO_A2, True)
    GPIO.output(GPIO_B1, True)
    GPIO.output(GPIO_B2, False)
    return

 
if __name__ == '__main__':
    try:
        while True:
            
            print ("Going forward")
            forward()
            time.sleep(3)
            print ("Going backward")
            reverse()
            time.sleep(3)
            print ("Going turn1")
            turn1()
            time.sleep(3)
            print ("Going turn2")
            turn2()
            time.sleep(3)
            
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Control stopped by User")
        GPIO.cleanup()