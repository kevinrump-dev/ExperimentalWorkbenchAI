import psutil
import time
# This class tests the incoming model in different aspects and gives the ouput to the extractor in the pipeline.
class Evaluator(object, test_data=None):

    def __init__(self):
        self.test_data = None
        self.__test_model()
        self.outcome = {}

    def __test_accuracy(self):
        # randomly test the model with random 10% of the data
        accuracy = []
        for i in range(5):
            random_test_data = self.test_data.sample(frac=0.1)
            accuracy.append(self.model.predict(random_test_data))
        self.outcome["accuracy"] = accuracy
        

    def __test_efficiency(self):
        # run the model with 10%, 20%, 50%, 75% and 100% of the data and for each check how much time it takes and how much usage the computer has
        percantages = [0.1, 0.2, 0.5, 0.75, 1]
        for i in percantages:
            # get the data for the current percentage
            current_data = self.test_data.sample(frac=i)
            # run the model with the current data
            start_time = time.time()
            predictions = self.model.predict(current_data)
            end_time = time.time()
            # get the usage of the computer
            cpu_usage = psutil.cpu_percent()
            # get the time it took to run the model
            time_taken = end_time - start_time
            # add the results to the outcome
            self.outcome["efficiency"][f"{i*100}%"] = {"amountOfData": i, "time": time_taken, "cpu_usage": cpu_usage, "ram_usage": psutil.virtual_memory().percent}
            if i == 1:
                self.predictions = predictions


    def __test_convergence(self):
        # test the convergence of the model, like how fast and how often the model converges
        pass

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
                if self.predictions[i] == 1 and self.test_data.iloc[i]["class"] == 1:
                    true_positive += 1
                # false positive is when we predicted its 1 and it was 0
                elif self.predictions[i] == 1 and self.test_data.iloc[i]["class"] == 0:
                    false_positive += 1
                # true negative is when we predicted its 0 and it was 0
                elif self.predictions[i] == 0 and self.test_data.iloc[i]["class"] == 0:
                    true_negative += 1
                # false negative is when we predicted its 0 and it was 1
                elif self.predictions[i] == 0 and self.test_data.iloc[i]["class"] == 1:
                    false_negative += 1
            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            f1_score = 2 * (precision * recall) / (precision + recall)
            self.outcome["metrics"] = {"precision": precision, "recall": recall, "f1_score": f1_score, "true_positive": true_positive, "false_positive": false_positive, "true_negative": true_negative, "false_negative": false_negative}
        elif self.algo_type == "regression":
            # we will calculate the MAE,MSE,RMSE,R2 from the self.predictions
            mae = 0
            mse = 0
            rmse = 0
            r2 = 0
            for i in range(len(self.predictions)):
                mae += abs(self.predictions[i] - self.test_data.iloc[i]["class"])
                mse += (self.predictions[i] - self.test_data.iloc[i]["class"]) ** 2
                rmse += (self.predictions[i] - self.test_data.iloc[i]["class"]) ** 2
                r2 += (self.predictions[i] - self.test_data.iloc[i]["class"]) ** 2
            mae = mae / len(self.predictions)
            mse = mse / len(self.predictions)
            rmse = rmse / len(self.predictions)
            r2 = r2 / len(self.predictions)
            self.outcome["metrics"] = {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}
        else:
            raise ValueError("Provide a valid algo_type")



    def __test_model(self):
        if self.test_data is None:
            raise ValueError("Provide a test data set")
        # test the model in different aspects
        self.__test_accuracy()
        self.__test_efficiency()
        self.__test_convergence()
        self.__test_metrics()

    def evaluate(self, model, algo_type=None):
        if model is None:
            raise ValueError("Provide a model")
        self.model = model
        self.algo_type = algo_type
        # test the model in different aspects
        self.__test_model()
        # return the outcome of the model
        return self.outcome