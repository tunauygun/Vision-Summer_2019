from networktables import NetworkTables
import logging
import time
import random

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server="roborio-4783-frc.local")
#NetworkTables.initialize(server="10.47.83.2:")

sd = NetworkTables.getTable("rpi2")
i = 0;

while True:
	sd.putNumber("RandomNumber", random.randint(1,10))
	#print(sd.getNumber("WritesPS",0))
	#sd.putString("StingTest", "ItWorks!!!")
	#sd.putNumber("numTest", i)
	#i += 1
	#time.sleep(1)
	
#Received an invalid UTF-8 string:
