#from langchain.chains import create_retrieval_chain
#from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from chain_util import format_docs
from db_mapper import db
from prompt import prompt

_llm = ChatOpenAI(
    api_key='sk-56edad48480b449a99a6a37267cabc90',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus"
)

class RagChain:

    def __init__(self, f_name, rag_db=db):
        #self._qa_chain = create_stuff_documents_chain(_llm, prompt)

        #self._rag_chain = create_retrieval_chain(
        #    rag_db.as_retriever(), self._qa_chain)
        self._rag_chain = (
            {
                'context': rag_db.as_filter_by_file_retriever(f_name) | format_docs,
                'question': RunnablePassthrough(),
            }
            | prompt
            | _llm
            | StrOutputParser()
        )


    def _invoke(self, q):
        if isinstance(q, str):
            return self._rag_chain.invoke(q)

        if isinstance(q, object):
            if not hasattr(q, 'input'):
                return {
                    'answer': '',
                }

            return self._rag_chain.invoke(q.input)

        if isinstance(q, list) or isinstance(q, tuple):
            return self._rag_chain.invoke(' '.join(list(q)))


    def __call__(self, q):
        return self._invoke(q)


    def invoke(self, q):
        return self._invoke(q)

if __name__ == '__main__':
    db.open('test-text')
    ctn = ''
    with open('../test/a.txt', 'r') as f:
        ctn = f.read()
        print(ctn)

    db.save_doc(ctn, 'a.txt')
    #db.filter_by_file('a.txt')

    rag = RagChain('a.txt')
    print(rag('这篇文章说了什么？'))
    db.close('test-text')

