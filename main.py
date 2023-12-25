from argparse import ArgumentParser
from src.retrieval import *

def main():
    init_parser = ArgumentParser()
    # init_parser.add_argument('-m', '--mode', type=str, required=True, help='The main function to run')
    init_args, init_extras = init_parser.parse_known_args()

    test_retrieval_engine = RetrievalEngine(type="es")
    test_retrieval_engine.load_data()

if __name__ == '__main__':
    main()