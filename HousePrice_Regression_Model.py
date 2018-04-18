# Importing all necessary packages
import numpy as np
import pickle  # Pickle is used to load saved machine learning model from local working directory.
import sys


class HousePricePrediction:
    def __init__(self, data):
        """
        Loads all necessary variables required.
        Data is the input features.
        Decision Tree - is the boosted decision tree which is saved as dt_boosted_model.sav in local drive.
        Random Forest - is the boosted RF which is saved as dt_boosted_model.sav in local drive.
        """

        self.data = data
        self.decisionTree = pickle.load(open("dt_boosted_model.sav", 'rb'))  # Loading the Decision Tree Model
        self.randomForest = pickle.load(open("rf_boosted_model.sav", 'rb'))  # Loading the Random Forest Model
        self.features = None

    def prediction(self):
        """ This function is used to Predict boston House Price.
        This uses 2 Machine Learning Model Decision Tree and Random Forest then take an average to predict House Price.
        """
        no_features = len(self.features)

        self.features = self.features.reshape(1, no_features)

        dt_prediction = self.decisionTree.predict(self.features)  # Prediction using Decision Tree

        rf_prediction = self.randomForest.predict(self.features)  # Prediction using Random Forest

        final_prediction = (dt_prediction + rf_prediction) / 2  # Taking average from 2 models

        return round(final_prediction[0]*1000, 2)

    @staticmethod
    def convert_string_num(x):

        """ This is for validation. To check if the given features/predictors are of type numeric or string.
        If the feature is string, then raise an exception and exit"""

        x = str(x)
        try:
            num = float(x)  # To validate given feature value can be converted to float iff not then exit.
            return num

        except Exception as e:
            sys.exit(e)

    def clean_data(self):

        """ This removes irrelevant features if any. Because for designed machine learning model can only take -
        'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT'.
        If any features other than this, the function removes those features/predictors and take only necessary ones."""

        key_set = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX',
                   'PTRATIO', 'B', 'LSTAT']  # Required features.
        available_key = []  # This list contains the number of features which are available (given as input).

        # Validating feature value should be of type numeric.
        for j in self.data:
            self.data[j] = HousePricePrediction.convert_string_num(self.data[j])

        try:
            for i in key_set:

                if i in self.data.keys():
                    # Append all valid keys (from user input) to the append_key list.
                    available_key.append(i)

            # Takes only those features which are valid.
            new_data = {k: self.data[k] for k in available_key}

            self.data = new_data

        except Exception as e:
            sys.exit(e)

    def missing_value_handling(self):

        """ This function handles the missing features and replace those missing features with mean value.
        In addition, this function maintains the order of the features/predictors which are necessary for ML model."""

        num_features = 13  # max number of features or predictors.

        try:
            if len(self.data.keys()) < num_features:

                # Mean of all predictors
                mean_dict = {"CRIM": 3.59376, "ZN": 11.36364, "INDUS": 11.13678, "CHAS": 0.06917, "NOX": 0.5547,
                             "RM": 6.28463, "AGE": 68.5749, "DIS": 3.79504, "RAD": 9.54941, "TAX": 408.23715,
                             "PTRATIO": 18.45553, "B": 356.67403, "LSTAT": 12.65306}

                # This gives missing predictors (keys).
                miss = set(mean_dict.keys()) - set(self.data.keys())

                # Add missing predictors and its corresponding means are add to the data.
                for i in miss:
                    self.data[i] = mean_dict[i]

                # Final processed data is stored in self.features - which are used in prediction functions.
                # The below line makes sure that order of the predictors are according to the requirement of
                # machine learning model.
                self.features = np.array([self.data['CRIM'], self.data['ZN'], self.data['INDUS'], self.data['CHAS'],
                                          self.data['NOX'], self.data['RM'], self.data['AGE'], self.data['DIS'],
                                          self.data['RAD'], self.data['TAX'], self.data['PTRATIO'],
                                          self.data['B'], self.data['LSTAT']])

            # If no features/predictors are missing - reorder the values as required by ML model.
            elif len(self.data.keys()) == num_features:

                self.features = np.array([self.data['CRIM'], self.data['ZN'], self.data['INDUS'], self.data['CHAS'],
                                          self.data['NOX'], self.data['RM'], self.data['AGE'], self.data['DIS'],
                                          self.data['RAD'], self.data['TAX'], self.data['PTRATIO'],
                                          self.data['B'], self.data['LSTAT']])

        except Exception as e:
            sys.exit(e)
