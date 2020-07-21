"""
        #author :   Fatih Kahraman
        #mail   :   fatih.khrmn@hotmail.com
        #web    :   www.fkahraman.com
"""

from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

import numpy as np
import os, joblib

def train_model():

    data = np.loadtxt("DATA/data.csv", delimiter=' ')

    X = data[:,:-1]

    y = data[:,-1]

    if not os.path.exists('DATA/'):
        os.makedirs('DATA/')

    feature_nb = 15

    # Select top K features
    k_best_selector = SelectKBest(f_regression, k=feature_nb)

    # Initialize Extremely Random Forests classifier
    classifier = ExtraTreesClassifier(n_estimators=10, max_depth=feature_nb*2)

    # Construct the pipeline
    processor_pipeline = Pipeline([('selector', k_best_selector), ('erf', classifier)])

    # Set the parameters
    processor_pipeline.set_params(selector__k=feature_nb, erf__n_estimators=5)

    # Training the pipeline
    processor_pipeline.fit(X, y)

    score = processor_pipeline.score(X, y)

    # Print scores
    print('Score: %{}'.format(round(score*100, 2)))

    if not os.path.exists('MODEL/'):
        os.makedirs('MODEL/')

    # Model persistence
    output_model_file = 'MODEL/model_RF.sav'

    # Save the model
    with open(output_model_file, 'wb') as f:
        joblib.dump(processor_pipeline, f)

if __name__ == '__main__':
    train_model()
