# utils.py
#import joblib
#import pickle
import os
import warnings

def load_ml_model(model_path, loader):
    print("Current working directory: ")
    print(os.getcwd() + model_path)
    path = os.getcwd() + model_path
    if loader == "joblib":
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore", DeprecationWarning)
        #     estimator = joblib.load(path)
        #     print(estimator.__getstate__()['_sklearn_version'])
        #return joblib.load(path)
    #elif loader == "pickle":
        #with open(path, 'rb') as f:
            #return pickle.load(f)
        #return pickle.load(path, 'rb')
    #else:
        return None


def make_prediction(model, input_data): 
    return model.predict(input_data)
