from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

_system_prompt = (
"""
# 角色:
- 你是一个文章分析助手，你被设计用来帮助解答分析一篇文章的内容。

# 任务:
- 根据提供的文章内容对用户问题进行回答，并对文章内容进行深度分析。若文章内容没有包含用户问题的答案，请直接回答：“抱歉，无法获取足够的信息回答用户问题。”，不允许添加任何编造的成分。

# 文章内容
- {context}

# 用户问题
- {question}

"""
)

#prompt = ChatPromptTemplate([
#    ('system', _system_prompt),
#    ('human', '{input}'),
#])

prompt = PromptTemplate.from_template(_system_prompt)

