import uuid

from langchain.text_splitter import CharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_community.vectorstores import FAISS
#from langchain_openai import ChatOpenAI
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import ConversationalRetrievalChain


def get_text_chunks(text):
    """
    对文本进行块的分割
    :param text:
    :return:
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=128,
        chunk_overlap=10,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    chunks_ids = [str(uuid.uuid4()) for _ in chunks]
    return chunks, chunks_ids


#def get_vectorstore(text_chunks):
#    # 利用openAI的嵌入式搜索系统进行文本搜索
#    embeddings = HuggingFaceEmbeddings()
#    # FAISS 相似向量检索库
#    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#    return vectorstore

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#def get_conversation_chain(vectorstore):
#    """
#    创建一个检索链
#    :param vectorstore:
#    :return:
#    """
#    llm = ChatOpenAI(
#        api_key='sk-56edad48480b449a99a6a37267cabc90',
#        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#        model="qwen-plus"
#    )
#    memory = ConversationBufferMemory(
#        memory_key='chat_history', return_messages=True)
#    conversation_chain = ConversationalRetrievalChain.from_llm(
#        llm=llm,
#        retriever=vectorstore.as_retriever(),
#        #memory=memory
#    )
#    return conversation_chain


#def parse(user_question, raw_text):
#    """
#    主要函数 对用户输入问题进行处理
#    :param raw_text:
#    :param user_question:
#    :return:
#    """
#    # 站点解析
#
#    if raw_text:
#        # 分块
#        text_chunks = get_text_chunks(raw_text)
#        # 创建向量库
#        vectorstore = get_vectorstore(text_chunks)
#        # 返回数据
#        ret_data = get_conversation_chain(vectorstore)({'question': user_question})
#        return ret_data['answer']


if __name__ == '__main__':
    #parse("这篇文章讲的什么？", "")
    pass
