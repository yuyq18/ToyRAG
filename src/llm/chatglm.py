import zhipuai
from .base import BaseLLM
from argparse import ArgumentParser
from loguru import logger
import json
 
# example:

# zhipuai.api_key = "your api key"
# response = zhipuai.model_api.sse_invoke(
#     model="chatglm_turbo",
#     prompt=[
#         {"role": "user", "content": "你好"},
#         {"role": "assistant", "content": "我是人工智能助手"},
#         {"role": "user", "content": "你叫什么名字"},
#         {"role": "assistant", "content": "我叫chatGLM"},
#         {"role": "user", "content": "你都可以做些什么事"},
#     ]
# )
