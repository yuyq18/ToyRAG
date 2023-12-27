from argparse import ArgumentParser
from src.retrieval import *

def main():
    init_parser = ArgumentParser()
    # init_parser.add_argument('-m', '--mode', type=str, required=True, help='The main function to run')
    init_args, init_extras = init_parser.parse_known_args()

    # bulid index
    test_retrieval_engine = RetrievalEngine(type="es")
    test_retrieval_engine.build_index()

    test_query = 'an explosion in Pennsylvania'
    res_df = test_retrieval_engine.query(query=test_query)
    print(res_df['_source.Description'])
if __name__ == '__main__':
    main()