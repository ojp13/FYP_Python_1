import numpy as np
import csv
import Perceptron_Class
import matplotlib.pyplot as plt
from Plot_Decision_Regions import plot_decision_regions

# Importing feature array

filename = 'feature_data.csv'

with open(filename, newline='') as f:
    raw_datafile = csv.reader(f)
    raw_data = list(raw_datafile)

    f.close()
    
num_moves = len(raw_data)           # Number of movements to classify
num_feats = len(raw_data[0]) - 1    # Number of features for each movement

feature_array = np.zeros([num_moves, num_feats], dtype = float)

for i in range(num_moves):
    for j in range(num_feats):
        feature_array[i,j] = raw_data[i][j]

# Standardising Feature array

feature_array_std = np.copy(feature_array)
feature_array_std[:,0] = (feature_array[:,0] - feature_array[:,0].mean()) / feature_array[:,0].std()
feature_array_std[:,1] = (feature_array[:,1] - feature_array[:,1].mean()) / feature_array[:,1].std()

target_values = np.zeros([num_moves], dtype = 'int') # Array of target values for ML algorithms (class labels)

i = 0
while i < 20:
    if i < 10:
        target_values[i] = 1
    else:
        target_values[i] = -1
    
    i += 1

print(np.unique(target_values))

### Plotting Data

plt.scatter(feature_array_std[:10,0], feature_array_std[:10,1], color = 'red', marker = 'o', label = 'Movement 1')
plt.scatter(feature_array_std[10:,0], feature_array_std[10:,1], color = 'blue', marker = 'x', label = 'Movement 2')
plt.xlabel('Total Displacement in x Direction (normalized)')
plt.ylabel('Total Displacement in y Direction (normalized)')
plt.legend(loc='upper left')
plt.show()

ppn = Perceptron_Class.Perceptron(eta = 0.1, n_iter = 20)
ppn.fit(feature_array[:,:2], target_values)

#plt.plot(range(1,len(ppn.errors_) + 1), ppn.errors_, marker = 'o')
#plt.xlabel('epochs')
#plt.ylabel('numer of updates')
#plt.show()

plot_decision_regions(feature_array_std[:,:2], target_values, classifier = ppn)
plt.xlabel('Total Displacement in x Direction (normalized)')
plt.ylabel('Total Displacement in y Direction (normalized)')
plt.legend(loc='upper left')
plt.show()
