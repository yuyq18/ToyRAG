# ToyRAG
THU-Advanced Machine Learning(Fall 2023) HW3: Retrieval-augmented generation (RAG)

### TODO:

1. LLM: ChatGPT-3.5-turbo (已完成)
2. ES: build index and test toy data （已完成）
3. bulid several test examples to test.csv
4. reconsider the format of retrieval results as prompt
5. effectiveness of the test query "Please describe the explosion happened in Pennsylvania in 2023."
6. 基于Embeddings的方法？


## 实现细节

### Retrieval Method

考虑如下两种检索方法：

1. 基于ES的BM25模型

基于 elastic-search 为 news 数据集建立数据库，检索时在 ["Title", "Description", "Body", "Keywords"] 几个字段进行模糊搜索。

2. 

（基于langchain.embeddings OpenAIEmbeddings） 

对文本进行编码并计算内积相似度

### Language model

选择 ChatGPT-3.5-turbo 作为本次作业的语言模型，调用api接口。

### Enhanced Method

将检索到的结果作为“reference information”拼接进给LLM的输入中，例如 query + "Here is some reference information: " + retrieval_results

## 效果展示

测试如下三个问题：
1. Please describe the explosion happened in Pennsylvania in 2023.
2. TODO
3. TODO

对比在拼接检索结果前后的回答：

TODO
