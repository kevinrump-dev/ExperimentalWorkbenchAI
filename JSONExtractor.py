import json
import numpy as np

def np_encoder(object):
        if isinstance(object, np.generic):
            return object.item()

class JSONExtractor(object):
    def __init__(self):
        self.output = {}

    def extract(self, output_filename,output_path, evaluator_outcome, analyzer_outcome):
        self.output["outputFileName"] = output_filename
        self.output["outputFilePath"] = output_path
        self.output["Evaluation"] = evaluator_outcome
        self.output["Analysis"] = analyzer_outcome

        with open(output_path + output_filename +".json", 'w') as outfile:
            json.dump(self.output, outfile, default=np_encoder)