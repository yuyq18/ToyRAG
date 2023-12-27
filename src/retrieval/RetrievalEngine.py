from argparse import ArgumentParser
from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch(hosts="http://localhost:9200")

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
        print(df.head(5))
        # for col in df.columns:
        #     print(col, df[col].unique().shape[0])
        for i in range(1):
            print('Title', df.loc[i, 'Title'])
            print("=====================")
            print('Description', df.loc[i, 'Description'])
            print("=====================")
            print('Body', df.loc[i, 'Body'])
            print("=====================")
            print('Keywords', df.loc[i, 'Keywords'])
            print("=====================")
        return df

    def build_index(self):
        df = self.load_data()
        # create indices
        mapping = {
            'properties': {
                'Body': {
                    'type': 'text',
                    'analyzer': 'whitespace',
                    'search_analyzer': 'whitespace'
                }
            }        
        }
        if es.indices.exists(index="corpus"):
            es.indices.delete(index="corpus")
        es.indices.create(index="corpus", ignore=400)
        es.indices.put_mapping(index='corpus', body=mapping)

        # build index
        # for quote in quotes:
        #     es.index(index='corpus', document=quote)
        for i in range(len(df)):
            doc = {
                "Title": df.loc[i, 'Title'],
                "Description": df.loc[i, 'Description'],
                "Body": df.loc[i, 'Body'],
                "Keywords": df.loc[i, 'Keywords'],
            }
            es.index(index='corpus', document=doc)
        print("finish index")

    def query(self, query):
        query = {
            'match': {
                'Body': query,
            }
        }
        result = es.search(index='corpus', query=query, size=10000)  # search
        res_df = pd.json_normalize(result['hits']['hits'])  # 转为 dataframe
        print(res_df.head())
        # pass
        return res_df
    