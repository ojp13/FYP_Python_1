import csv
from scipy.signal.signaltools import lfilter
import numpy as np
import matplotlib.pyplot as plt
from twos_Comp import twos_comp
from scipy import signal
import Movement_Class

### Reading in data from CSV

filename = 'test_3.csv'

with open(filename, newline='') as f:
    rawDataFile = csv.reader(f)
    rawData = list(rawDataFile)

numRows = len(rawData)      
numCols = len(rawData[0])

print(numRows, numCols)

rawDataShifted = np.empty([numRows,22]) #initialise an empty array with the same number of rows as the raw data file and 22 columns
#22 column values; 0-Gyro x; 1-Gryo y; 2-Gyro z; 3-Mag x; 4-Mag y; 5-Mag z; 6-Acc x; 7-Acc y; 8-Acc z; 9-MMG1; 10-MMG2; 
#                 11-MMG3; 12-MGG4; 13-MMG5; 14-MMG6; 15-MMG7; 16-MMG8; 17-Clock; 18-Quat. W; 19-Quat. X; 20-Quat. Y; 21-Quat. Z

wantedColumns = [6, 7, 8] #Only some values are wanted

for x in range(0, numRows-1):

    for i in wantedColumns:
        # Values copied by: Low Byte OR'd with (High Byte bit shifted left by 8)
        rawDataShifted[x,i] = twos_comp((int(rawData[x][ 2 * i + 1 ]) | (int(rawData[x][ 2 * i + 2])<< 8 )),16)

    for i in range(17,21):
        # Values copied directly
        rawDataShifted[x,i] = rawData[x][ i + 18 ]



### Processing/smoothing data

offsetZ = np.mean(rawDataShifted[:,8]) # Offset due to gravity in acc z data

accX  = rawDataShifted[:,6]
accY  = rawDataShifted[:,7]
accZ  = rawDataShifted[:,8] - offsetZ # Gravity is is negative direction, so offsetZ has a negative magnitude

n = 15
b = [1.0 / n] * n   # Denominator Coefficient for IIR filter
a = 1               # Numerator Coefficient for IIR filter

accXSmoothed = signal.lfilter(b, a, accX)
accYSmoothed = signal.lfilter(b, a, accY)
accZSmoothed = signal.lfilter(b, a, accZ)


#plt.scatter(range(len(accXSmoothed)), accXSmoothed, s = 0.1)
#plt.scatter(range(len(accYSmoothed)), accYSmoothed, s = 0.1)
#plt.scatter(range(len(accZSmoothed)), accZSmoothed, s = 0.1)

#plt.show()

### Trying to tell when a movement is happening is acceleration data

threshold = 4000    # Value above which we believe a movement to be happening in the acceleration data
seqReq = 50         # Sequence Required: Number dictating how many previous values have to have been above the threshold to be sure
                    # a movement is actually happening and it isn't just noise

moveIndaccX = np.zeros([numRows], dtype = int)   # Zero array with numRows rows 
moveIndaccY = np.zeros([numRows], dtype = int)
moveIndaccZ = np.zeros([numRows], dtype = int)

for i in range(0, numRows):     # Return 1 if value is over threshold, even temporarily
    if abs(accXSmoothed[i]) > threshold:
        moveIndaccX[i] = 1
    if abs(accYSmoothed[i]) > threshold:
        moveIndaccY[i] = 1
    if abs(accZSmoothed[i]) > threshold:
        moveIndaccZ[i] = 1

moveIndSmoothaccX = np.ones([numRows - seqReq + 1], dtype = int) # Movement Indicator Smooth - initialise array of zeros
# This array will show a 1 when the last seqReq values in seqReq were above a threshold
moveIndSmoothaccY = np.ones([numRows - seqReq + 1], dtype = int)
moveIndSmoothaccZ = np.ones([numRows - seqReq + 1], dtype = int)

for i in range(seqReq - 1, numRows):    # Return 1 if only last n = seqReq values were above threshold
    for j in range(0, seqReq - 1):
        moveIndSmoothaccX[i - (seqReq - 1)] = moveIndSmoothaccX[i - (seqReq - 1)] & moveIndaccX[i - j]
        moveIndSmoothaccY[i - (seqReq - 1)] = moveIndSmoothaccY[i - (seqReq - 1)] & moveIndaccY[i - j]
        moveIndSmoothaccZ[i - (seqReq - 1)] = moveIndSmoothaccZ[i - (seqReq - 1)] & moveIndaccZ[i - j]

#plotxaxisIndex = range(0, numRows-seqReq+1)

#plt.scatter(plotxaxisIndex, moveIndSmoothaccX, s = 0.1)
#plt.scatter(plotxaxisIndex, moveIndSmoothaccY, s = 0.1)
#plt.scatter(plotxaxisIndex, moveIndSmoothaccZ, s = 0.1)

#plt.show()

moveIndSmoothaccAll = np.zeros([numRows - seqReq + 1], dtype = int) # Single array to demonstrate when movement is happening in accelerometer data

for i in range(0, numRows - seqReq):
    moveIndSmoothaccAll[i] = moveIndSmoothaccX[i] | moveIndSmoothaccY[i] | moveIndSmoothaccZ[i] # Bitwise OR of all acc components



### Here we will capture the index of the data point at the start of the movement, then collect data in acc data from that index oxwards

stepValue = 500    # This is the length (in sampling periods) that we believe a movement will go on for
backTrack = 20      # Number of steps movement is happening before it reaches threshold value
indexValues = []    # Initialising list for values of index at which movement starts

rowIncrementer = 1  # Initialising an incrementer for a while loop

while rowIncrementer < (numRows - seqReq): # Looping through the binary array that dictates whether a movement is happening or not
    if moveIndSmoothaccAll[rowIncrementer] != moveIndSmoothaccAll[rowIncrementer-1]:
        indexValues.append(rowIncrementer)
        rowIncrementer += stepValue
    else:
        rowIncrementer += 1

numMoves = len(indexValues) # Number of movements found in data

print(numMoves)

### Here we will collect the data for ech movement in an object. The object name will be a list index

# Putting acc data for each movement into a big array for easy reference

move_acc_array = np.zeros([stepValue + backTrack, numMoves, 3], dtype = float)

for i in range (0, numMoves):
    move_acc_array[:,i,0] = accXSmoothed[(indexValues[i]-backTrack):(indexValues[i]+stepValue)]
    move_acc_array[:,i,1] = accYSmoothed[(indexValues[i]-backTrack):(indexValues[i]+stepValue)]
    move_acc_array[:,i,2] = accZSmoothed[(indexValues[i]-backTrack):(indexValues[i]+stepValue)]

list_moves = [[] for i in range(numMoves)] # Creates an empty list to store objects 

for i in range(numMoves):
    list_moves[i] = Movement_Class.Movement(move_acc_array[:,i,0], move_acc_array[:,i,1], move_acc_array[:,i,2], i+1)

for i in range(numMoves):
    plt.scatter(list_moves[i].total_distX, list_moves[i].total_distY, s = 5)

plt.xlabel('Displacement in x direction [arbitrary units]')
plt.ylabel('Displacement in y direction [arbitrary units]')
plt.legend(loc='upper left')

plt.show()
