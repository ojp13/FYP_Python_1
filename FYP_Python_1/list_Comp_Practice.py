import math
import Movement_Class
import numpy as np
import matplotlib.pyplot as plt

n = 20

interval_movement = 100
len_data = 2000
time = range(len_data)


accX = np.zeros([len_data], dtype = float)
accY = np.zeros([len_data], dtype = float)
accZ = np.zeros([len_data], dtype = float)

for i in range(len_data):
    accX[i] = math.sin(time[i] * 0.05 * math.pi) + 0.5
    accY[i] = math.sin(time[i] * 0.05 * math.pi) + 0
    accZ[i] = math.sin(time[i] * 0.05 * math.pi) - 0.5

move_acc_array = np.zeros([interval_movement, n, 3], dtype = float)

for i in range (0, n):
    move_acc_array[:,i,0] = accX[(i * interval_movement):((i + 1) * interval_movement)]
    move_acc_array[:,i,1] = accY[(i * interval_movement):((i + 1) * interval_movement)]
    move_acc_array[:,i,2] = accZ[(i * interval_movement):((i + 1) * interval_movement)]

plt.scatter(range(0,len(move_acc_array)), move_acc_array[:,0,0], s = 1)
plt.scatter(range(0,len(move_acc_array)), move_acc_array[:,0,1], s = 1)
plt.scatter(range(0,len(move_acc_array)), move_acc_array[:,0,2], s = 1)

plt.show()

list_moves = [[] for i in range(n)]

for i in range(n):
    list_moves[i] = Movement_Class.Movement(move_acc_array[:,i,0], move_acc_array[:,i,1], move_acc_array[:,i,2], i+1)
    print(i)

for i in range(n):
    list_moves[i].describe_Movement()


