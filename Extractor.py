
from abc import abstractmethod


class Extractor(object):
    
    def __init__(self, model):
        self.model = model
    
    @abstractmethod
    def extract(self):
        pass
