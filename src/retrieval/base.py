from loguru import logger
from argparse import ArgumentParser

class BaseModel:
    @staticmethod
    def parse_retrieval_args(parser: ArgumentParser) -> ArgumentParser:
        raise NotImplementedError
    
    def __init__(self):
        pass
    
    def __getattr__(self, __name: str) -> any:
        # return none if attribute not exists
        if __name not in self.__dict__:
            return None
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{__name}'")


    def build(self):
        raise NotImplementedError

    def query(self, query):
        raise NotImplementedError
