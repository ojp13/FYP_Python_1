#SVM Classifier using SKLearn

from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
from Plot_Decision_Regions import plot_decision_regions

##df = pd.read_csv("iris.data",
##                 header=None)

filename = "/home/pi/FYP_Python_1/FYP_Python_1/Dev_App_V1/featurearray_2.pickle"
pickle_in = open(filename,"rb") #We would like to open a file to read data from
df = pickle.load(pickle_in)
pickle_in.close()

features = list(df)
feature_index = [0,1]
feature1 = features[feature_index[0]]
feature2 = features[feature_index[1]]


y = df.iloc[:,-1].values
X = df.iloc[:,feature_index].values

print(y)
y = np.where(y == 1, 1, -1)
print(y)

x_pos_index = []
x_neg_index = []



for i in range(len(y)):
    if y[i] == 1:
        x_pos_index.append(i)
    else:
        x_neg_index.append(i)


plt.scatter(X[x_pos_index,0], X[x_pos_index,1],
            color="red", marker="o", label="positive")

plt.scatter(X[x_neg_index,0], X[x_neg_index,1],
            color="blue", marker="x", label="negative")
plt.xlabel(feature1)
plt.ylabel(feature2)
plt.legend(loc="upper left")
plt.show()


svm = SVC(kernel="linear", C=5.0, random_state=1)
svm.fit(X, y)

plot_decision_regions(X, y, classifier=svm)
plt.xlabel(feature1)
plt.ylabel(feature2)
plt.legend(loc="upper left")
plt.show()
