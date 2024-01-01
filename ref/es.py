# from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from app.utils import *
import random
import pandas as pd
import sys
sys.path.append("..")
# from seg.deepthulac.compressed_infer import Seg
# lac = Seg.load(path='../seg/deepthulac/checkpoint', pretrain_dir='../seg/deepthulac/custom_pretrained/vocab.txt')

# 确认已在本地启动了Elasticsearch
# https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html
es = Elasticsearch(hosts="http://localhost:9200")



# quotes = load_json('data/corpus.json')
news = pd.read_csv('data/news.csv')

def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    return obj

# 分词器
# lac = Seg.load(path='seg/deepthulac/checkpoint', pretrain_dir='seg/deepthulac/custom_pretrained/vocab.txt')

# Elasticsearch
es = Elasticsearch(hosts="http://localhost:9200")

# 全部语料和测试集
quotes = load_json('data/corpus.json')
test_set = load_json('data/test_easy.json')

# create indices
# mapping = {
#     'properties': {
#         'content_seg': {
#             'type': 'text',
#             'analyzer': 'whitespace',
#             'search_analyzer': 'whitespace'
#         }
#     }        
# }
# if es.indices.exists(index="corpus"):
#     es.indices.delete(index="corpus")
# es.indices.create(index="corpus", ignore=400)
# es.indices.put_mapping(index='corpus', body=mapping)

# build index
# for quote in quotes:
#     es.index(index='corpus', document=quote)
# print("finish index")

# search
query = {
    'match': {
        'content_seg': "时光 如 河水"
    }
}

def index(query):
    # 调用选定的方法
    # results = bm25_api(query)
    results = improved_api(query)
    return results


def random_api(query):
    return random.sample(quotes, 10)


def bm25_api(query):
    # baseline实现：
    #   建立索引时，使用es默认的BM25相似度，对空格分词的名句使用whitespace作为analyzer；
    #   查询时，对query进行空格分词，然后作为match的参数进行查询。
    # TODO: 实现BM25相似度查询，在此处调用es的api（已建好表）
    words = lac.seg([query])  # query 分词
    query = {
        'match': {
            'content_seg': ' '.join(words[0])
        }
    }
    result = es.search(index='corpus', query=query, size=10000)  # search
    df = pd.json_normalize(result['hits']['hits'])  # 转为 dataframe
    df.rename(columns = {"_source.content": "content", "_source.author":"author"},  inplace=True)
    ret = df.loc[:, ['content', 'author']].to_json(orient='records', force_ascii=False)
    return eval(ret)

# stopword_list = [k.strip() for k in open('data/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list = ['的', '地', '在', '、', '会', '要']
def improved_api(query):
    # TODO: 实现你的改进算法，使之在测试集上性能超过baseline。
    # 例如:
    #   算法挑选查询中的重要词，移除不重要的词（包括去停用词）；
    #   对BM25的前k个结果进行rerank，在BM25公式中使用调和平均，使与query具有更多共同词的名言排在更前面；
    #   结合字和词的混合检索策略；
    #   更多其他改进策略。
    words = lac.seg([query])  # query 分词
    # 去除停用词
    new_query_words = [w for w in words[0] if w not in stopword_list]
    query = {
        'match': {
            'content_seg': ' '.join(new_query_words)
        }
    }
    result = es.search(index='corpus', query=query, size=10000)
    df = pd.json_normalize(result['hits']['hits'])  # 转为 dataframe
    df.rename(columns = {"_source.content": "content", "_source.author":"author"},  inplace=True)
    ret = df.loc[:, ['content', 'author']].to_json(orient='records', force_ascii=False)
    return eval(ret)
