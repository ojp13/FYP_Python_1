import csv
import numpy as np
import matplotlib.pyplot as plt
from twos_Comp import twos_comp
from scipy import signal

filename = 'test3.csv'

with open(filename, newline='') as f:
    rawDataFile = csv.reader(f)
    rawData = list(rawDataFile)

numRows = len(rawData)
numCols = len(rawData[0])

print(numRows, numCols)

rawDataShifted = np.empty([numRows,22]) #initialise an empty array with the same number of rows as the raw data file 22 columns
#22 column values; 0-Gyro x; 1-Gryo y; 2-Gyro z; 3-Mag x; 4-Mag y; 5-Mag z; 6-Acc x; 7-Acc y; 8-Acc z; 9-MMG1; 10-MMG2; 
#                 11-MMG3; 12-MGG4; 13-MMG5; 14-MMG6; 15-MMG7; 16-MMG8; 17-Clock; 18-Quat. W; 19-Quat. X; 20-Quat. Y; 21-Quat. Z

wantedColumns = [6, 7, 8] #Only some values are wanted

for x in range(0,numRows-1):

    for i in wantedColumns:
        # Values copied by: Low Byte OR'd with (High Byte bit shifted left by 8)
        rawDataShifted[x,i] = twos_comp((int(rawData[x][ 2 * i + 1 ]) | (int(rawData[x][ 2 * i + 2])<< 8 )),16)

    for i in range(17,21):
        # Values copied directly
        rawDataShifted[x,i] = rawData[x][ i + 18 ]


## Smoothing attempt 1 ( 3 point moving average )
#rawDataSmoothed = np.empty([numRows - 2,22])

#for i in range(1, numRows-2): # First and last points can't be averaged
#    # Smoothing data with 3 point average

#    for j in range(0, 21):
#        rawDataSmoothed[i,j] = (rawDataShifted[i-1, j] + rawDataShifted[i, j] + rawDataShifted[i+1, j]) / 3
    
#timeSmoothed = range(1, numRows - 1) # (numRows - 2) elements

# Smoothing attempt 2 ( Savitzky-Golay filter )

rawDataSmoothed = signal.savgol_filter()

#gyroX = np.empty([numRows,1])
#gyroY = np.empty([numRows,1])
#gyroZ = np.empty([numRows,1])
#magX  = np.empty([numRows,1])
#magY  = np.empty([numRows,1])
#magZ  = np.empty([numRows,1])
accX  = np.empty([numRows,1])
accY  = np.empty([numRows,1])
accZ  = np.empty([numRows,1])

#gyrox = rawdatasmoothed[:,0]
#gyroy = rawdatasmoothed[:,1]
#gyroz = rawdatasmoothed[:,2]
#magx  = rawdatasmoothed[:,3]
#magy  = rawdatasmoothed[:,4]
#magz  = rawdatasmoothed[:,5]
accX  = rawDataSmoothed[:,6]
accY  = rawDataSmoothed[:,7]
accZ  = rawDataSmoothed[:,8]


plt.scatter(timeSmoothed, accY, s=5)

plt.show()
