import json
import pandas as pd
from seg.deepthulac.compressed_infer import Seg
from elasticsearch import Elasticsearch

def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    return obj

# 分词器
lac = Seg.load(path='seg/deepthulac/checkpoint', pretrain_dir='seg/deepthulac/custom_pretrained/vocab.txt')

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

top_k = 10000
recall_3 = 0
recall_10 = 0
recall_50 = 0
mrr = 0

ii = 0

# baseline
# for test_query in test_set:
#     # ii += 1
#     query['match']['content_seg'] = test_query['query_seg']
#     result = es.search(index='corpus', query=query, size=top_k)

#     hit_size = min(result['hits']['total']['value'], top_k)
#     df = pd.json_normalize(result['hits']['hits'])  # 转化为 dataframe 结构
#     contents = df['_source.content']  # 搜索结果的content列表

#     try:  # 计算 rank
#         rank = list(contents).index(test_query['golden_quote']) + 1  
#     except ValueError:
#         rank = (hit_size + len(quotes)) / 2
    
#     mrr += 1/rank
#     recall_3 += (rank <= 3)
#     recall_10 += (rank <= 10)
#     recall_50 += (rank <= 50)

    # print(ii, rank, test_query['query_seg'], test_query['golden_quote'], contents[0])

# improve
# stopword_list = [k.strip() for k in open('data/cn_stopwords.txt', encoding='utf8').readlines() if k.strip() != '']
stopword_list = ['的', '地', '在', '、', '会', '要']

for test_query in test_set:
    ii += 1
    # 1. 去除停用词
    query_words = test_query['query_seg'].split()
    new_query_words = [w for w in query_words if w not in stopword_list]
    query['match']['content_seg'] = ' '.join(new_query_words)

    result = es.search(index='corpus', query=query, size=top_k)

    hit_size = min(result['hits']['total']['value'], top_k)
    df = pd.json_normalize(result['hits']['hits'])  # 转化为 dataframe 结构
    
    contents = df['_source.content']  # 搜索结果的content列表

    try:  # 计算 rank
        rank = list(contents).index(test_query['golden_quote']) + 1  
    except ValueError:
        rank = (hit_size + len(quotes)) / 2
    
    mrr += 1/rank
    recall_3 += (rank <= 3)
    recall_10 += (rank <= 10)
    recall_50 += (rank <= 50)

    print(ii, rank, test_query['query_seg'], test_query['golden_quote'], contents[0])


recall_3 /= len(test_set)
recall_10 /= len(test_set)
recall_50 /= len(test_set)
mrr /= len(test_set)

print("recall@3: %.4f" % recall_3)
print("recall@10: %.4f" % recall_10)
print("recall@50: %.4f" % recall_50)
print("mrr: %.4f" % mrr)

