#Testing the performance of a classifier induced from raw data
#This script allows for changing of maximum test set size, then picks different training set sizes

import pickle
import threading
import pandas as pd
import numpy as np
import math
import time
from scipy.integrate import simps
from scipy.integrate import cumtrapz
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

#Settings
smoothing = True
N = 20
normalization = True
test_size = 0.4 #Has to be a multiple of 0.04
test_steps = int(((1 - test_size) / 0.04) + 1)


BT_isRecording = False
IMU_Data_Key = ["x acceleration", "y acceleration", "z acceleration", "x gyroscope", "y gyroscope", "z gyroscope"]
movement_features_key = ["x Total Displacement", "y Total Displacement", "z Total Displacement",
                         "x Total Rotation", "y Total Rotation", "z Total Rotation",
                         "x Peak Displacement", "y Peak Displacement", "z Peak Displacement",
                         "x Peak Rotation", "y Peak Rotation", "z Peak Rotation",
                         "class label"]

features_df = pd.DataFrame(columns=movement_features_key)
features_index = [0,1,2,3,4,5,6,7,8,9,10,11]
movement_rawdata_collected = []

#Constants to keep track of settings

filename = "\Testing1_4.pickle"
filename = "C:\FYP_Python_1\FYP_Python_1\Project_Testing" + filename

#Loading the raw data file
pickle_in = open(filename,"rb") #We would like to open a file to read data from
movement_rawdata_collected = pickle.load(pickle_in)
pickle_in.close()

#smoothing the raw data

num_samples = len(movement_rawdata_collected)

if smoothing:
    movement_rawdata_collected_unsmoothed = movement_rawdata_collected
    movement_rawdata_collected = []
    movement_rawdata = {}

    for sample in range(num_samples):
        
        for Key in IMU_Data_Key:
            movement_rawdata[Key] = np.convolve(movement_rawdata_collected_unsmoothed[sample][Key][:], np.ones((N,))/N, mode='valid')

        movement_rawdata["Class Label"] = movement_rawdata_collected_unsmoothed[sample]["Class Label"]
        movement_rawdata_collected.append(movement_rawdata)
        movement_rawdata = {}
    
#Creating the feature array

x_totaldisp = np.zeros(num_samples)
y_totaldisp = np.zeros(num_samples)
z_totaldisp = np.zeros(num_samples)
x_totalrot = np.zeros(num_samples)
y_totalrot = np.zeros(num_samples)
z_totalrot = np.zeros(num_samples)
x_peakvel = np.zeros(num_samples)
y_peakvel = np.zeros(num_samples)
z_peakvel = np.zeros(num_samples)
x_peakrot = np.zeros(num_samples)
y_peakrot = np.zeros(num_samples)
z_peakrot = np.zeros(num_samples)

classlabels = np.zeros(num_samples, dtype=int)

for i in range(num_samples):
    x_velocity = cumtrapz(movement_rawdata_collected[i]["x acceleration"][:])
    x_peakvel[i] = abs(max(x_velocity, key=abs))
    x_totaldisp[i] = simps(x_velocity)
    y_velocity = cumtrapz(movement_rawdata_collected[i]["y acceleration"][:])
    y_peakvel[i] = abs(max(y_velocity, key=abs))
    y_totaldisp[i] = simps(y_velocity)
    z_velocity = cumtrapz(movement_rawdata_collected[i]["z acceleration"][:])
    z_peakvel[i] = abs(max(z_velocity, key=abs))
    z_totaldisp[i] = simps(z_velocity)
    
    x_rot_velocity = cumtrapz(movement_rawdata_collected[i]["x gyroscope"][:])
    x_peakrot[i] = abs(max(x_rot_velocity, key=abs))
    x_totalrot[i] = simps(x_rot_velocity)
    y_rot_velocity = cumtrapz(movement_rawdata_collected[i]["y gyroscope"][:])
    y_peakrot[i] = abs(max(y_rot_velocity, key=abs))
    y_totalrot[i] = simps(y_rot_velocity)
    z_rot_velocity = cumtrapz(movement_rawdata_collected[i]["z gyroscope"][:])
    z_peakrot[i] = abs(max(z_rot_velocity, key=abs))
    z_totalrot[i] = simps(z_rot_velocity)

    classlabels[i] = int(movement_rawdata_collected[i]["Class Label"][0])

feature_normalisation_factor = (sum(x_totaldisp) + sum(y_totaldisp) + sum(z_totaldisp) + sum(x_totalrot)
                                + sum(y_totalrot) + sum(z_totalrot)) / (6 * num_samples)

if normalization: #If feature normalisation is set to true
    x_totaldisp = [float(i)/feature_normalisation_factor for i in x_totaldisp]
    x_peakvel = [float(i)/feature_normalisation_factor for i in x_peakvel]
    y_totaldisp = [float(i)/feature_normalisation_factor for i in y_totaldisp]
    y_peakvel = [float(i)/feature_normalisation_factor for i in y_peakvel]
    z_totaldisp = [float(i)/feature_normalisation_factor for i in z_totaldisp]
    z_peakvel = [float(i)/feature_normalisation_factor for i in z_peakvel]
    x_totalrot= [float(i)/feature_normalisation_factor for i in x_totalrot]
    x_peakrot = [float(i)/feature_normalisation_factor for i in x_peakrot]
    y_totalrot= [float(i)/feature_normalisation_factor for i in y_totalrot]
    y_peakrot = [float(i)/feature_normalisation_factor for i in y_peakrot]    
    z_totalrot= [float(i)/feature_normalisation_factor for i in z_totalrot]
    z_peakrot = [float(i)/feature_normalisation_factor for i in z_peakrot]

features_df["x Total Displacement"] = x_totaldisp
features_df["y Total Displacement"] = y_totaldisp
features_df["z Total Displacement"] = z_totaldisp
features_df["x Total Rotation"] = x_totalrot
features_df["y Total Rotation"] = y_totalrot
features_df["z Total Rotation"] = z_totalrot
features_df["x Peak Displacement"] = x_peakvel
features_df["y Peak Displacement"] = y_peakvel
features_df["z Peak Displacement"] = z_peakvel
features_df["x Peak Rotation"] = x_peakrot
features_df["y Peak Rotation"] = y_peakrot
features_df["z Peak Rotation"] = z_peakrot
features_df["class label"] = classlabels

y = features_df.iloc[:, -1].values
X = features_df.iloc[:, features_index].values

print(X)

max_training_set_size = []
average_class_error = []


for test_size in range(1, 25):
    test_size = test_size * 0.04
    test_steps = int(((1 - test_size) / 0.04) + 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
                                                    random_state=0, stratify=y)

    X_testfixed = X_test
    y_testfixed = y_test
    
    for train_size in range(1, test_steps):
        test_size_temp = (1 - 0.04 * train_size)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size_temp,
                                                        random_state=42, stratify=y)

        svm = SVC(kernel="linear", C=0.1, random_state=1)
        svm.fit(X_train, y_train)
        X_predicted = svm.predict(X_testfixed)
        counter = 0
        class_error = []
        for sample_number in range(len(X_predicted)):
            if X_predicted[sample_number] != y_testfixed[sample_number]:
                counter += 1

        class_error.append(float((len(X_predicted)-counter)/len(X_predicted)))

    average_class_error.append(sum(class_error)/float(len(class_error)))
    max_training_set_size.append(int((1-test_size)*100))
    

    
            



plt.scatter(max_training_set_size, average_class_error, marker="x", s=5)
plt.xlabel("Size of training set as percentage of total data")
plt.ylabel("Classification Accuracy")
plt.show()








