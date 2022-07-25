from Analyser import Analyser
from Evaluator import Evaluator
from Extractor import Extractor


class Pipeline(object):

    def __init__(self, steps, model, config, preprocessor=None):
        self.steps = steps
        self.config = config
        self.model = model
        self.preprocessor = preprocessor
        self.__check_input()
        self.__check_model()
        self.__check_config()

    def __check_input(self):
        # go through the input an check
        if not isinstance(self.steps[0], Analyser):
            raise TypeError("First Step must be an Analyser")
        if not isinstance(self.steps[1], Evaluator):
            raise TypeError("Second Step must be an Evaluator")
        if not isinstance(self.steps[2], Extractor):
            raise TypeError("Third Step must be an Extractor")

    def __check_config(self):
        # the config has to contain certain keys: type, parameters, outputType, outputFileType, outputFileName, outputFilePath
        if not "type" in self.config:
            raise KeyError("Config must contain a type")
        if not "outputType" in self.config:
            raise KeyError("Config must contain an outputType")
        if self.config["outputType"] is ("graphical" or "*"):
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
        if not hasattr(self.model, "transform"):
            raise AttributeError("Model must have a transform method")

    def test(self):
        # first call the analyser
        outcome_analyser = self.steps[0].analyse()
        # then call the evaluator
        outcome_evaluator = self.steps[1].evaluate()
        # then call the extractor
        self.steps[2].extract(outcome_analyser, outcome_evaluator)