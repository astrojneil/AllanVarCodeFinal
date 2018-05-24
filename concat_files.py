#Concatenate files generated from the startStop.py
#requires a list of file numbers and the file names
#will produce one large file with all of the individual
#files added on sequencially

import numpy as np

multifile_name = 'savefiles/640test_'
filenumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

mainfile = open('640_final.dat', 'w')
prev_time = 0.0
prev_step = 0

#loop through all small files
for f in filenumbers:
    singlefile = open(multifile_name+str(f)+'.dat', 'r')
    i = 0
    newtime = 0.0
    newstep = 0
    savetime = 0.0
    for line in singlefile:
        if f == 1:  #if the first file
            #separate time from data (in [])
            splitLine1 = line.split('[')
            temp = splitLine1[0]

            #time is first thing before a space
            time = float(temp.split(' ')[0])
            step = int(temp.split(' ')[1])

            newtime = prev_time+time
            newstep = prev_step+step

            newline = str(newtime)+' '+str(newstep)+' ['+splitLine1[1]
            mainfile.write(newline)
        else:   #all other files
            if i == 0:
                #separate time from data (in [])
                splitLine1 = line.split('[')
                temp = splitLine1[0]

                #time is first thing before a space
                savetime = float(temp.split(' ')[0])

            if i >= 1:   #skip the first line of all but first file
                #separate time from data (in [])
                splitLine1 = line.split('[')
                temp = splitLine1[0]

                #time is first thing before a space
                time = float(temp.split(' ')[0])
                step = int(temp.split(' ')[1])

                newtime = prev_time+(time-savetime)
                newstep = prev_step+step

                newline = str(newtime)+' '+str(newstep)+' ['+splitLine1[1]
                mainfile.write(newline)
        i = i+1

    singlefile.close()
    print("Finished with file "+str(f))

    prev_time = newtime
    prev_step = newstep
