# util.py is a class used for static methods that are used throughout the project

# Used to check if the params are valid
# param - x_value: int between 0 - 100
# param - y_value: int between 0 - 100
# returns: true if params are valid, otherwise false.
def valid_params(x_value, y_value):
    if x_value is None or y_value is None:
        return False
    elif not isinstance(x_value, int) or not isinstance(y_value, int):
        return False
    elif x_value > 100 or y_value > 100:
        return False
    elif x_value < 0 or y_value < 0:
        return False
    else:
        return True