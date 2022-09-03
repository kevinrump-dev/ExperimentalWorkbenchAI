
from abc import abstractmethod


class Extractor(object):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def extract(self):
        pass
