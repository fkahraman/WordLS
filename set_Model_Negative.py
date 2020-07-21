"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""

from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

import numpy as np
from sklearn.model_selection import train_test_split
import pickle, os

from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn import svm

from sklearn.neighbors import NearestCentroid


data = np.loadtxt("DATA/negative_data_structure.txt", delimiter=' ')

X = data[:,:-1]

y = data[:,-1]

print('Data sayısı: ', len(y))

#Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.201, random_state=np.random.randint(1000), shuffle=True)

print("Train: ", len(y_train))
print("Test: ", len(y_test))

feature_nb = 12

# Select top K features
k_best_selector = SelectKBest(f_regression, k=feature_nb)

# Initialize Extremely Random Forests classifier
classifier = ExtraTreesClassifier(n_estimators=60, max_depth=feature_nb*2)

# Construct the pipeline
model = Pipeline([('selector', k_best_selector), ('erf', classifier)])

# Set the parameters
model.set_params(selector__k=feature_nb, erf__n_estimators=30)

# Training the pipeline
model.fit(X, y)

if not os.path.exists('MODEL/'):
    os.makedirs('MODEL/')

score = model.score(X_test, y_test)

# Print scores
print("\nScore: %", round(score*100, 2))


# Model persistence
output_model_file = 'MODEL/model_negative.pkl'

# Save the model
with open(output_model_file, 'wb') as f:
    pickle.dump(model, f)