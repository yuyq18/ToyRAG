from argparse import ArgumentParser
from elasticsearch import Elasticsearch
import pandas as pd
from tqdm import trange
from loguru import logger
from .base import BaseModel

class ESModel(BaseModel):
    @staticmethod
    def parse_retrieval_args(parser: ArgumentParser) -> ArgumentParser:
        parser.add_argument('--max_doc', type=int, default=5, help='max document number for each query')
        parser.add_argument('--dataset', type=str, default='news', help='dataset name')
        parser.add_argument('--data_path', type=str, default='data/news.csv', help='retrieval data file')
        return parser
    
    def __init__(self):
        parser = ArgumentParser()
        parser = self.parse_retrieval_args(parser)
        args, extras = parser.parse_known_args()

        self.data_path = args.data_path
        self.dataset = args.dataset
        self.max_doc = args.max_doc
        # log the arguments
        logger.success(args)
        super().__init__()


    def build(self):
        es = Elasticsearch(hosts="http://localhost:9200", timeout=300)
        mapping = {
            'properties': {
                'Title': {
                    'type': 'text',
                    'analyzer': 'standard',
                    'search_analyzer': 'standard'
                },
                'Description': {
                    'type': 'text',
                    'analyzer': 'standard',
                    'search_analyzer': 'standard'
                },
                'Body': {
                    'type': 'text',
                    'analyzer': 'standard',
                    'search_analyzer': 'standard'
                }
            }        
        }
        if es.indices.exists(index=self.dataset):
            es.indices.delete(index=self.dataset)
        es.indices.create(index=self.dataset, ignore=400)
        es.indices.put_mapping(index='news', body=mapping)

        # build index
        df = pd.read_csv(self.data_path)
        success = 0
        for i in range(len(df)):
            doc = {
                "Title": df.loc[i, 'Title'],
                "Description": df.loc[i, 'Description'],
                "Body": df.loc[i, 'Body']
            }
            try:
                es.index(index='news', document=doc, request_timeout=300)
                success += 1
            except Exception as e:
                logger.error(e)
                logger.debug(f"Document {i}: {doc}")
        logger.success(f"Finish index for {success} documents.")

    def query(self, query):
        es = Elasticsearch(hosts="http://localhost:9200", timeout=300)
        if not es.indices.exists(index=self.dataset):
            logger.debug("Creating index...")

        query = {
            "multi_match": {
                "query": query,
                "fields": ["Title", "Description", "Body"]
            }
        }
        result = es.search(index='news', query=query, size=self.max_doc)  # search
        res_df = pd.json_normalize(result['hits']['hits'])  # 转为 dataframe
        res_df.rename(columns={'_source.Title': 'Title',
                            '_source.Description': 'Description',
                            '_source.Body': 'Body'}, inplace=True)
        
        return res_df[['Title', 'Description', 'Body']]
    