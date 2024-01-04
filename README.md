# ToyRAG
THU-Advanced Machine Learning(Fall 2023) HW3: Retrieval-augmented generation (RAG)

## 框架实现

本次作业实现了一个简易的检索增强生成框架（RAG），代码已在[github](https://github.com/yuyq18/ToyRAG)上开源。具体实现细节如下：

### Retrieval model

在本作业中，考虑利用elastic-search作为检索模型，为 news 数据集建立数据库并创建索引，利用BM25算法计算相关性分数返回检索结果。

在具体实现上，在框架中实现检索模型的基类，规定`build`和`query`函数接口。针对 elastic-search 实现‘ESModel’类和相应接口。在检索时，对于 ["Title", "Description", "Body"] 几个字段进行模糊搜索，利用BM25算法计算相关性分数，返回相关性最高的几条新闻作为参考信息。


### Language model

选择 ChatGPT-3.5-turbo(下称 GPT3.5) 作为本次作业的语言模型，实现‘LLM’基类和针对GPT调用的‘GPTLLM’类和相应接口，在`step`函数中调用GPT3.5的api接口。在本次试验中将对比同一语言模型下，是否提供检索结果对于实验效果的影响。

### RAG Method

在检索增强方面，考虑将elastic-search检索到的结果作为“reference information”拼接在LLM的输入中，输入文本模板为 `问题` + `Here is some reference information: ` + `检索结果`。


## 效果展示

为验证检索增强的效果，针对性地选择了发生在2023年的新闻事件进行提问。问题类型包括描述事件本身、事件后续影响以及事实性判断等。受篇幅影响，这里展现在下面三个问题上的实验效果：

1. Please describe the explosion happened in Pennsylvania in March 2023.
2. Do you know the casualties and economic losses caused by the floods in Libya？
3. Did Turkey approve Finland’s application to join NATO?

#### 1. 描述2023年3月发生在宾夕法尼亚州的爆炸事件

在未提供检索结果的设定下，GPT3.5无法回答关于这一事件的问题。

```
I'm sorry, but as an AI language model, I don't have access to real-time information or the ability to browse the internet. Therefore, I cannot provide details about specific events that may have occurred in the future, such as an explosion in Pennsylvania in March 2023. It's always best to refer to reliable news sources or local authorities for the most accurate and up-to-date information on any incidents.
```

经过elasticsearch检索后，按相关程度为该问题提供reference information(此处省略大段文本):

```
Title: Death toll from explosion at Pennsylvania candy factory climbs to 4 as hope of finding more survivors wanes  Body: A fourth person has been confirmed dead in an explosion at an eastern Pennsylvania candy factory, officials said Sunday, ...
Title: Candy factory didn't evacuate concerned workers before Pennsylvania explosion that killed 7, OSHA finds ... 
Title: 5 derailed train cars carrying hazardous material at risk of exploding are no longer burning ...
```

可以观察到，elasticsearch成功检索出关于宾夕法尼亚州爆炸事件两条相关新闻进行发挥。

提供检索结果后，GPT3.5的回答为：
```
The explosion at the R.M. Palmer Co. candy factory in Pennsylvania occurred on March 24, 2023. The explosion resulted in the death of seven people and injured nearly a dozen others. The explosion completely leveled the factory building, causing devastation in the community of West Reading.
```

可以看到，GPT3.5根据检索结果对该事件进行了很好的描述。


#### 2. 利比亚洪灾的伤亡情况和经济损失

类似地，在”利比亚洪灾的伤亡情况和经济损失“这一问题上，GPT3.5无法给出回答。

```
I'm sorry, but as an AI language model, I don't have real-time data or access to current news updates. It's best to refer to reliable news sources or government agencies for the most accurate and up-to-date information on casualties and economic losses caused by floods in Libya.
```

而提供elasticsearch的检索结果后，GPT3.5能够正确回答这一问题。

```
According to reports, at least 5,000 people have died, with thousands more missing. The floods have caused extensive damage to buildings, homes, and infrastructure in the affected areas. The International Committee of the Red Cross (ICRC) described the floods as a "catastrophe" and stated that entire neighborhoods were swept into the sea. The floods were caused by heavy rainfall and the bursting of two dams in the country's northeast. The city of Derna has seen the worst of the devastation, with reports of a seven-meter wave wiping out buildings. The floods have also disrupted access to the affected areas, making it challenging for relief workers to deliver aid. The economic losses caused by the floods are yet to be determined.
```


#### 3. 土耳其同意芬兰加入北约了吗？

在”土耳其是否同意芬兰加入北约“这一问题上，GPT3.5给出了错误回答。

```
No, Turkey does not have the authority to approve or reject Finland's application to join NATO. The decision to accept new members into NATO is made collectively by all member states through a consensus-based process.
```

经过elasticsearch检索后，按相关程度为该问题提供reference information:

```
Title: Turkey approves Finland's NATO application, clearing the last hurdle. Sweden is still waiting  Body: Turkey has finally approved Finland’s application to join NATO, ...
Title: Opinion: Finland wants to join NATO. But it may have to ...
Title: Turkey says Sweden was complicit in burning of Quran amid tension over NATO membership bid ...
```

根据检索到的新闻语料，GPT3.5能够正确回答这一问题。

```
Yes, Turkey has approved Finland's application to join NATO. The Turkish Parliament voted unanimously in favor of Finland's membership, clearing the last hurdle in the accession process. All 30 NATO members have now ratified Finland's membership. However, Turkey has not indicated whether it will approve Sweden's NATO membership.
```
