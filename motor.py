#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_A1 = 14 #2
GPIO_A2 = 15 #3
GPIO_B1 = 26 #14
GPIO_B2 = 19 #15
 
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

 
if __name__ == '__main__':
    try:
	i = 0;
        while (i<2):
            i = i+1
            print ("Going forward")
            forward()
            time.sleep(1)
            print ("Going backward")
            reverse()
            time.sleep(1)
            #print ("Going right")
            #turn1()
            #time.sleep(3)
            #print ("Going left")
            #turn2()
            #time.sleep(3)
            
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Control stopped by User")
        GPIO.cleanup()
