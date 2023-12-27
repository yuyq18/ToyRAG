from argparse import ArgumentParser
from elasticsearch import Elasticsearch
import pandas as pd
from tqdm import trange

# Elasticsearch
es = Elasticsearch(hosts="http://localhost:9200", timeout=300)

class RetrievalEngine:
    @staticmethod
    def parse_task_args(parser: ArgumentParser) -> ArgumentParser:
        parser.add_argument('--retrieval_config', type=str, default='config/api-config.json', help='Configuration file for retrieval engine')
        parser.add_argument('--data_path', type=str, default='data/news.csv', help='retrieval data file')
        return parser
    
    def __init__(self, type="es"):
        parser = ArgumentParser()
        parser = self.parse_task_args(parser)
        args, extras = parser.parse_known_args()
        self.type = type
        self.data_path = args.data_path

    def load_data(self):
        df = pd.read_csv(self.data_path)
        print('index length: ', len(df))
        return df

    def build_index(self):
        df = self.load_data()
        # create indices
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
                },
                # 'Keywords': {
                #     'type': 'text',
                #     'analyzer': 'standard',
                #     'search_analyzer': 'standard'
                # }
            }        
        }
        if es.indices.exists(index="news"):
            es.indices.delete(index="news")
        es.indices.create(index="news", ignore=400)
        es.indices.put_mapping(index='news', body=mapping)

        # build index
        # for i in range(len(df)):
        for i in trange(50):
            doc = {
                "Title": df.loc[i, 'Title'],
                "Description": df.loc[i, 'Description'],
                "Body": df.loc[i, 'Body'],
                # "Keywords": df.loc[i, 'Keywords'],
            }
            res = es.index(index='news', document=doc, request_timeout=300)
        print("Finish index")

    def query(self, query):
        query = {
            'match': {
                'Description': query,
            }
        }
        result = es.search(index='news', query=query, size=10000)  # search

        print("==================")
        res_df = pd.json_normalize(result['hits']['hits'])  # 转为 dataframe
        print(res_df.columns)
        # pass
        return res_df
    