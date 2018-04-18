#Support vector machine classifier

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

class Support_Vector_Machine:
    def __init__(self, visualization=True):
        self.visualization = visualization
        self.colors = {1:"r",-1:"b"}
        if self.visualization:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1,1,1)

    def fit(self, data):
        # Training the algorithm based on fed in feature data
        self.data = data

        opt_dict = {} #{ ||w||: [w,b] } Dictionary, key is magnitude of w, values are w and b

        #Transforms applied to the w/b vectors to compensate for feature signs
        transforms = [[1,1],
                      [-1,1],
                      [-1,-1],
                      [1,-1]]
        
        #Maximum and minimum values for graph and initial estimates for w and b
        all_data = []
        for yi in self.data:
            for featureset in self.data[yi]:
                for feature in featureset:
                    all_data.append(feature)

        self.max_feature_value = max(all_data)
        self.min_feature_value = min(all_data)

        all_data = None

        #For optimisation of SVM
        step_sizes = [self.max_feature_value * 0.1,
                      self.max_feature_value * 0.01,
                      self.max_feature_value * 0.001]

        #Optimising the bias value
        b_range_multiple = 5
        
        

    def predict(self, features):
        # Returns the sign when evaluating( x.w+b )
        classification = np.sign(np.dot(np.array(features),self.w)+self.b)

        return classification
        

data_dict = {-1:np.array([[1,7]
                          [2,8]
                          [3,8],])
             ,1:np.array([[5,1]
                          [6,-1]
                          [7,3],])}

