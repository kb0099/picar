#Libraries
import RPi.GPIO as GPIO
import time
#from RPIO import PWM
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_A1 = 14 #2
GPIO_A2 = 15 #3
GPIO_B1 = 26 #14
GPIO_B2 = 19 #15
GPIO_A3 = 18 #4
GPIO_B3 = 13 #18

GPIO_TRIGGER = 2#23
GPIO_ECHO = 3#24

#servo = PWM.Servo()
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_A1, GPIO.OUT)
GPIO.setup(GPIO_A2, GPIO.OUT)
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)
GPIO.setup(GPIO_A3, GPIO.OUT)
GPIO.setup(GPIO_B3, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Initial Pwm
p1 = GPIO.PWM(GPIO_A3, 100)
p2 = GPIO.PWM(GPIO_B3, 100)
p1.start(20);
p2.start(20);

def forward():
	# set Trigger to HIGH
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)
	#GPIO.output(GPIO_A3, True)
	#GPIO.output(GPIO_B3, True)

	#for ii in range (20):
	p1.ChangeDutyCycle(50)
	p2.ChangeDutyCycle(50)
	

	#servo.set_servo(GPIO_A1, speed)
	#servo.set_servo(GPIO_B1, speed)
	return

def reverse():
	GPIO.output(GPIO_A1, False)
	GPIO.output(GPIO_A2, True)
	GPIO.output(GPIO_B1, False)
	GPIO.output(GPIO_B2, True)
	p1.ChangeDutyCycle(40)
	p2.ChangeDutyCycle(40)
	return

def slow_right():
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)
	p1.ChangeDutyCycle(40)
	p2.ChangeDutyCycle(30)
	return

def fast_right():
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, False)
	GPIO.output(GPIO_B2, True)
	p1.ChangeDutyCycle(70)
	p2.ChangeDutyCycle(40)
	return

def slow_left():
	GPIO.output(GPIO_A1, True)
	GPIO.output(GPIO_A2, False)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)
	p1.ChangeDutyCycle(30)
	p2.ChangeDutyCycle(40)
	return

def fast_left():
	GPIO.output(GPIO_A1, False)
	GPIO.output(GPIO_A2, True)
	GPIO.output(GPIO_B1, True)
	GPIO.output(GPIO_B2, False)
	p1.ChangeDutyCycle(30)
	p2.ChangeDutyCycle(70)
	return

def stop():
	p1.ChangeDutyCycle(0)
	p2.ChangeDutyCycle(0)
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
	# call the forward method
	try:
		#forward()
		time.sleep(1)
                print "sleeping 1"
		dir = 0
		while True:
                        print "checking dist"
			sens = distance()
                        print "dist = ", sens
			if sens < 30:
				reverse()
                                print "reversing"
				time.sleep(1)
				if dir == 0:
					slow_left()
                                        print "left"
					time.sleep(1)
					dir = 1
					forward()
                                        print "forward"
                                        time.sleep(1);
				elif dir == 1:
					slow_right()
                                        print "slow right"
					time.sleep(1)
					dir = 2
					forward()
				elif dir == 2:
					fast_left()
                                        print "fast left"
					time.sleep(1)
					dir = 3
					forward()
				else:
					fast_right()
                                        print "fast right"
					time.sleep(1)
					dir = 0
					forward()       
		#stop();
		#p1.stop();
		#p2.stop();
		#GPIO.cleanup();
	
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		stop()
		GPIO.cleanup();
	p1.stop()
	p2.stop()
	GPIO.cleanup();
	
