#########################################
#EUC-race.py
#SMDE 19/08/2016
#This is an edit of the original race.py to
#accommodate two working tracks, i.e. two cars
#
#
#########################################

#########################################
#Imports and initialisation
#########################################
import time
from datetime import datetime
from riak import RiakClient as rc
import RPi.GPIO as GPIO

#########################################
#Setup of Pi
#########################################
GPIO.setmode(GPIO.BCM)

channel1=4
GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Add additional channel
channel2=5
GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#########################################
#variables
#########################################
start1=time.time()
stop1=time.time()
firstlap1=True

#double up on variables
start2=time.time()
stop2=time.time()
firstlap2=True

#########################################
#initialisation for each run
#########################################
driver1email=str(input("Enter driver1's email\n"))
driver2email=str(input("Enter driver2's email\n")) #second email

print "Drivers you may start your laps\n"
laptimes1=[]
laptimes2=[]

###############################################
#Commit times to database
###############################################
def addLapTimes(laptimes1,laptimes2):
	lts1=laptimes1
	lts2=laptimes2
	print lts1
	print lts2
	host='192.168.0.15'
	port=8087
	nodes=[{'host':host,'port':port}]
	conn=rc(protocol='pbc',nodes=nodes)
	print conn.ping() #should be True
	t=conn.table('EUClaptimes')
	print t
	#set time stamp
	records=[]
	timestamp=int(time.time()*1000)
	print timestamp

	#iterate through both laptimes list
	for l in lts1:
		print l
		r=["EUCStockholm",timestamp,l[0],l[1]]
		print r
		records.append(r)
		timestamp = timestamp+1000

	for l in lts2:
		print l
		r=["EUCStockholm",timestamp,l[0],l[1]]
		print r
		records.append(r)
		timestamp = timestamp+1000

	to=t.new(records)
	print "Created table object"
	print "Store result: ",to.store()

########################################
##Switch callbacks
########################################
def my_callback1(channel1):
	global start1, stop1, firstlap1, driver1email,laptimes1
	if (firstlap1==True):
		start1=time.time()
		firstlap1=False
		print "Lap timing started driver 1"
	else:
		result1=[]
		stop1=time.time()
		laptime1=stop1-start1
		start1=stop1
		result.append(driver1email)
		result.append(laptime1)
		print driver1email," Laptime= ",laptime1," s"
		laptimes1.append(result)

def my_callback2(channel1):
	global start2, stop2, firstlap2, driver2email,laptimes2
	if (firstlap2==True):
		start2=time.time()
		firstlap2=False
		print "Lap timing started driver 2"
	else:
		result2=[]
		stop2=time.time()
		laptime2=stop2-start2
		start2=stop2
		result.append(driver2email)
		result.append(laptime2)
		print driver2email," Laptime= ",laptime2," s"
		laptimes2.append(result)

#########################################
#Switch events setup
#########################################

GPIO.add_event_detect(channel1, GPIO.RISING, callback=my_callback1, bouncetime=200)
GPIO.add_event_detect(channel2, GPIO.RISING, callback=my_callback2, bouncetime=200)

#########################################
#main dummy loop
#########################################
try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print laptimes1, laptimes2
	#now to input lap times into Riak
	addLapTimes(laptimes1, laptimes2)
