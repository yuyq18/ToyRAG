# ToyRAG
THU-Advanced Machine Learning(Fall 2023) HW3: Retrieval-augmented generation (RAG)

### TODO:

1. LLM: ChatGLM api https://open.bigmodel.cn/dev/api#overview  https://open.bigmodel.cn/usercenter/apikeys
2. es: build index and test toy data （已完成）
3. concate the search results with initial prompts.

### Retrieval-augmented Method

基于ES的BM25模型

1. 先检索再LLM

考虑拼接prompt的方式，例如 query + "Here are some contexts which may help you: " + retrieval_results

2. 多轮检索

3. TODO

参考REPLUG, FLARE等工作


