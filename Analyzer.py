import pandas as pd
import json

class Analyzer(object):

    def __init__(self, x_test, y_test, x_columns=None, y_column=None):
        self.x_test = x_test
        self.y_test = y_test
        self.x_columns = x_columns
        self.y_column = y_column
        

    def transform_data(self):
        # transform the data in pandas dataframes
        if self.x_columns and self.y_column:  
            self.x_test = pd.DataFrame(self.x_test, columns=self.x_columns)
            self.y_test = pd.DataFrame(self.y_test, columns=[self.y_column])
        else:
            # check if the data is already in pandas dataframes
            if not isinstance(self.x_test, pd.DataFrame):
                raise TypeError("x_test must be a pandas DataFrame or a numpy array, then you must specify the columns")
            if not isinstance(self.y_test, pd.Series):
                raise TypeError("y_test must be a pandas Series or a numpy array, then you must specify the columns")
    
    def __analyze(self, column, column_name=None):
        column.replace(" ", float("NaN"), inplace=True)
        col = {"header": column_name}
        if list(column.unique()) == [0, 1] or list(column.unique()) == [1, 0] or column.dtype == "object":
            try:
                column = column.astype(float)
                col["type"] = "number"
            except ValueError as e:
                column = column.astype("category")
        if column.dtype.name != "category":
            column.fillna(value=column.median(), inplace=True)
            col["max"] = column.max()
            col["min"] = column.min()
            col["mean"] = column.mean()
            col["median"] = column.median()
            col["std"] = column.std()
            col["var"] = column.var()
            col["type"] = "number"
        if column.dtype.name == "category":
            column.fillna(
                value=column.value_counts().index[0], inplace=True)
            # get the mean of the categories
            col["mean"] = sum(col["data"]) / len(col["data"])
            # add important information to know about categorical data
            col["maxName"] = column.value_counts().index[0]
            col["max"] = column.value_counts()[0]
            col["minName"] = column.value_counts().index[-1]
            col["min"] = list(column.value_counts())[-1]
            col["type"] = "category"
        return col

    def __analyze_x(self):
        analyzed_x = []
        for column in self.x_test:
            col = self.__analyze(self.x_test[column], column)
            analyzed_x.append(col)
        return analyzed_x

    def __analyze_y(self):
        analyzed_y = []
        col = self.__analyze(self.y_test, self.y_test.name)
        analyzed_y.append(col)
        return analyzed_y
    
    def analyze(self):
        self.transform_data()
        self.analyzed_information = {
            "x": self.__analyze_x(),
            "y": self.__analyze_y()
        }
        return self.analyzed_information