import psutil
import time
from sklearn.metrics import accuracy_score
# This class tests the incoming model in different aspects and gives the ouput to the extractor in the pipeline.
class Evaluator(object):

    def __init__(self, x_test=None, y_test=None):
        self.x_test = x_test
        self.y_test = y_test
        self.outcome = {}

    def __test_accuracy(self):
        # randomly test the model with random 10% of the data
        predictions = self.model.predict(self.x_test)
        self.outcome["accuracy"] = accuracy_score(self.y_test, predictions)
        

    def __test_efficiency(self):
        # run the model with 10%, 20%, 50%, 75% and 100% of the data and for each check how much time it takes and how much usage the computer has
        percantages = [0.1, 0.2, 0.5, 0.75, 1]
        self.outcome["efficiency"] = {}
        for i in percantages:
            # take the current percantage of data from x and y make sure they are same index so y and x from the same row stay same row
            x_test = self.x_test[:int(len(self.x_test) * i)]
            # run the model with the current data
            start_time = time.time()
            predictions = self.model.predict(x_test)
            end_time = time.time()
            # get the usage of the computer
            cpu_usage = psutil.cpu_percent()
            # get the time it took to run the model
            time_taken = end_time - start_time
            # add the results to the outcome
            self.outcome["efficiency"][f"{i*100}%"] = {"amountOfData": i, "time": time_taken, "cpu_usage": cpu_usage, "ram_usage": psutil.virtual_memory().percent}
            if i == 1:
                self.predictions = predictions


    def __test_metrics(self):
        # test the different metrics for the specific type (classification or regression)
        if self.algo_type == "classification":
            # calculate the f1-score, precision and recall from the self.predictions
            true_positive = 0
            false_positive = 0
            true_negative = 0
            false_negative = 0
            # true positive is when we predicted its 1 and it was 1
            for i in range(len(self.predictions)):
                if self.predictions[i] == 1 and self.y_test.iloc[i] == 1:
                    true_positive += 1
                # false positive is when we predicted its 1 and it was 0
                elif self.predictions[i] == 1 and self.y_test.iloc[i] == 0:
                    false_positive += 1
                # true negative is when we predicted its 0 and it was 0
                elif self.predictions[i] == 0 and self.y_test.iloc[i] == 0:
                    true_negative += 1
                # false negative is when we predicted its 0 and it was 1
                elif self.predictions[i] == 0 and self.y_test.iloc[i] == 1:
                    false_negative += 1
            if true_positive + false_positive == 0:
                precision = 0
            else:
                precision = true_positive / (true_positive + false_positive)
            if true_positive + false_negative == 0:
                recall = 0
            else:
                recall = true_positive / (true_positive + false_negative)
            if precision + recall == 0:
                f1_score = 0
            else:
                f1_score = 2 * (precision * recall) / (precision + recall)
            self.outcome["metrics"] = {"precision": precision, "recall": recall, "f1_score": f1_score, "true_positive": true_positive, "false_positive": false_positive, "true_negative": true_negative, "false_negative": false_negative}
        elif self.algo_type == "regression":
            # we will calculate the MAE,MSE,RMSE,R2 from the self.predictions
            mae = abs(self.predictions - self.y_test).mean()
            mse = ((self.predictions - self.y_test) ** 2).mean()
            rmse = ((self.predictions - self.y_test) ** 2).mean() ** 0.5
            r2 = 1 - ((self.predictions - self.y_test) ** 2).mean() / ((self.y_test - self.y_test.mean()) ** 2).mean()
            self.outcome["metrics"] = {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}
        else:
            raise ValueError("Provide a valid algo_type")



    def __test_model(self):
        if self.x_test is None or self.y_test is None:
            raise ValueError("Provide a test data set")
        # test the model in different aspects
        if self.algo_type == "classification":
            self.__test_accuracy()
        self.__test_efficiency()
        self.__test_metrics()

    def evaluate(self, model=None, algo_type=None):
        if model is None:
            raise ValueError("Provide a model")
        self.model = model
        self.algo_type = algo_type
        # test the model in different aspects
        self.__test_model()
        # return the outcome of the model
        return self.outcome