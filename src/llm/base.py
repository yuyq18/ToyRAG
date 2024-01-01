from loguru import logger
from argparse import ArgumentParser

class BaseLLM:
    @staticmethod
    def parse_llm_args(parser: ArgumentParser) -> ArgumentParser:
        raise NotImplementedError
    
    def __init__(self, args):
        pass
    
    def __getattr__(self, __name: str) -> any:
        # return none if attribute not exists
        if __name not in self.__dict__:
            return None
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{__name}'")

    def step(self, question, retrieval_res):
        raise NotImplementedError