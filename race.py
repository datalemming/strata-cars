
import time
from datetime import datetime
from riak import RiakClient as rc
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

channel=4
GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

start=time.time()
stop=time.time()
firstlap=True
driveremail=str(input("Enter driver's email to start\n"))
print "Driver you may start your laps\n"
laptimes=[]

##
def addLapTimes(laptimes):
	lts=laptimes
	print lts
	host='192.168.0.15'
	port=8087
	nodes=[{'host':host,'port':port}]
	conn=rc(protocol='pbc',nodes=nodes)
	print conn.ping() #should be True
	t=conn.table('stratalaptimes')
	print t	
	#set time stamp
	records=[]
	timestamp=int(time.time()*1000)
	print timestamp
		
	#iterate through the laptimes list
	for l in lts:
		print l
		r=["StrataLondon",timestamp,l[0],l[1]]
		print r
		records.append(r)
		timestamp = timestamp+1000
	to=t.new(records)
	print "Created table object"
	print "Store result: ",to.store()

##

def my_callback(channel):
	global start, stop, firstlap, driveremail,laptimes
	if (firstlap==True):
		start=time.time()
		firstlap=False
		print "Lap timing started"
	else:
		result=[]
		stop=time.time()
		laptime=stop-start
		start=stop
		result.append(driveremail)
		result.append(laptime)
		print driveremail," Laptime= ",laptime," s"
		laptimes.append(result)
		
		
GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print laptimes
	#now to input lap times into Riak
	addLapTimes(laptimes)

