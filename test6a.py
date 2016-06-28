
import time
from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

channel=4
GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_UP)

start=time.time()
stop=time.time()
firstlap=True
driveremail=str(input("Enter driver's email to start\n"))
print "Driver you may start your laps\n"
laptimes=[]



def my_callback(channel):
	global start, stop, firstlap, driveremail,laptimes
	if (firstlap==True):
		start=time.time()
		firstlap=False
		print "Lap timing started"
	else:
		stop=time.time()
		laptime=stop-start
		start=stop
		result=driveremail+","+str(laptime)
		print driveremail," Laptime= ",laptime," s"
		laptimes.append(result)
		
		
GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback, bouncetime=200)

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print laptimes

