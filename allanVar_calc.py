#Allan Variance Code - python version
#J'Neil Cottle
#reads file which contains output file from an instrument
#computes the allan variance, outputs it to a file
import math
import numpy as np
class RoachData(object):
  bins = 2048
  timeSteps = 0
  data = []
  timeStamps = []

  def __init__(self):
      self.bins = 2048
      self.timeSteps = 0
      self.data = []
      self.timeStamps = []

  #parseLine
  #replaces characters to make line pars-able
  def parseLine(self, dataline):
  #separate time from data (in [])
    splitLine1 = dataline.split('[')
    temp = splitLine1[0]
    #get rid of extra spaces
    dataString = splitLine1[1].replace(' ','').replace(']','')

    #time is first thing before a space
    time = float(temp.split(' ')[0])
    self.timeStamps.append(time)

    #data is separated by commas
    dataStrings = dataString.split(',')

    newArray = []
    for i in range(len(dataStrings)):
      if(dataStrings[i].isspace() or dataStrings[i] == ''):
	      addDataString = 0.0
	      print('error')
      else:
	      addDataString = dataStrings[i]
      newArray.append(float(addDataString))

    self.bins = i
    self.data.append(newArray)

  #readRochData
  #reads in from line and parses lines into the roach data variables
  def readRoachData(self, datafile):
    steps = 0
    for line in datafile:
      steps = steps+1
      self.parseLine(line)

    self.timeSteps = steps

#getTimeSeries
#selects one frequency bin and returns all data for that bin
  def getTimeSeries(self, binNum):
    timeSeries = []
    for i in range(self.timeSteps):
        timeSeries.append(self.data[i][binNum])

    return timeSeries


#variance:
#loops over data, skipping integer multipler [n]
#sums data separated by n time steps
#returns normalized sum over 2m
def find_variance(data_short, n):
    Sum = 0
    i = 0
    while i < ((len(data_short)/n)-1):
        Sum = Sum + (data_short[n*(i + 1)] - data_short[n*i])**2
        i = i+1

    return Sum/(2*(len(data_short)-1))

def find_variance_overlap(data_short, n):
    Sum = 0
    j = 0
    M = len(data_short) #M in this definition is the whole dataset
    while j < (M-(2*n)):
        i = j
        Sum2 = 0
        while i <= j+n-1:
            Sum2 = Sum2 + (data_short[i + n] - data_short[i])
            i = i+1

        Sum = Sum + Sum2**2
        j = j+1

    return Sum/(2*(n**2)*(M-2*n+1))


#error:
#returns sqrt( var^2 (2/(n-1)))
def find_error(variance, numMeasure):
    return math.sqrt(variance**2*(2.0/(numMeasure -1.0)))

#truncate:
#returns new array of data with longest possible power of 2 Length
def truncate(dataArray):
    shortData = []
    #find highest power of 2
    j = 1
    j = len(dataArray)
    #while j <= len(dataArray)/2:
        #j = j*2


    for i in range(len(dataArray)):
        if i <= j:
            shortData.append(dataArray[i])
        else:
            break

    return shortData

#MeasurementPeriod: finds the length of a single timestep
def timeStep_len(roachdata):
    print (str((roachdata.timeStamps[-1] - roachdata.timeStamps[0])/len(roachdata.timeStamps)))
    return (roachdata.timeStamps[-1] - roachdata.timeStamps[0])/len(roachdata.timeStamps)


def find_AllVar(data1, data2, outfile):
    #find difference of two nodes
    data1 = np.array(data1)
    data2 = np.array(data2)

## here is where we take the difference of the two nodes!!
    data = (data1 - data2)*2
    #loops through integer multiple of timestep until total/4 (i=i*2)
    i = 1
    time_len = timeStep_len(roachdata)
    while ( i < (len(data)/4)):  # to allow at least 4 measurements in calc
        #set tau, call variance and error
        tau = i*time_len
        variance = find_variance_overlap(data, i)
        error = find_error(variance, int(len(data)/i))
        outfile.write(str(tau)+","+str(variance)+','+str(error)+'\n')
        i = i*2

    #write tau, error and variance to file

#main:
#------------------------------------------------------
#read in file
datafile = open('frequencyData.dat', 'r')

#reads in data from file to roachdata object
roachdata = RoachData()
roachdata.readRoachData(datafile)
datafile.close()

#define the nodes of interest
nodemin = 53
nodemax = 1792
edgebuff = 30


#find the middle of the nodes considered, define the nodes used for analysis
mid1 = int((nodemax-nodemin)/2)+nodemin
mid2 = mid1+1

edge1 = mid1-5
edge2 = mid1+5  #make the edge nodes about 10 channels apart

#open output files
outputfile_mid = open('allanVar_adj.dat', 'w')
outputfile_edge = open('allanVar_sep.dat', 'w')


#gets data for one particular node (frequency)
data_mid1 = roachdata.getTimeSeries(mid1)
data_mid2 = roachdata.getTimeSeries(mid2)

data_edge1 = roachdata.getTimeSeries(edge1)
data_edge2 = roachdata.getTimeSeries(edge2)


#truncates data to longest possible amount with a power of two Length
data_mid1 = truncate(data_mid1)
data_mid2 = truncate(data_mid2)

data_edge1 = truncate(data_edge1)
data_edge2 = truncate(data_edge2)

#finds AllVar for this outfile
find_AllVar(data_mid1, data_mid2, outputfile_mid)
find_AllVar(data_edge1, data_edge2, outputfile_edge)

outputfile_mid.close()
outputfile_edge.close()

#end of main
