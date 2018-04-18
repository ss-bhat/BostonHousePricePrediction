from Demo import HousePrice_Regression_Model as Model


def main(data):
    """ This is our main function which calls the class HousePrice Regression Model."""
    features = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX',
                'PTRATIO', 'B', 'LSTAT']

    # This is the validation -
    # If no data - returns message: Please Enter Data
    # If all values are zero - returns a invalid feature.
    if (len(data.keys()) != 0) and (sum(data.values())) != 0:

        # If at least one feature is valid then give the prediction
        if any(i in data.keys() for i in features):
            inst_obj = Model.HousePricePrediction(data)
            inst_obj.clean_data()
            inst_obj.missing_value_handling()
            # Return Json file.
            return inst_obj.prediction()

        return "Entered key is Invalid. At least one valid key-value pair is required for prediction"

    return "Please Enter the Data"
