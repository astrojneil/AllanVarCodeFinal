import subprocess as sp
import time

length = 60 #wait 5 seconds
duration = 300
startTime = time.time()
finalEndTime = startTime+duration  #run for a total of 20 seconds
i = 1
while(time.time() < finalEndTime):
	longScript = sp.call(['python', 'longscript.py', str(i), str(length)]) #runs longscript.py
	runTimeLen = time.time()-startTime
	print('Finished round '+str(i)+'; Runtime: '+str(round(runTimeLen/3600.0, 4))+' hours ('+str(round(runTimeLen/60.0, 4))+' minutes)')
	startTime = time.time()
	i = i+1

print('Done!')

