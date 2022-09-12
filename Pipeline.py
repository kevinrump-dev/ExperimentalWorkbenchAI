from Analyzer import Analyzer
from Evaluator import Evaluator
from JSONExtractor import JSONExtractor
from GraphicalExtractor import GraphicalExtractor


class Pipeline(object):

    def __init__(self, steps, model, config, preprocessor=None):
        self.steps = steps
        self.config = config
        self.model = model
        self.preprocessor = preprocessor
        self.__check_steps()
        self.__check_model()
        self.__check_config()

    def __check_steps(self):
        # go through the input an check
        if not isinstance(self.steps[0], Analyzer):
            raise TypeError("First Step must be an Analyser")
        if not isinstance(self.steps[1], Evaluator):
            raise TypeError("Second Step must be an Evaluator")
        if not isinstance(self.steps[2], (JSONExtractor, GraphicalExtractor)):
            raise TypeError("Third Step must be an Extractor")
        if len(self.steps) > 3:
            if not isinstance(self.steps[-1], GraphicalExtractor):
                raise TypeError("Last Step must be an Graphical Extractor")

    def __check_config(self):
        # the config has to contain certain keys: type, outputType, outputFileType, outputFileName, outputFilePath
        if not "type" in self.config:
            raise KeyError("Config must contain a type")
        if not "outputType" in self.config:
            raise KeyError("Config must contain an outputType")
        if self.config["outputType"] is ("Graphical" or "*"):
            if not "outputFileType" in self.config:
                raise KeyError("Config must contain an outputFileType")
        if not "outputFileName" in self.config:
            raise KeyError("Config must contain an outputFileName")
        if not "outputFilePath" in self.config:
            raise KeyError("Config must contain an outputFilePath")
        if not "trainedState" in self.config:
            raise KeyError("Config must contain a trainedState")
        if self.config["trainedState"] == False:
            if self.preprocessor is None:
                raise KeyError("Provide a preprocessor if the model is not trained")


    def __check_model(self):
        # check if the model has the right methods we need for the documentation
        if not hasattr(self.model, "predict"):
            raise AttributeError("Model must have a predict method")
        if not hasattr(self.model, "fit"):
            raise AttributeError("Model must have a fit method")
        if self.config["type"] == "classification" and not hasattr(self.model, "predict_proba"):
            raise AttributeError("Classification Model must have a predict_proba method")

    def test(self):
        # first call the analyser
        outcome_analyser = self.steps[0].analyze()
        # then call the evaluator
        outcome_evaluator = self.steps[1].evaluate(self.model, self.config["type"])
        # when outputType is graphical, call the graphical extractor
        if self.config["outputType"] == "Graphical":
            self.steps[2].extract(self.config["outputFileType"], self.config["outputFileName"], self.config["outputFilePath"], outcome_evaluator, outcome_analyser)
        # when outputType is JSON, call the JSON extractor
        elif self.config["outputType"] == "JSON":
            self.steps[2].extract(self.config["outputFileName"], self.config["outputFilePath"], outcome_evaluator, outcome_analyser)
        # when outputType is *, call the graphical and JSON extractor
        elif self.config["outputType"] == "*":
            self.steps[2].extract(self.config["outputFileName"], self.config["outputFilePath"], outcome_evaluator, outcome_analyser)
            self.steps[3].extract(self.config["outputFileType"], self.config["outputFileName"], self.config["outputFilePath"], outcome_evaluator, outcome_analyser)