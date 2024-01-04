import os
import sys
from argparse import ArgumentParser
from loguru import logger
import pandas as pd
from src.retrieval import *
from src.llm import *
from src.utils import *


def parse_base_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument('--retrieval', type=str, default='ES', choices=['ES', 'Embed'], help='retrieval engine type')
    parser.add_argument('--llm', type=str, default='GPT', choices=['GPT'], help='llm type')
    parser.add_argument('--test_data', type=str, default='data/test.csv', help='Test data file')
    parser.add_argument('--verbose', type=str, default='INFO', choices=['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'], help='Log level')
    return parser

def main():
    parser = ArgumentParser()
    parser = parse_base_args(parser)
    args, extras = parser.parse_known_args()

    logger.remove()
    logger.add(sys.stderr, level=args.verbose)
    os.makedirs('logs', exist_ok=True)
    # log name use the time when the program starts, level is INFO
    logger.add('logs/{time:YYYY-MM-DD:HH:mm:ss}.log', level='DEBUG')

    # get retrieval model
    try:
        retrieval_model = eval(args.retrieval+'Model')()
    except NameError:
        logger.error('No such retrieval_model!')
    # get llm model
    try:
        llm_model = eval(args.llm+'LLM')()
    except NameError:
        logger.error('No such LLM!')
    
    # build index
    # retrieval_model.build()

    # test
    df = pd.read_csv(args.test_data)
    for i in range(len(df)):
        query = df.loc[i, 'query']
        retrieval_docs = retrieval_model.query(query=query)
        retrieval_res = format_docs(retrieval_docs)
        llm_response, llm_response_ref = llm_model.step(question=query, retrieval_res=retrieval_res)
        logger.success(llm_response)
        logger.success(llm_response_ref)
    
    
if __name__ == '__main__':
    main()