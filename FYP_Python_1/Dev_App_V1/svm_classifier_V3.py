#Support vector machine classifier

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

class Support_Vector_Machine:
    def __init__(self, visualization=True): #Visualisation is in case we want to plot our classifier
        self.visualization = visualization
        self.colors = {1:"r",-1:"b"}
        if self.visualization:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1,1,1)

    def fit(self, data):
        # Training the algorithm based on fed in feature data
        self.data = data
        
        #The aim of this bit of code is to choose the best values for the vectors w and b that will guarantee
        #The best performance on future data. This is equivalent to choosing the decision boundary/separating
        #Hyperplane that is the furthest distance from both support vectors
        #We have asserted that the support vectors satisfy the equation yi(xi.w+b)=0, and that we want to min
        #The magnitude of w
        
        opt_dict = {} #{ ||w||: [w,b] } Dictionary, key is magnitude of w, values are w and b

        #Transforms applied to the w vectors, as the vector elements can have different signs but give same mag
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

        all_data = None #So we don't have to carry around the data in memory
        
        #For optimisation of SVM
        step_sizes = [self.max_feature_value * 0.1,
                      self.max_feature_value * 0.01,
                      self.max_feature_value * 0.001]

        #Optimising the bias value
        b_range_multiple = 5
        b_multiple = 5
        latest_optimum = self.max_feature_value*10

        for step in step_sizes:
            w = np.array([latest_optimum, latest_optimum])
            optimized = False
            while not optimized:
                for b in np.arange(-1*(self.max_feature_value*b_range_multiple),
                                   self.max_feature_value*b_range_multiple,
                                   step.b_multiple):
                    for transformation in transforms:
                        w_t = w*transformation
                        found_option = True

                        for i in self.data:
                            for xi in self.data[i]:
                                yi = i
                                if not yi*(np.dot(w_t,xi)+b) >= 1:
                                    found_option = False

                        if found_option:
                            opt_dict[np.linalg.norm(w_t)] = [w_t,b]

                if w[0] < 0:
                    optimized = True
                    print("Optimised a step")
                else:
                    w = w - step

            norms = sorted([n for n in opt_dict])
            opt_choice = opt_dict[norms[0]]
            self.w = opt_choice[0]
            self.b = opt_choice[1]
            latest_optimum = opt_choice[0][0] + step*2
            
                    
        

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

