#Support vector machine classifier

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pickle
style.use('ggplot')

class Support_Vector_Machine:
    def __init__(self, features_df):
        #Extracting data from the dataframe

        y = features_df.loc[:,"class label"] #Y is an array with dimensions [1, num_samples]

        num_samples = len(y)
        
        features = list(features_df) #Returns the column headings/feature names (w/ class label col)
        features.pop() #Removes the last class label column
        self.num_features = len(features)
        
        data_dict_positive = [] #Empty list to store feature sets from positive samples in
        data_dict_negative = []
        feature_set = [] #An empty list to store individual sample feature sets into


        for yi in range(num_samples):
            feature_set.clear()
            for feature in features: #Creates the individual feature sets for each samples
                feature_set.append(features_df.loc[yi, feature])

            if features_df.loc[yi,"class label"] == 1: #If the class label is 1
                data_dict_positive.append(feature_set) #Append the featureset to the collection of positive featuresets

            else:
                data_dict_negative.append(feature_set)

        data_dict = {-1:np.array(data_dict_negative), 1:np.array(data_dict_positive)}

        self.data = data_dict

    def fit(self):
        
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

        w = np.zeros([self.num_features])
        w = [latest_optimum for i in self.num_features]

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
        
filename = "/home/pi/FYP_Python_1/FYP_Python_1/Dev_App_V1/featurearray_2.pickle"
pickle_in = open(filename,"rb") #We would like to open a file to read data from
features_df = pickle.load(pickle_in)
pickle_in.close()


SVM = Support_Vector_Machine(features_df)

print(SVM.data)
        


























